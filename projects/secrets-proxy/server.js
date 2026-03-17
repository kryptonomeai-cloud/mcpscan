import express from 'express';
import { randomUUID } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import { SecretsStore } from './lib/secrets-store.js';
import { WebAuthnManager } from './lib/webauthn.js';
import { sendApprovalNotification } from './lib/telegram.js';
import { logAudit } from './lib/audit.js';
import { localhostOnly } from './lib/middleware.js';
import { scheduleRotation, performAutoRotation } from './lib/rotation.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(readFileSync(join(__dirname, 'config.json'), 'utf8'));
const DATA_DIR = join(__dirname, 'data');
const STATE_FILE = join(DATA_DIR, 'state.json');
const chatId = () => process.env.TELEGRAM_CHAT_ID || config.telegramChatId;

if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });

// ── State ──────────────────────────────────────────────────────────────────
function loadState() {
  if (!existsSync(STATE_FILE)) return { lockdown: false };
  return JSON.parse(readFileSync(STATE_FILE, 'utf8'));
}
function saveState(s) {
  writeFileSync(STATE_FILE, JSON.stringify(s, null, 2), 'utf8');
}

let state = loadState();
const store = new SecretsStore();
const webauthn = new WebAuthnManager({
  rpID: config.rpID,
  rpName: config.rpName,
  origin: config.origin,
});

// ── In-memory request tracking ─────────────────────────────────────────────
const pendingRequests = new Map();
const standingApprovals = new Map();
const sessionApprovals = new Map();

// ── Expiry sweep ───────────────────────────────────────────────────────────
setInterval(() => {
  const now = Date.now();
  for (const [id, req] of pendingRequests) {
    if (req.status === 'pending' && now - req.createdAt > config.requestTTL * 1000) {
      req.status = 'expired';
      req.expiredAt = new Date().toISOString();
      logAudit({
        event: 'request_expired',
        request_id: id,
        secret_name: req.secretName,
        tier: req.tier,
      });
    }
    // Clean up old entries after 10 minutes
    if (req.status !== 'pending' && now - req.createdAt > 600_000) {
      pendingRequests.delete(id);
    }
  }
  // Sweep expired session approvals
  for (const [name, approval] of sessionApprovals) {
    if (now > approval.expiresAt) {
      sessionApprovals.delete(name);
      logAudit({ event: 'session_approval_expired', secret_name: name });
    }
  }
}, 5000);

// ── Express setup ──────────────────────────────────────────────────────────
const app = express();
app.set('trust proxy', false);
app.use(express.json());
app.use(express.static(join(__dirname, 'public')));

// ── Agent API (localhost only) ─────────────────────────────────────────────

// Request a secret
app.post('/api/request', localhostOnly, (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: 'Missing "name" field' });
  if (!store.has(name)) return res.status(404).json({ error: 'Secret not found' });

  if (state.lockdown) {
    logAudit({ event: 'request_denied_lockdown', secret_name: name });
    return res.status(403).json({ error: 'System in lockdown' });
  }

  const meta = store.getMeta(name);
  const tier = meta.tier;
  const now = Date.now();

  // Standing approval — return immediately if already approved
  if (tier === 'standing' && standingApprovals.has(name)) {
    const requestId = randomUUID();
    const secret = store.get(name);
    logAudit({
      event: 'standing_approval_used',
      request_id: requestId,
      secret_name: name,
      tier,
    });
    return res.json({
      request_id: requestId,
      status: 'approved',
      secret: secret.value,
      tier,
      note: 'Standing approval — no re-auth needed',
    });
  }

  // Session approval — return immediately if within TTL
  if (tier === 'session' && sessionApprovals.has(name)) {
    const approval = sessionApprovals.get(name);
    if (now < approval.expiresAt) {
      const requestId = randomUUID();
      const secret = store.get(name);
      logAudit({
        event: 'session_approval_used',
        request_id: requestId,
        secret_name: name,
        tier,
        session_expires_at: new Date(approval.expiresAt).toISOString(),
      });
      return res.json({
        request_id: requestId,
        status: 'approved',
        secret: secret.value,
        tier,
        session_expires_at: new Date(approval.expiresAt).toISOString(),
        note: 'Session approval — valid within TTL',
      });
    }
    sessionApprovals.delete(name);
  }

  // Normal flow — create pending request
  const requestId = randomUUID();
  pendingRequests.set(requestId, {
    secretName: name,
    status: 'pending',
    createdAt: now,
    tier,
    ip: req.ip,
  });

  logAudit({
    event: 'request_created',
    request_id: requestId,
    secret_name: name,
    tier,
    ip: req.ip,
  });

  // Send Telegram notification
  const approveUrl = `${config.origin}/approve/${requestId}`;
  sendApprovalNotification({
    secretName: name,
    requestId,
    approveUrl,
    chatId: chatId(),
  }).catch(() => {});

  res.json({ request_id: requestId, status: 'pending', tier });
});

