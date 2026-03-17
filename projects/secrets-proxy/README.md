# Secrets Proxy 🔐

A WebAuthn-based secrets proxy that lets an AI agent request credentials with human biometric approval.

## How It Works

1. Agent requests a secret by name via localhost API
2. You get a Telegram notification with an approval link
3. Open the link → authenticate with Face ID / fingerprint / security key
4. Secret is released to the agent with a 60-second TTL
5. (Optional) Secret auto-rotates after use so the old password is immediately invalid

## Setup

```bash
cd projects/secrets-proxy
npm install
```

### Register a WebAuthn credential
Start the server, then open `http://localhost:18900/register.html` on a device with biometrics.

### Configure Telegram (optional)
Store your bot token in macOS Keychain:
```bash
security add-generic-password -s "secrets-proxy-telegram-token" -a "bot-token" -w "YOUR_BOT_TOKEN" -U
```
Or set `TELEGRAM_BOT_TOKEN` env var.

### Add secrets
```bash
# One-time (default) — needs approval every time
node cli.js add "NAS sudo" "password123"

# With auto-rotation — generates new password after each use
node cli.js add "NAS sudo" "password123" --tier one-time --rotation auto \
  --rotate-cmd "ssh nas \"echo 'user:{NEW_PASSWORD}' | sudo chpasswd\""

# Session — approved once, available for 1 hour
node cli.js add "Docker token" "abc..." --tier session --ttl 3600

# Standing — approved once, available until revoked
node cli.js add "SearXNG key" "xyz..." --tier standing

# With notify-on-use rotation
node cli.js add "Paperless token" "abc..." --tier session --rotation notify
```

### Start the server
```bash
npm start
```

## Access Tiers

| Tier | Behavior | Re-approval |
|------|----------|-------------|
| `one-time` | Single use per approval, 60s TTL | Every time |
| `session` | Available for configurable TTL (default 1h) | After TTL expires |
| `standing` | Available until explicitly revoked | Never (until revoked) |

## Rotation Modes

| Mode | Behavior |
|------|----------|
| `auto` | Generates new password + runs rotation command after use |
| `notify` | Sends Telegram alert suggesting manual rotation |
| `none` | No rotation (default) |

## Agent API (localhost only, port 18900)

### Request a secret
```bash
curl -X POST http://127.0.0.1:18900/api/request \
  -H 'Content-Type: application/json' \
  -d '{"name": "NAS sudo"}'
# → {"request_id": "...", "status": "pending", "tier": "one-time"}
# For standing/session with cached approval:
# → {"request_id": "...", "status": "approved", "secret": "...", "tier": "standing"}
```

### Poll for result
```bash
curl http://127.0.0.1:18900/api/poll/REQUEST_ID
# → {"status": "approved", "secret": "thepassword", ...}
```

### Revoke approval
```bash
curl -X POST http://127.0.0.1:18900/api/revoke/SearXNG%20key
```

### Manual rotation
```bash
curl -X POST http://127.0.0.1:18900/api/rotate/NAS%20sudo
```

### Lockdown
```bash
curl -X POST http://127.0.0.1:18900/api/lockdown   # block all requests
curl -X POST http://127.0.0.1:18900/api/unlock      # requires WebAuthn
```

## CLI

```bash
node cli.js add <name> <value> [--tier ...] [--ttl N] [--rotation ...] [--rotate-cmd "..."]
node cli.js list
node cli.js remove <name>
node cli.js revoke <name>     # revoke cached approval (server must be running)
node cli.js rotate <name>     # trigger manual rotation (server must be running)
```

## Security

- Internal API bound to localhost only
- Secrets encrypted with AES-256-GCM, master key in macOS Keychain
- Secrets never logged or included in error messages
- Request IDs are crypto-random UUIDs
- Pending requests expire after 5 minutes
- Approved one-time secrets expire after 60 seconds, single poll only
- Auto-rotation invalidates used passwords immediately
- Full audit log at `data/audit.jsonl`

## Config

Edit `config.json`:
```json
{
  "port": 18900,
  "rpID": "localhost",
  "rpName": "Secrets Proxy",
  "origin": "http://localhost:18900",
  "telegramChatId": "8387589944",
  "requestTTL": 300,
  "secretTTL": 60,
  "bindHost": "0.0.0.0"
}
```

For remote access (e.g., via Tailscale), update `rpID` and `origin` to match your hostname.
