/* EduNode Service Worker — offline shell caching */
const CACHE = 'edunode-v1';
const SHELL = [
  '/',
  '/chat',
  '/quiz',
  '/flashcard',
  '/podcast',
  '/progress',
  '/static/css/style.css',
  '/static/icons/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
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
  // Only cache GET requests for same origin
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  // Network-first for API calls
  if (url.pathname.startsWith('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() =>
        caches.match(e.request).then(r => r || new Response('{"error":"offline"}', {
          headers: {'Content-Type': 'application/json'}
        }))
      )
    );
    return;
  }

  // Cache-first for shell + static assets
  e.respondWith(
    caches.match(e.request).then(cached => {
      const fresh = fetch(e.request).then(res => {
        if (res && res.status === 200) {
          caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        }
        return res;
      });
      return cached || fresh;
    })
  );
});