// Poll for result
app.get('/api/poll/:requestId', localhostOnly, (req, res) => {
  const entry = pendingRequests.get(req.params.requestId);
  if (!entry) return res.status(404).json({ error: 'Request not found or expired' });

  const response = {
    request_id: req.params.requestId,
    status: entry.status,
    secret_name: entry.secretName,
    tier: entry.tier,
  };

  if (entry.status === 'approved') {
    response.secret = entry.secret;
    response.expires_at = entry.expiresAt;

    // One-time: purge after single read and trigger rotation
    if (entry.tier === 'one-time') {
      pendingRequests.delete(req.params.requestId);
      logAudit({
        event: 'secret_delivered',
        request_id: req.params.requestId,
        secret_name: entry.secretName,
        tier: entry.tier,
      });
      // Trigger rotation asynchronously
      scheduleRotation({
        secretName: entry.secretName,
        store,
        chatId: chatId(),
        requestId: req.params.requestId,
        tier: entry.tier,
      });
    }
  }

  res.json(response);
});

// Revoke standing/session approval
app.post('/api/revoke/:secretName', localhostOnly, (req, res) => {
  const name = decodeURIComponent(req.params.secretName);
  let revoked = false;

  if (standingApprovals.has(name)) {
    standingApprovals.delete(name);
    revoked = true;
  }
  if (sessionApprovals.has(name)) {
    sessionApprovals.delete(name);
    revoked = true;
  }

  logAudit({ event: 'approval_revoked', secret_name: name, revoked });
  res.json({ revoked, secret_name: name });
});

// Manual rotation trigger
app.post('/api/rotate/:secretName', localhostOnly, async (req, res) => {
  const name = decodeURIComponent(req.params.secretName);
  if (!store.has(name)) return res.status(404).json({ error: 'Secret not found' });

  const meta = store.getMeta(name);
  if (meta.rotation !== 'auto') {
    return res.status(400).json({ error: `Secret rotation mode is "${meta.rotation}", not "auto"` });
  }
  if (!store.get(name).rotateCmd) {
    return res.status(400).json({ error: 'No rotateCmd configured for this secret' });
  }

  logAudit({ event: 'manual_rotation_triggered', secret_name: name });

  // Run rotation in background
  performAutoRotation({
    secretName: name,
    store,
    chatId: chatId(),
    requestId: 'manual',
  }).then(() => {
    // rotation logs its own audit entries
  });

  res.json({ triggered: true, secret_name: name });
});

// Lockdown
app.post('/api/lockdown', localhostOnly, (_req, res) => {
  state.lockdown = true;
  saveState(state);
  logAudit({ event: 'lockdown_enabled' });
  res.json({ lockdown: true });
});

// Unlock (requires WebAuthn)
app.post('/api/unlock', async (req, res) => {
  try {
    const { authResponse } = req.body;
    if (!authResponse) return res.status(400).json({ error: 'Missing authResponse' });
    await webauthn.verifyAuthentication(authResponse);
    state.lockdown = false;
    saveState(state);
    logAudit({ event: 'lockdown_disabled' });
    res.json({ lockdown: false });
  } catch (err) {
    res.status(401).json({ error: err.message });
  }
});

// Status
app.get('/api/status', localhostOnly, (_req, res) => {
  res.json({
    lockdown: state.lockdown,
    pendingRequests: pendingRequests.size,
    standingApprovals: [...standingApprovals.keys()],
    sessionApprovals: [...sessionApprovals.entries()].map(([name, a]) => ({
      name,
      expiresAt: new Date(a.expiresAt).toISOString(),
    })),
    hasRegisteredCredentials: webauthn.hasRegisteredCredentials(),
  });
});

// ── Public request info (for approval page, no secret values) ──────────────
app.get('/api/request-info/:requestId', (req, res) => {
  const entry = pendingRequests.get(req.params.requestId);
  if (!entry) return res.status(404).json({ error: 'Request not found or expired' });
  res.json({
    request_id: req.params.requestId,
    secret_name: entry.secretName,
    status: entry.status,
    tier: entry.tier,
    created_at: new Date(entry.createdAt).toISOString(),
  });
});

