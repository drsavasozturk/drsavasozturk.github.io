// drsavasozturk.com service worker · sürüm etiketi her güncellemede değişir
const V = 'drso-2026-11-08g';
const CEK = ["./", "index.html", "ozgecmis.html", "yayinlar.html", "hasta.html", "atlaslar.html", "kunye.html", "kullanim-kosullari.html", "gizlilik.html", "surum-notlari.html", "404.html", "stil.css", "hareket.js", "foto-portre.jpg", "ikon.svg", "ikon-d.svg", "ikon-y.svg", "manifest.webmanifest", "yazi_tipleri/fonts.css", "yazi_tipleri/lora-latin-500-normal.woff2", "yazi_tipleri/lora-latin-600-normal.woff2", "yazi_tipleri/lora-latin-700-normal.woff2", "yazi_tipleri/lora-latin-ext-500-normal.woff2", "yazi_tipleri/lora-latin-ext-600-normal.woff2", "yazi_tipleri/lora-latin-ext-700-normal.woff2", "yazi_tipleri/source-sans-3-latin-400-normal.woff2", "yazi_tipleri/source-sans-3-latin-600-normal.woff2", "yazi_tipleri/source-sans-3-latin-700-normal.woff2", "yazi_tipleri/source-sans-3-latin-800-normal.woff2", "yazi_tipleri/source-sans-3-latin-ext-400-normal.woff2", "yazi_tipleri/source-sans-3-latin-ext-600-normal.woff2", "yazi_tipleri/source-sans-3-latin-ext-700-normal.woff2", "yazi_tipleri/source-sans-3-latin-ext-800-normal.woff2"];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(CEK.map(u => new Request(u, {cache: 'reload'})))).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil((async () => {
  const eski = (await caches.keys()).filter(k => k !== V);
  await Promise.all(eski.map(k => caches.delete(k)));
  await self.clients.claim();
  if (eski.length) (await self.clients.matchAll({type: 'window'})).forEach(c => c.postMessage({t: 'yeni'}));
})()); });
self.addEventListener('message', e => {
  if (e.data && e.data.t === 'sakla' && typeof e.data.u === 'string' && new URL(e.data.u).origin === location.origin)
    e.waitUntil(caches.open(V).then(c => c.match(e.data.u).then(h => h || c.add(new Request(e.data.u, {cache: 'reload'})))).catch(() => {}));
});
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET') return;
  const u = new URL(r.url); if (u.origin !== location.origin || u.pathname.includes('/indir/')) return;
  e.respondWith((async () => {
    const c = await caches.open(V);
    const hit = await c.match(r, {ignoreSearch: true}); if (hit) return hit;
    try { const res = await fetch(r); if (res.ok && res.type === 'basic') c.put(r, res.clone()); return res; }
    catch (x) { if (r.mode === 'navigate') { const h = await c.match('404.html'); if (h) return h; } throw x; }
  })());
});
