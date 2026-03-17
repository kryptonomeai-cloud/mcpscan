import { createCipheriv, createDecipheriv, randomBytes, scryptSync } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';

const DATA_DIR = new URL('../data/', import.meta.url).pathname;
const SECRETS_FILE = DATA_DIR + 'secrets.enc';
const KEYCHAIN_SERVICE = 'secrets-proxy';
const KEYCHAIN_ACCOUNT = 'master-passphrase';
const VALID_TIERS = ['one-time', 'session', 'standing'];
const VALID_ROTATIONS = ['auto', 'notify', 'none'];

function ensureDataDir() {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
}

function getPassphrase() {
  try {
    const result = execSync(
      `security find-generic-password -s "${KEYCHAIN_SERVICE}" -a "${KEYCHAIN_ACCOUNT}" -w 2>/dev/null`,
      { encoding: 'utf8' }
    ).trim();
    if (result) return result;
  } catch {
    // Not found — generate and store one
  }
  const passphrase = randomBytes(32).toString('hex');
  execSync(
    `security add-generic-password -s "${KEYCHAIN_SERVICE}" -a "${KEYCHAIN_ACCOUNT}" -w "${passphrase}" -U`,
    { encoding: 'utf8' }
  );
  console.log('Generated and stored master passphrase in macOS Keychain');
  return passphrase;
}

function deriveKey(passphrase) {
  return scryptSync(passphrase, 'secrets-proxy-salt-v1', 32);
}

function encrypt(data, key) {
  const iv = randomBytes(16);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(JSON.stringify(data), 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]).toString('base64');
}

function decrypt(encoded, key) {
  const buf = Buffer.from(encoded, 'base64');
  const iv = buf.subarray(0, 16);
  const tag = buf.subarray(16, 32);
  const encrypted = buf.subarray(32);
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
  return JSON.parse(decrypted.toString('utf8'));
}

export class SecretsStore {
  #key;

  constructor() {
    ensureDataDir();
    const passphrase = getPassphrase();
    this.#key = deriveKey(passphrase);
  }

  #load() {
    if (!existsSync(SECRETS_FILE)) return {};
    const encoded = readFileSync(SECRETS_FILE, 'utf8').trim();
    if (!encoded) return {};
    return decrypt(encoded, this.#key);
  }

  #save(secrets) {
    ensureDataDir();
    writeFileSync(SECRETS_FILE, encrypt(secrets, this.#key), 'utf8');
  }

  /**
   * Add or update a secret.
   * @param {string} name
   * @param {string} value
   * @param {object} opts - { tier, ttl, rotation, rotateCmd }
   */
  add(name, value, opts = {}) {
    const tier = opts.tier || 'one-time';
    if (!VALID_TIERS.includes(tier)) {
      throw new Error(`Invalid tier "${tier}". Must be one of: ${VALID_TIERS.join(', ')}`);
    }
    const rotation = opts.rotation || 'none';
    if (!VALID_ROTATIONS.includes(rotation)) {
      throw new Error(`Invalid rotation "${rotation}". Must be one of: ${VALID_ROTATIONS.join(', ')}`);
    }

    const secrets = this.#load();

    // Preserve lastRotated if updating an existing secret
    const existing = secrets[name];
    const entry = { value, tier, rotation };

    if (tier === 'session') {
      entry.ttl = opts.ttl || 3600;
    }
    if (rotation === 'auto' && opts.rotateCmd) {
      entry.rotateCmd = opts.rotateCmd;
    }
    if (existing?.lastRotated) {
      entry.lastRotated = existing.lastRotated;
    }

    secrets[name] = entry;
    this.#save(secrets);
  }

  remove(name) {
    const secrets = this.#load();
    if (!(name in secrets)) return false;
    delete secrets[name];
    this.#save(secrets);
    return true;
  }

  list() {
    const secrets = this.#load();
    return Object.entries(secrets).map(([name, entry]) => ({
      name,
      tier: entry.tier || 'one-time',
      ttl: entry.ttl,
      rotation: entry.rotation || 'none',
      hasRotateCmd: !!entry.rotateCmd,
      lastRotated: entry.lastRotated,
    }));
  }

  get(name) {
    const secrets = this.#load();
    const entry = secrets[name];
    if (!entry) return null;
    return {
      value: entry.value,
      tier: entry.tier || 'one-time',
      ttl: entry.ttl,
      rotation: entry.rotation || 'none',
      rotateCmd: entry.rotateCmd,
      lastRotated: entry.lastRotated,
    };
  }

  has(name) {
    return this.#load().hasOwnProperty(name);
  }

  getMeta(name) {
    const secrets = this.#load();
    const entry = secrets[name];
    if (!entry) return null;
    return {
      tier: entry.tier || 'one-time',
      ttl: entry.ttl,
      rotation: entry.rotation || 'none',
      hasRotateCmd: !!entry.rotateCmd,
      lastRotated: entry.lastRotated,
    };
  }

  /**
   * Update the lastRotated timestamp for a secret.
   */
  setLastRotated(name, timestamp) {
    const secrets = this.#load();
    if (!(name in secrets)) return false;
    secrets[name].lastRotated = timestamp;
    this.#save(secrets);
    return true;
  }
}
