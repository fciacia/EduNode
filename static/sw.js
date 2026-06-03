/* Edge Service Worker — installable offline app shell */
const CACHE = 'edge-v1';

/* Precache the whole shell so every page works offline after the first install,
   not just pages the student has already visited. Same-origin only (cross-origin
   fonts fall back to system fonts when offline). */
const SHELL = [
  '/', '/chat', '/quiz', '/flashcard', '/podcast', '/progress',
  '/static/css/style.css',
  '/static/icons/sprite.svg',
  '/static/icons/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/js/i18n.js',
  '/static/js/onboarding.js',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      // allSettled so one failed page can't abort the whole install
      .then(c => Promise.allSettled(SHELL.map(u => c.add(new Request(u, { cache: 'reload' })))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  // Network-first for API calls, with an offline JSON fallback.
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() =>
        caches.match(e.request).then(r => r || new Response('{"error":"offline"}', {
          headers: { 'Content-Type': 'application/json' }
        }))
      )
    );
    return;
  }

  const isStatic = /\.(png|jpg|jpeg|gif|ico|woff2?|svg)$/i.test(url.pathname);

  // Network-first for HTML pages and JS/CSS — always fresh when online, cached
  // when offline; falls back to the home shell for never-visited pages.
  if (!isStatic) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() =>
        caches.match(e.request).then(r => r || caches.match('/'))
      )
    );
    return;
  }

  // Cache-first for images / icons / fonts.
  e.respondWith(
    caches.match(e.request).then(cached => cached ||
      fetch(e.request).then(res => {
        if (res && res.status === 200) {
          caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        }
        return res;
      })
    )
  );
});
