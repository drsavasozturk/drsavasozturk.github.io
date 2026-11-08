// drsavasozturk.com · hareket.js (8 Kasım 2026)
// 1) "Yeni" rozeti: eklenmesinden 30 gün sonra gizlenir (kurulum tarihine bağlı kalmaz).
// 2) Yumuşak beliriş: bölümler ve kartlar ekrana girince 8 px aşağıdan solarak gelir, kardeşler 60 ms arayla; her öğe için bir kez.
// 3) Sayaçlar: kartlardaki sayılar (.say b) ekrana girince 600 ms'de hedefe sayılır.
// Tarayıcıda "hareketi azalt" açıksa ya da IntersectionObserver yoksa 2 ve 3 hiç çalışmaz; sayfa olduğu gibi görünür.
(function () {
  var d = document, h = d.documentElement;
  var yeniler = d.querySelectorAll('.yeni[data-tarih]');
  for (var i = 0; i < yeniler.length; i++) {
    var t = Date.parse(yeniler[i].getAttribute('data-tarih'));
    if (t && (Date.now() - t) / 864e5 > 30) yeniler[i].classList.add('eski');
  }
  if (!('IntersectionObserver' in window) || !('matchMedia' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  h.classList.add('js');
  var sec = '.kahraman, .giris, main.ic > section > h2, .kart, .vid, .son li';
  var els = [].slice.call(d.querySelectorAll(sec));
  for (var j = 0; j < els.length; j++) els[j].classList.add('bel');
  var gid = 0;
  var io = new IntersectionObserver(function (ents) {
    var grup = {};
    for (var k = 0; k < ents.length; k++) {
      var en = ents[k]; if (!en.isIntersecting) continue;
      var e = en.target, p = e.parentNode, id = p.__gid || (p.__gid = ++gid);
      var n = grup[id] || 0; grup[id] = n + 1;
      e.style.transitionDelay = Math.min(n, 5) * 60 + 'ms';
      e.classList.add('gor'); io.unobserve(e); sayac(e);
    }
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
  for (var m = 0; m < els.length; m++) io.observe(els[m]);
  function sayac(e) {
    var bs = e.querySelectorAll('.say b');
    for (var q = 0; q < bs.length; q++) (function (b) {
      var s = b.textContent.trim(); if (!/^\d{1,6}$/.test(s)) return;
      var hedef = +s, t0 = null; b.textContent = '0';
      function adim(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / 600, 1), k = 1 - Math.pow(1 - p, 3);
        b.textContent = p < 1 ? String(Math.round(hedef * k)) : s;
        if (p < 1) requestAnimationFrame(adim);
      }
      requestAnimationFrame(adim);
    })(bs[q]);
  }
})();
