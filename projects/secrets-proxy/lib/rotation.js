import { randomBytes } from 'node:crypto';
import { exec } from 'node:child_process';
import { logAudit } from './audit.js';
import { sendRotationNotification, sendRotationFailedNotification } from './telegram.js';

/**
 * Generate a crypto-random password, 24 chars, base64url encoded.
 */
function generatePassword() {
  return randomBytes(18).toString('base64url'); // 18 bytes → 24 base64url chars
}

/**
 * Run a rotation command, substituting placeholders.
 * Returns { success, error? }
 */
function runRotateCmd(cmd, oldPassword, newPassword) {
  const expanded = cmd
    .replaceAll('{NEW_PASSWORD}', newPassword)
    .replaceAll('{OLD_PASSWORD}', oldPassword);

  return new Promise((resolve) => {
    exec(expanded, { timeout: 30_000 }, (err, stdout, stderr) => {
      if (err) {
        resolve({ success: false, error: err.message, stderr });
      } else {
        resolve({ success: true, stdout });
      }
    });
  });
}

/**
 * Perform auto-rotation for a secret.
 * @param {object} opts
 * @param {string} opts.secretName
 * @param {object} opts.store - SecretsStore instance
 * @param {string} opts.chatId - Telegram chat ID
 * @param {string} opts.requestId - For audit trail
 */
export async function performAutoRotation({ secretName, store, chatId, requestId }) {
  const entry = store.get(secretName);
  if (!entry) {
    logAudit({ event: 'rotation_skipped', secret_name: secretName, reason: 'secret_not_found' });
    return;
  }

  if (entry.rotation !== 'auto' || !entry.rotateCmd) {
    logAudit({ event: 'rotation_skipped', secret_name: secretName, reason: 'no_rotate_cmd' });
    return;
  }

  const oldPassword = entry.value;
  const newPassword = generatePassword();

  logAudit({
    event: 'rotation_started',
    secret_name: secretName,
    request_id: requestId,
  });

  const result = await runRotateCmd(entry.rotateCmd, oldPassword, newPassword);

  if (result.success) {
    // Update the store with the new password
    store.add(secretName, newPassword, {
      tier: entry.tier,
      ttl: entry.ttl,
      rotation: entry.rotation,
      rotateCmd: entry.rotateCmd,
    });
    store.setLastRotated(secretName, new Date().toISOString());

    logAudit({
      event: 'rotation_completed',
      secret_name: secretName,
      request_id: requestId,
    });
  } else {
    // Rotation failed — DON'T change the password, alert via Telegram
    logAudit({
      event: 'rotation_failed',
      secret_name: secretName,
      request_id: requestId,
      error: result.error,
    });

    await sendRotationFailedNotification({
      secretName,
      error: result.error,
      chatId,
    }).catch(() => {});
  }
}

/**
 * Send a notify-rotate Telegram message.
 */
export async function performNotifyRotation({ secretName, chatId, requestId }) {
  logAudit({
    event: 'rotation_notify_sent',
    secret_name: secretName,
    request_id: requestId,
  });

  await sendRotationNotification({ secretName, chatId }).catch(() => {});
}

/**
 * Schedule rotation based on tier and rotation mode.
 * - one-time: rotate immediately after poll
 * - session: rotate after session TTL expires
 * - standing + auto: treated as notify (warned at CLI time)
 */
export function scheduleRotation({ secretName, store, chatId, requestId, tier, sessionExpiresAt }) {
  const entry = store.get(secretName);
  if (!entry || !entry.rotation || entry.rotation === 'none') return;

  const rotation = entry.rotation;

  if (rotation === 'notify') {
    // Always fire immediately for notify
    performNotifyRotation({ secretName, chatId, requestId });
    return;
  }

  if (rotation === 'auto') {
    if (tier === 'standing') {
      // standing + auto → treat as notify (safety fallback)
      performNotifyRotation({ secretName, chatId, requestId });
      return;
    }

    if (tier === 'one-time') {
      // Rotate immediately
      performAutoRotation({ secretName, store, chatId, requestId });
    } else if (tier === 'session') {
      // Rotate after session TTL expires
      const delay = sessionExpiresAt ? sessionExpiresAt - Date.now() : 0;
      if (delay > 0) {
        setTimeout(() => {
          performAutoRotation({ secretName, store, chatId, requestId });
        }, delay);
        logAudit({
          event: 'rotation_scheduled',
          secret_name: secretName,
          request_id: requestId,
          rotate_at: new Date(sessionExpiresAt).toISOString(),
        });
      } else {
        performAutoRotation({ secretName, store, chatId, requestId });
      }
    }
  }
}
