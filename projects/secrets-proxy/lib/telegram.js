import { execSync } from 'node:child_process';

let cachedToken = null;

function getBotToken() {
  if (cachedToken) return cachedToken;

  if (process.env.TELEGRAM_BOT_TOKEN) {
    cachedToken = process.env.TELEGRAM_BOT_TOKEN;
    return cachedToken;
  }

  try {
    cachedToken = execSync(
      'security find-generic-password -s "secrets-proxy-telegram-token" -a "bot-token" -w 2>/dev/null',
      { encoding: 'utf8' }
    ).trim();
    if (cachedToken) return cachedToken;
  } catch {
    // Not found
  }

  console.warn('⚠️  No Telegram bot token configured. Notifications disabled.');
  return null;
}

async function sendTelegram({ chatId, text, replyMarkup }) {
  const token = getBotToken();
  if (!token) {
    console.warn('Telegram notification skipped — no bot token');
    return;
  }

  const body = {
    chat_id: chatId,
    text,
    parse_mode: 'Markdown',
  };
  if (replyMarkup) body.reply_markup = replyMarkup;

  try {
    const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.text();
      console.error('Telegram API error:', err);
    }
  } catch (err) {
    console.error('Telegram send failed:', err.message);
  }
}

export async function sendApprovalNotification({ secretName, requestId, approveUrl, chatId }) {
  const timestamp = new Date().toLocaleString('en-GB', {
    timeZone: 'Europe/London',
    dateStyle: 'medium',
    timeStyle: 'short',
  });

  await sendTelegram({
    chatId,
    text: `🔐 *Secret requested:* \`${secretName}\`\n📅 *Requested at:* ${timestamp}`,
    replyMarkup: {
      inline_keyboard: [[{ text: 'Approve →', url: approveUrl }]],
    },
  });
}

export async function sendRotationNotification({ secretName, chatId }) {
  await sendTelegram({
    chatId,
    text: `⚠️ Secret \`${secretName}\` was used. Consider rotating it.`,
  });
}

export async function sendRotationFailedNotification({ secretName, error, chatId }) {
  await sendTelegram({
    chatId,
    text: `🚨 *Auto-rotation FAILED* for \`${secretName}\`\n\nOld password still active. Please rotate manually.\n\nError: \`${error}\``,
  });
}
