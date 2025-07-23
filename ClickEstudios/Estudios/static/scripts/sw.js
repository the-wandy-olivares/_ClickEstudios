const CACHE_NAME = "clickestudios-cache-v2";
const urlsToCache = [
  "/",
  "/offline/",
  // "/static/css/styles.css",
  // "/static/js/app.js"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request).then(res => res || caches.match("/offline/"))
    )
  );
});