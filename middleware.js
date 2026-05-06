// Vercel Edge Middleware — branded password gate.
//
// Flow:
//   1. User visits any URL.
//   2. If they have a valid session cookie, request passes through.
//   3. Otherwise the middleware returns a branded login page (HTML).
//   4. Submitting the form POSTs to /__auth, which checks the password
//      against SITE_PASSWORD, sets a session cookie, and redirects back
//      to the original URL.
//
// The cookie value is SHA-256(SITE_PASSWORD). Rotating SITE_PASSWORD
// in Vercel invalidates every existing session automatically — no
// extra session-store needed.
//
// SITE_PASSWORD is read from the Vercel project's Environment Variables.
// While SITE_PASSWORD is unset, the middleware passes through (so you
// can't accidentally lock the site out during initial setup).
//
// /assets/images/* and /robots.txt are excluded from the gate so
// favicons and link-preview images stay public for unauthenticated
// crawlers / iMessage / Slack.

export const config = {
  matcher: [
    '/((?!_next|_vercel|assets/images/|robots\\.txt).*)',
  ],
};

const COOKIE_NAME = 'gg26_staff_auth';
const COOKIE_MAX_AGE = 60 * 60 * 24 * 7; // 7 days
const AUTH_PATH = '/__auth';

export default async function middleware(request) {
  const expected = process.env.SITE_PASSWORD || '';

  // Open mode while no password configured — set SITE_PASSWORD in
  // Vercel to enforce.
  if (!expected) return;

  const url = new URL(request.url);
  const expectedHash = await sha256(expected);

  // Handle the login form submission
  if (url.pathname === AUTH_PATH && request.method === 'POST') {
    let supplied = '';
    let next = '/';
    try {
      const form = await request.formData();
      supplied = String(form.get('password') || '');
      next = String(form.get('next') || '/');
    } catch {
      return loginPage('/', { error: 'Could not read form. Try again.' });
    }
    if (!safeRedirect(next)) next = '/';

    if (!timingSafeEqual(supplied, expected)) {
      return loginPage(next, { error: 'Wrong password. Try again.' });
    }

    // Authenticated — set cookie + redirect
    return new Response(null, {
      status: 302,
      headers: {
        'Location': next,
        'Set-Cookie': cookieString(COOKIE_NAME, expectedHash, COOKIE_MAX_AGE),
        'Cache-Control': 'no-store',
      },
    });
  }

  // Check session cookie
  const cookieValue = readCookie(request.headers.get('cookie') || '', COOKIE_NAME);
  if (cookieValue && timingSafeEqual(cookieValue, expectedHash)) {
    return; // Authenticated — fall through
  }

  // Not authenticated — render the login form. Capture the original
  // URL so the form can redirect them back after login.
  const next = url.pathname + url.search;
  return loginPage(next, {});
}

// ---- helpers ----

function loginPage(next, opts) {
  const error = opts && opts.error ? opts.error : '';
  const safeNext = safeRedirect(next) ? next : '/';
  const html = renderHTML(safeNext, error);
  return new Response(html, {
    status: error ? 401 : 200,
    headers: {
      'Content-Type': 'text/html; charset=UTF-8',
      'Cache-Control': 'no-store',
    },
  });
}

function renderHTML(next, error) {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<meta name="theme-color" content="#050505">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" href="/assets/images/gold-house-ico.png">
<link rel="apple-touch-icon" href="/assets/images/gold-house-ico.png">
<title>Sign in · GG26 Staff Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050505;
    --bg-elev: #181818;
    --text: #f4ede0;
    --text-dim: #a8a094;
    --gold: #c89c3f;
    --gold-bright: #e8b94a;
    --gold-soft: rgba(200, 156, 63, 0.12);
    --border: #2a2a2a;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; min-height: 100vh; background: var(--bg); color: var(--text); font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; }
  body {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background:
      radial-gradient(ellipse 60% 40% at 50% 30%, rgba(200, 156, 63, 0.10), transparent 70%),
      var(--bg);
  }
  .card {
    width: 100%;
    max-width: 380px;
    padding: 32px 28px;
    text-align: center;
    background: var(--bg-elev);
    border: 1px solid var(--border);
    border-radius: 16px;
  }
  .logo { display: block; margin: 0 auto 22px; height: 30px; width: auto; }
  h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin: 0 0 8px;
    color: var(--text);
  }
  .sub {
    color: var(--text-dim);
    font-size: 13px;
    letter-spacing: 0.01em;
    margin: 0 0 24px;
    line-height: 1.5;
  }
  form { display: flex; flex-direction: column; gap: 12px; }
  input[type=password] {
    width: 100%;
    padding: 12px 14px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-family: inherit;
    font-size: 15px;
    letter-spacing: 0.02em;
    outline: none;
    transition: border-color 0.15s;
  }
  input[type=password]:focus { border-color: var(--gold); }
  input[type=password]::placeholder { color: var(--text-dim); opacity: 0.6; }
  button {
    width: 100%;
    padding: 12px 14px;
    background: var(--gold);
    color: #0b0a07;
    border: none;
    border-radius: 10px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    cursor: pointer;
    transition: background 0.15s;
  }
  button:hover, button:focus { background: var(--gold-bright); }
  button:active { transform: scale(0.98); }
  .error {
    margin: 0 0 12px;
    padding: 8px 12px;
    background: rgba(232, 80, 80, 0.10);
    border: 1px solid rgba(232, 80, 80, 0.40);
    border-radius: 8px;
    color: #ffb3b3;
    font-size: 13px;
  }
  .footer {
    margin-top: 22px;
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.04em;
  }
</style>
</head>
<body>
  <main class="card">
    <img src="/assets/images/gold-house-ico.png" alt="Gold House" class="logo">
    <h1>Staff Access</h1>
    <p class="sub">Enter the password shared with your team to continue.</p>
    ${error ? `<p class="error">${esc(error)}</p>` : ''}
    <form method="POST" action="${esc(AUTH_PATH)}" autocomplete="on">
      <input type="hidden" name="next" value="${esc(next)}">
      <input
        type="password"
        name="password"
        placeholder="Password"
        autofocus
        required
        autocomplete="current-password"
      >
      <button type="submit">Sign in</button>
    </form>
    <div class="footer">Gold Gala · May 9, 2026</div>
  </main>
</body>
</html>`;
}

function cookieString(name, value, maxAge) {
  return [
    `${name}=${value}`,
    'HttpOnly',
    'Secure',
    'SameSite=Strict',
    'Path=/',
    `Max-Age=${maxAge}`,
  ].join('; ');
}

function readCookie(header, name) {
  const m = header.match(new RegExp(`(?:^|;\\s*)${name}=([^;]+)`));
  return m ? m[1] : null;
}

// Only allow same-origin redirects (prevent open-redirect abuse)
function safeRedirect(next) {
  if (typeof next !== 'string') return false;
  if (!next.startsWith('/')) return false;
  if (next.startsWith('//')) return false;
  return true;
}

async function sha256(s) {
  const data = new TextEncoder().encode(s);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) {
    r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return r === 0;
}
