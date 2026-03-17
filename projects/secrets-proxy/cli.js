import { SecretsStore } from './lib/secrets-store.js';

const args = process.argv.slice(2);
const command = args[0];

const store = new SecretsStore();

function usage() {
  console.log(`Usage:
  node cli.js add <name> <value> [--tier one-time|session|standing] [--ttl <seconds>]
                                 [--rotation auto|notify|none] [--rotate-cmd <command>]
  node cli.js remove <name>
  node cli.js list
  node cli.js revoke <name>         (revokes standing/session approval via API)
  node cli.js rotate <name>         (manually trigger rotation via API)
  `);
  process.exit(1);
}

function parseFlags(flagArgs) {
  const flags = {};
  for (let i = 0; i < flagArgs.length; i++) {
    if (flagArgs[i] === '--tier' && flagArgs[i + 1]) {
      flags.tier = flagArgs[++i];
    } else if (flagArgs[i] === '--ttl' && flagArgs[i + 1]) {
      flags.ttl = parseInt(flagArgs[++i], 10);
    } else if (flagArgs[i] === '--rotation' && flagArgs[i + 1]) {
      flags.rotation = flagArgs[++i];
    } else if (flagArgs[i] === '--rotate-cmd' && flagArgs[i + 1]) {
      flags.rotateCmd = flagArgs[++i];
    }
  }
  return flags;
}

switch (command) {
  case 'add': {
    const name = args[1];
    const value = args[2];
    if (!name || !value) {
      console.error('Error: name and value are required');
      usage();
    }
    const flags = parseFlags(args.slice(3));
    const tier = flags.tier || 'one-time';
    let rotation = flags.rotation || 'none';

    // Warn about standing + auto-rotate
    if (tier === 'standing' && rotation === 'auto') {
      console.warn('⚠️  Warning: standing + auto-rotate is not supported (secret is always available).');
      console.warn('   Treating as "notify" rotation instead.');
      rotation = 'notify';
    }

    // Warn if auto rotation without a command
    if (rotation === 'auto' && !flags.rotateCmd) {
      console.warn('⚠️  Warning: auto rotation set but no --rotate-cmd provided.');
      console.warn('   Rotation will fail until a rotate command is configured.');
    }

    try {
      store.add(name, value, {
        tier,
        ttl: flags.ttl,
        rotation,
        rotateCmd: flags.rotateCmd,
      });
      const ttlNote = tier === 'session' ? ` (TTL: ${flags.ttl || 3600}s)` : '';
      const rotNote = rotation !== 'none' ? ` [rotation: ${rotation}]` : '';
      console.log(`✅ Secret "${name}" added [tier: ${tier}${ttlNote}]${rotNote}`);
    } catch (err) {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
    break;
  }

  case 'remove': {
    const name = args[1];
    if (!name) { console.error('Error: name is required'); usage(); }
    if (store.remove(name)) {
      console.log(`✅ Secret "${name}" removed`);
    } else {
      console.error(`Secret "${name}" not found`);
      process.exit(1);
    }
    break;
  }

  case 'list': {
    const secrets = store.list();
    if (secrets.length === 0) {
      console.log('No secrets stored.');
    } else {
      console.log('Stored secrets:');
      for (const s of secrets) {
        const ttlNote = s.tier === 'session' ? ` (TTL: ${s.ttl || 3600}s)` : '';
        const rotNote = s.rotation !== 'none' ? ` [rotation: ${s.rotation}${s.hasRotateCmd ? ', cmd ✓' : ''}]` : '';
        const lastRot = s.lastRotated ? ` (last rotated: ${s.lastRotated})` : '';
        console.log(`  • ${s.name} [${s.tier}${ttlNote}]${rotNote}${lastRot}`);
      }
    }
    break;
  }

  case 'revoke': {
    const name = args[1];
    if (!name) { console.error('Error: name is required'); usage(); }
    try {
      const res = await fetch(`http://127.0.0.1:18900/api/revoke/${encodeURIComponent(name)}`, {
        method: 'POST',
      });
      const data = await res.json();
      if (data.revoked) {
        console.log(`✅ Approval for "${name}" revoked`);
      } else {
        console.log(`No active approval found for "${name}"`);
      }
    } catch {
      console.error('Error: Could not connect to secrets-proxy server. Is it running?');
      process.exit(1);
    }
    break;
  }

  case 'rotate': {
    const name = args[1];
    if (!name) { console.error('Error: name is required'); usage(); }
    try {
      const res = await fetch(`http://127.0.0.1:18900/api/rotate/${encodeURIComponent(name)}`, {
        method: 'POST',
      });
      const data = await res.json();
      if (res.ok && data.triggered) {
        console.log(`✅ Rotation triggered for "${name}"`);
      } else {
        console.error(`Error: ${data.error}`);
        process.exit(1);
      }
    } catch {
      console.error('Error: Could not connect to secrets-proxy server. Is it running?');
      process.exit(1);
    }
    break;
  }

  default:
    usage();
}