// ── WebAuthn routes ────────────────────────────────────────────────────────

app.get('/api/webauthn/register-options', async (_req, res) => {
  try {
    const options = await webauthn.generateRegOptions();
    res.json(options);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/webauthn/register', async (req, res) => {
  try {
    const result = await webauthn.verifyRegistration(req.body);
    logAudit({ event: 'webauthn_registered' });
    res.json(result);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.get('/api/webauthn/auth-options', async (_req, res) => {
  try {
    const options = await webauthn.generateAuthOptions();
    res.json(options);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/webauthn/authenticate', async (req, res) => {
  try {
    const result = await webauthn.verifyAuthentication(req.body);
    res.json(result);
  } catch (err) {
    res.status(401).json({ error: err.message });
  }
});

// ── Approval endpoint ──────────────────────────────────────────────────────

app.post('/api/approve/:requestId', async (req, res) => {
  const entry = pendingRequests.get(req.params.requestId);
  if (!entry) return res.status(404).json({ error: 'Request not found or expired' });
  if (entry.status !== 'pending') return res.status(400).json({ error: `Request already ${entry.status}` });

  try {
    const { authResponse } = req.body;
    if (!authResponse) return res.status(400).json({ error: 'Missing authResponse' });
    await webauthn.verifyAuthentication(authResponse);
  } catch (err) {
    return res.status(401).json({ error: 'WebAuthn verification failed: ' + err.message });
  }

  const secret = store.get(entry.secretName);
  if (!secret) {
    entry.status = 'error';
    return res.status(500).json({ error: 'Secret no longer exists' });
  }

  const now = Date.now();
  entry.status = 'approved';
  entry.approvedAt = new Date().toISOString();
  entry.secret = secret.value;
  entry.expiresAt = new Date(now + config.secretTTL * 1000).toISOString();

  // Set up tiered approval caching
  const tier = entry.tier;
  if (tier === 'standing') {
    standingApprovals.set(entry.secretName, { approvedAt: now });
  } else if (tier === 'session') {
    const meta = store.getMeta(entry.secretName);
    const sessionTTL = (meta.ttl || 3600) * 1000;
    const expiresAt = now + sessionTTL;
    sessionApprovals.set(entry.secretName, { approvedAt: now, expiresAt });

    // Schedule rotation for when session expires
    scheduleRotation({
      secretName: entry.secretName,
      store,
      chatId: chatId(),
      requestId: req.params.requestId,
      tier,
      sessionExpiresAt: expiresAt,
    });
  }

  logAudit({
    event: 'request_approved',
    request_id: req.params.requestId,
    secret_name: entry.secretName,
    tier,
    rotation: secret.rotation,
    ip: req.ip,
  });

  // Auto-expire the delivered secret for one-time tier
  if (tier === 'one-time') {
    setTimeout(() => {
      const e = pendingRequests.get(req.params.requestId);
      if (e && e.status === 'approved') {
        e.status = 'expired';
        e.secret = undefined;
        e.expiredAt = new Date().toISOString();
        logAudit({
          event: 'secret_expired',
          request_id: req.params.requestId,
          secret_name: e.secretName,
          tier,
        });
      }
    }, config.secretTTL * 1000);
  }

  res.json({ approved: true, tier });
});

// Deny endpoint
app.post('/api/deny/:requestId', (req, res) => {
  const entry = pendingRequests.get(req.params.requestId);
  if (!entry) return res.status(404).json({ error: 'Request not found' });
  if (entry.status !== 'pending') return res.status(400).json({ error: `Request already ${entry.status}` });

  entry.status = 'denied';
  entry.deniedAt = new Date().toISOString();

  logAudit({
    event: 'request_denied',
    request_id: req.params.requestId,
    secret_name: entry.secretName,
    tier: entry.tier,
    ip: req.ip,
  });

  res.json({ denied: true });
});

// ── Approval page route ────────────────────────────────────────────────────
app.get('/approve/:requestId', (_req, res) => {
  res.sendFile(join(__dirname, 'public', 'approve.html'));
});

// ── Start server ───────────────────────────────────────────────────────────
app.listen(config.port, config.bindHost, () => {
  console.log(`🔐 Secrets Proxy running on ${config.bindHost}:${config.port}`);
  console.log(`   Lockdown: ${state.lockdown ? 'ON' : 'off'}`);
  console.log(`   WebAuthn RP: ${config.rpID} (${config.rpName})`);
  console.log(`   Credentials registered: ${webauthn.hasRegisteredCredentials()}`);
});
