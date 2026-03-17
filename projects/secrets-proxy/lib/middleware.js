const LOCALHOST_ADDRS = new Set(['127.0.0.1', '::1', '::ffff:127.0.0.1']);

export function localhostOnly(req, res, next) {
  const ip = req.ip || req.connection?.remoteAddress;
  if (LOCALHOST_ADDRS.has(ip)) {
    return next();
  }
  res.status(403).json({ error: 'Forbidden — localhost only' });
}
