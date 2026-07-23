const CACHE_NAME = 'famo-omnisphere-v1';

// Full manifest matching your repository layout branch
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './logomatrix.html',
  './jurkzillon.html',
  './runner.html',
  './switchboard.html',
  './omnisphere-arcade-matrix.html',
  './omnisphere-the-34.html',
  './Ecosystem_DNA.md'
];

// 1. INSTALLATION: Pre-cache the main app ecosystem matrix
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Ghost-Protocol] Core network assets locked.');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// 2. ACTIVATION: Clean out legacy network versions instantly 
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. INTERCEPTION: Run blazing fast offline cache fallback logic
self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, response.clone());
            return response;
          });
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
