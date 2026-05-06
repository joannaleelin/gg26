// Vercel Edge Middleware — HTTP Basic Auth for the entire site.
//
// Set SITE_PASSWORD in your Vercel project's Environment Variables to
// require a password on every request. While SITE_PASSWORD is unset
// (e.g. during initial setup), the middleware passes through so the
// site stays accessible.
//
// Username is ignored — anyone with the password gets in. Browser
// stores credentials for the session, so users only see the login
// dialog once until they close the browser.
//
// /assets/images/* stays public so favicons and og:image link-previews
// (iMessage, Slack, etc.) work for unauthenticated viewers.

export const config = {
  matcher: [
    '/((?!_next|_vercel|assets/images/).*)',
  ],
};

const REALM = 'GG26 Staff Hub';

export default function middleware(request) {
  const expected = process.env.SITE_PASSWORD || '';

  // Gate is open while no password is configured — set SITE_PASSWORD
  // in Vercel to enforce. This avoids accidentally locking the site
  // out if the env var ever gets cleared.
  if (!expected) return;

  const auth = request.headers.get('authorization') || '';
  if (!auth.startsWith('Basic ')) return unauthorized();

  let decoded = '';
  try {
    decoded = atob(auth.slice(6));
  } catch {
    return unauthorized();
  }

  const colon = decoded.indexOf(':');
  if (colon < 0) return unauthorized();

  // Username is ignored; only the password matters
  const supplied = decoded.slice(colon + 1);
  if (!timingSafeEqual(supplied, expected)) return unauthorized();

  // Authenticated — fall through to serve the requested file
  return;
}

function unauthorized() {
  return new Response('Authentication required.\n', {
    status: 401,
    headers: {
      'WWW-Authenticate': `Basic realm="${REALM}", charset="UTF-8"`,
      'Content-Type': 'text/plain; charset=UTF-8',
      'Cache-Control': 'no-store',
    },
  });
}

// Constant-time string comparison so an attacker can't deduce the
// password by measuring how long the comparison takes
function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) {
    r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return r === 0;
}
