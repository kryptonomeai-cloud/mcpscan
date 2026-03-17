import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse,
} from '@simplewebauthn/server';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';

const DATA_DIR = new URL('../data/', import.meta.url).pathname;
const CREDENTIALS_FILE = DATA_DIR + 'webauthn-credentials.json';

function ensureDataDir() {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
}

function loadCredentials() {
  if (!existsSync(CREDENTIALS_FILE)) return { users: {}, challenges: {} };
  return JSON.parse(readFileSync(CREDENTIALS_FILE, 'utf8'));
}

function saveCredentials(data) {
  ensureDataDir();
  writeFileSync(CREDENTIALS_FILE, JSON.stringify(data, null, 2), 'utf8');
}

export class WebAuthnManager {
  #rpID;
  #rpName;
  #origin;

  constructor({ rpID, rpName, origin }) {
    this.#rpID = rpID;
    this.#rpName = rpName;
    this.#origin = origin;
  }

  hasRegisteredCredentials() {
    const data = loadCredentials();
    const user = data.users?.['admin'];
    return !!(user && user.credentials && user.credentials.length > 0);
  }

  async generateRegOptions() {
    const data = loadCredentials();
    const userId = 'admin';
    const user = data.users?.[userId] || { id: userId, credentials: [] };

    const options = await generateRegistrationOptions({
      rpName: this.#rpName,
      rpID: this.#rpID,
      userName: 'admin',
      userDisplayName: 'Secrets Proxy Admin',
      attestationType: 'none',
      authenticatorSelection: {
        residentKey: 'preferred',
        userVerification: 'required',
      },
      excludeCredentials: user.credentials.map((c) => ({
        id: c.id,
        transports: c.transports,
      })),
    });

    // Store challenge for verification
    data.challenges = data.challenges || {};
    data.challenges[userId] = options.challenge;
    if (!data.users) data.users = {};
    data.users[userId] = user;
    saveCredentials(data);

    return options;
  }

  async verifyRegistration(response) {
    const data = loadCredentials();
    const userId = 'admin';
    const expectedChallenge = data.challenges?.[userId];

    if (!expectedChallenge) {
      throw new Error('No registration challenge found');
    }

    const verification = await verifyRegistrationResponse({
      response,
      expectedChallenge,
      expectedOrigin: this.#origin,
      expectedRPID: this.#rpID,
    });

    if (!verification.verified || !verification.registrationInfo) {
      throw new Error('Registration verification failed');
    }

    const { credential } = verification.registrationInfo;
    const newCred = {
      id: credential.id,
      publicKey: Buffer.from(credential.publicKey).toString('base64'),
      counter: credential.counter,
      transports: response.response.transports || [],
    };

    data.users[userId].credentials.push(newCred);
    delete data.challenges[userId];
    saveCredentials(data);

    return { verified: true };
  }

  async generateAuthOptions() {
    const data = loadCredentials();
    const userId = 'admin';
    const user = data.users?.[userId];

    if (!user || !user.credentials.length) {
      throw new Error('No registered credentials. Register first.');
    }

    const options = await generateAuthenticationOptions({
      rpID: this.#rpID,
      allowCredentials: user.credentials.map((c) => ({
        id: c.id,
        transports: c.transports,
      })),
      userVerification: 'required',
    });

    data.challenges = data.challenges || {};
    data.challenges[userId] = options.challenge;
    saveCredentials(data);

    return options;
  }

  async verifyAuthentication(response) {
    const data = loadCredentials();
    const userId = 'admin';
    const expectedChallenge = data.challenges?.[userId];

    if (!expectedChallenge) {
      throw new Error('No authentication challenge found');
    }

    const user = data.users[userId];
    const credential = user.credentials.find((c) => c.id === response.id);

    if (!credential) {
      throw new Error('Credential not found');
    }

    const verification = await verifyAuthenticationResponse({
      response,
      expectedChallenge,
      expectedOrigin: this.#origin,
      expectedRPID: this.#rpID,
      credential: {
        id: credential.id,
        publicKey: Uint8Array.from(Buffer.from(credential.publicKey, 'base64')),
        counter: credential.counter,
        transports: credential.transports,
      },
    });

    if (!verification.verified) {
      throw new Error('Authentication verification failed');
    }

    // Update counter
    credential.counter = verification.authenticationInfo.newCounter;
    delete data.challenges[userId];
    saveCredentials(data);

    return { verified: true };
  }
}
