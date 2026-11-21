/* drsavasozturk.com · Nefroloji Ders Serisi · etkileşimli şekiller (PİLOT, 20 Kasım 2026; yayında değil)
   Mevcut statik SVG şekillere slayt kimliğiyle dokunma, sürükleme ve hareket ekler.
   İlk görünüm her zaman bugünkü statik şekildir; JS çalışmazsa şekil olduğu gibi kalır.
   Dokunma yalnız etkileşimli bir ögedeyse yutulur (slayt ilerlemez); kaydırma (swipe) her yerde çalışır. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var C = { mavi: '#0b6e99', kirmizi: '#c0392b', yesil: '#1f8a4c', mor: '#6a4c93', altin: '#c98a00', gri: '#6b7b8a', su: '#3d9ad1' };

  function el(tag, at, par) { var e = document.createElementNS(NS, tag); for (var k in at) e.setAttribute(k, at[k]); if (par) par.appendChild(e); return e; }
  function yazi(par, x, y, s, at) { var o = { x: x, y: y, 'font-size': 12 }; for (var k in at) o[k] = at[k]; var t = el('text', o, par); t.textContent = s; return t; }
  function metin(svg, bas) {
    var T = svg.querySelectorAll('text');
    for (var i = 0; i < T.length; i++) if (T[i].textContent.replace(/\s+/g, ' ').trim().indexOf(bas) === 0) return T[i];
    return null;
  }
  function kutu(svg, bas) {           // metni içeren en küçük dikdörtgen (etiket kutusu)
    var t = metin(svg, bas); if (!t) return null;
    var b = t.getBBox(), cx = b.x + b.width / 2, cy = b.y + b.height / 2, vb = svg.viewBox.baseVal, en = null, A = 1e12;
    [].forEach.call(svg.querySelectorAll('rect'), function (r) {
      if (r.closest('.etk-k')) return;
      var q = r.getBBox(); if (q.width >= vb.width * .97) return;
      if (cx > q.x && cx < q.x + q.width && cy > q.y && cy < q.y + q.height && q.width * q.height < A) { A = q.width * q.height; en = q; }
    });
    return en ? { x: en.x, y: en.y, w: en.width, h: en.height } : { x: b.x - 6, y: b.y - 4, w: b.width + 12, h: b.height + 8 };
  }
  function nokta(svg, e) { var p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); }
  function acik(svg) { var s = svg.closest('.slide'); return !s || s.classList.contains('on'); }
  function tr(n, d) { return n.toFixed(d).replace('.', ','); }
  function yut(e) { e.stopPropagation(); }
  function dugme(n, ad, fn) {          // dokunma, fare ve klavye (Enter / boşluk) ile seçilebilir öge
    n.setAttribute('tabindex', '0'); n.setAttribute('role', 'button'); n.setAttribute('aria-label', ad); n.style.cursor = 'pointer';
    n.addEventListener('click', function (e) { yut(e); fn(e); });
    n.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { yut(e); e.preventDefault(); fn(e); } });
  }
  function surukle(svg, alan, fn, adim) {   // fn(x, y) · adim(+1 | -1) klavye okları
    alan.style.touchAction = 'none'; alan.style.cursor = 'ew-resize'; alan.setAttribute('tabindex', '0');
    svg.style.touchAction = 'pan-y';   // SVG ögelerinde touch-action her tarayıcıda işlemez; yatay jest (geri git) şekil üstünde kapalı
    var a = false;
    alan.addEventListener('pointerdown', function (e) { a = true; try { alan.setPointerCapture(e.pointerId); } catch (_) {} var p = nokta(svg, e); fn(p.x, p.y); e.preventDefault(); });
    alan.addEventListener('pointermove', function (e) { if (a) { var p = nokta(svg, e); fn(p.x, p.y); } });
    alan.addEventListener('pointerup', function () { a = false; }); alan.addEventListener('pointercancel', function () { a = false; });
    ['click', 'touchstart', 'touchmove', 'touchend', 'wheel'].forEach(function (t) { alan.addEventListener(t, yut, { passive: true }); });
    alan.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { yut(e); e.preventDefault(); adim(e.key === 'ArrowRight' ? 1 : -1); }
    });
  }
  function seffaf(par, s) {            // görünmez dokunma alanı
    var at = { fill: '#000', 'fill-opacity': 0 };
    if (s.c) { at.cx = s.c[0]; at.cy = s.c[1]; at.r = s.c[2]; return el('circle', at, par); }
    at.x = s.r[0]; at.y = s.r[1]; at.width = s.r[2]; at.height = s.r[3]; at.rx = 8; return el('rect', at, par);
  }
  function ipucu(par, x, y, s) { return yazi(par, x, y, s, { 'font-size': 11.5, 'font-weight': 700, fill: C.gri, 'text-anchor': 'end' }); }
  function katman(svg, hit) { var g = el('g', { 'class': 'etk-k' }, svg); if (!hit) g.setAttribute('pointer-events', 'none'); return g; }

  // ------------------------------------------------------------------ 1 · odak: dokunulan bölüm öne çıkar, gerisi soluklaşır
  //   cfg.akis: hücre şekillerinde zardan geçen oklar boyunca iyon akışı; seçilen bozuklukta o taşıyıcının akışı durur
  function bosKose(svg, w, h) {        // ipucu için yazı ve kutu içermeyen köşe
    var vb = svg.viewBox.baseVal, K = [[vb.x + vb.width - 6, vb.y + vb.height - 5, 'end'], [vb.x + vb.width - 6, vb.y + 14, 'end'], [vb.x + 6, vb.y + vb.height - 5, 'start'], [vb.x + 6, vb.y + 14, 'start']];
    var B = [].map.call(svg.querySelectorAll('text, line, path, circle, ellipse, polygon'), function (e) { return e.closest('.etk-k') ? null : e.getBBox(); }).filter(Boolean);
    [].forEach.call(svg.querySelectorAll('rect'), function (r) { if (r.closest('.etk-k')) return; var q = r.getBBox(); if (q.width < vb.width * .995 || q.height < vb.height * .9) B.push(q); });
    for (var i = 0; i < K.length; i++) {
      var x0 = K[i][2] === 'end' ? K[i][0] - w : K[i][0], y0 = K[i][1] - h + 2;
      if (!B.some(function (q) { return q.x < x0 + w && q.x + q.width > x0 && q.y < y0 + h && q.y + q.height > y0; })) return K[i];
    }
    return null;
  }
  function odak(svg, cfg) {
    var vb = svg.viewBox.baseVal, slayt = svg.closest('.slide'), secili = -1;
    var akisK = cfg.akis ? katman(svg) : null;
    var ust = katman(svg), hit = katman(svg, true);
    var perde = el('path', { fill: '#fff', 'fill-rule': 'evenodd', opacity: 0, 'class': 'etk-perde' }, ust), halka = el('g', {}, ust);
    function bicim(s) { if (s.k) { var q = kutu(svg, s.k); return q ? { r: [q.x - 4, q.y - 4, q.w + 8, q.h + 8] } : null; } return s; }
    function yol(s) {
      if (s.c) { var x = s.c[0], y = s.c[1], r = s.c[2]; return 'M' + (x - r) + ' ' + y + 'a' + r + ' ' + r + ' 0 1 0 ' + 2 * r + ' 0a' + r + ' ' + r + ' 0 1 0 ' + (-2 * r) + ' 0Z'; }
      var q = s.r; return 'M' + q[0] + ' ' + q[1] + 'h' + q[2] + 'v' + q[3] + 'h' + (-q[2]) + 'Z';
    }
    function icinde(s, x, y) { if (s.c) return Math.hypot(x - s.c[0], y - s.c[1]) <= s.c[2]; var q = s.r; return x >= q[0] && x <= q[0] + q[2] && y >= q[1] && y <= q[1] + q[3]; }
    var H = cfg.hedef.map(function (h) { return { h: h, d: h.delik.map(bicim).filter(Boolean) }; });
    var ISA = [];   // ✗ (kayıp, kırmızı) ve ✓ (kazanım, yeşil) işaretleri
    if (cfg.akis) [].forEach.call(svg.querySelectorAll('ellipse'), function (e) {
      var f = e.getAttribute('fill'); if ((f !== '#c0392b' && f !== '#1f8a4c') || e.getBBox().width > 24) return;
      var g = [e], n = e.nextElementSibling;
      for (var k = 0; k < 2 && n && (n.tagName === 'line' || n.tagName === 'path'); k++) { g.push(n); n = n.nextElementSibling; }
      var q = e.getBBox(); ISA.push({ e: g, x: q.x + q.width / 2, y: q.y + q.height / 2, k: f === '#c0392b' });
    });
    // iyon akışı
    var A = [], saatA = null;
    if (cfg.akis) {
      A = cfg.akis.map(function (o) {
        var n = Math.max(2, Math.round(Math.hypot(o.x2 - o.x1, o.y2 - o.y1) / 70)), d = [];
        for (var k = 0; k < n; k++) d.push(el('circle', { r: 4.2, fill: o.c, stroke: '#fff', 'stroke-width': 1, opacity: 0 }, akisK));
        return { o: o, d: d, dur: false, L: Math.hypot(o.x2 - o.x1, o.y2 - o.y1) };
      });
      saatA = saat(svg, function (t) {
        A.forEach(function (a) {
          a.d.forEach(function (c, k) {
            var u = ((t * 70 / a.L) + k / a.d.length) % 1;
            if (a.hiz) u = ((t * 160 / a.L) + k / a.d.length) % 1;   // işlev kazanımı: akış hızlanır
            if (a.yav) u = ((t * 24 / a.L) + k / a.d.length) % 1;    // azalmış işlev: akış yavaşlar
            if (a.dur) { u = Math.min(u, .42); }       // işlev kaybı: iyon zara kadar gelir, geçemez
            c.setAttribute('cx', a.o.x1 + (a.o.x2 - a.o.x1) * u); c.setAttribute('cy', a.o.y1 + (a.o.y2 - a.o.y1) * u);
            c.setAttribute('opacity', a.dur ? .35 : (a.yav ? .6 : .95));
          });
        });
      });
      saatA.dg = function (o) { A.forEach(function (a) { a.d.forEach(function (c) { if (!o) c.setAttribute('opacity', 0); }); }); };
    }
    function satirlar(ad) {
      if (!slayt) return [];
      return [].filter.call(slayt.querySelectorAll('tr'), function (r) { var c = r.cells[0]; return c && ad && c.textContent.trim().indexOf(ad) === 0; });
    }
    function goster(i) {
      secili = i; halka.innerHTML = '';
      if (slayt) [].forEach.call(slayt.querySelectorAll('tr.etk-satir'), function (r) { r.classList.remove('etk-satir'); });
      var turler = {};
      A.forEach(function (a) {
        var tur = null;
        if (i >= 0 && H[i].h.etki) H[i].h.etki.forEach(function (e) { if (Math.abs(a.o.y1 - e[1]) < 14 && a.o.ms.some(function (m) { return Math.abs(m - e[0]) < 8; })) tur = e[2]; });
        else if (i >= 0 && H[i].d.some(function (s) { return a.o.ms.some(function (m) { return icinde(s, m, a.o.y1); }); })) tur = H[i].h.tur || 'x';
        a.hiz = tur === 'a'; a.yav = tur === 'y'; a.dur = tur === 'x'; if (tur) turler[tur] = 1;
      });
      ISA.forEach(function (o) {   // seçilen bozuklukla çelişen işaret (kazanımda ✗, kayıpta ✓) gizlenir
        var gizle = i >= 0 && H[i].d.some(function (s) { return icinde(s, o.x, o.y) || (s.c && Math.hypot(o.x - s.c[0], o.y - s.c[1]) < s.c[2] + 14); }) &&
          ((o.k && turler.a && !turler.x) || (!o.k && turler.x && !turler.a));
        o.e.forEach(function (e) { e.style.opacity = gizle ? 0 : ''; });
      });
      if (i < 0) { perde.setAttribute('opacity', 0); return; }
      var h = H[i];
      perde.setAttribute('d', 'M' + vb.x + ' ' + vb.y + 'h' + vb.width + 'v' + vb.height + 'h' + (-vb.width) + 'Z' + h.d.map(yol).join(''));
      perde.setAttribute('opacity', cfg.akis ? .7 : .8);
      h.d.forEach(function (s) { if (s.r) el('path', { d: yol(s), fill: 'none', stroke: cfg.renk || C.mavi, 'stroke-width': 3 }, halka); });
      satirlar(h.h.satir).forEach(function (r) { r.classList.add('etk-satir'); });
      if (saatA) saatA.bas();
    }
    H.forEach(function (h, i) { h.d.forEach(function (s) { dugme(seffaf(hit, s), h.h.ad, function () { goster(secili === i ? -1 : i); }); }); });
    svg.addEventListener('click', function (e) {
      if (secili >= 0) { yut(e); goster(-1); return; }          // odak açıkken boş yere dokunma odağı kapatır
      if (saatA) { yut(e); if (saatA.oyn) saatA.dur(); else saatA.bas(); }   // hücre şekli: akışı oynat / durdur
    });
    var ip = cfg.ipucu || (function () { var m = cfg.akis ? '☝ şekle dokunun: iyon akışı · etikete: bozukluk' : '☝ kutulara dokunun', k = bosKose(svg, m.length * 6.4, 14); return k ? [k[0], k[1], m, k[2]] : null; })();
    if (ip) yazi(ust, ip[0], ip[1], ip[2], { 'font-size': 11.5, 'font-weight': 700, fill: C.gri, 'text-anchor': ip[3] || 'end' });
  }

  // ------------------------------------------------------------------ 1a · kartlar: kutulu harita/sınıflama şekillerinde kutuları kendiliğinden bul
  function kartlar(svg, cfg) {
    var vb = svg.viewBox.baseVal;
    var T = [].filter.call(svg.querySelectorAll('text'), function (t) { return !t.closest('.etk-k') && t.textContent.trim(); }).map(function (t) { return { t: t, b: t.getBBox(), k: t.getAttribute('font-weight') === '800' }; });
    var R = [].filter.call(svg.querySelectorAll('rect'), function (r) { return !r.closest('.etk-k'); }).map(function (r) { return r.getBBox(); })
      .filter(function (b) { return b.width > 90 && b.height > 50 && b.width < vb.width * .9; });
    function ic(o) { return T.filter(function (q) { var cx = q.b.x + q.b.width / 2, cy = q.b.y + q.b.height / 2; return cx > o.x && cx < o.x + o.width && cy > o.y && cy < o.y + o.height; }); }
    var K = R.filter(function (o) { var q = ic(o); return q.length >= 3 && q.some(function (x) { return x.k && x.b.y - o.y < 30; }); });
    K = K.filter(function (o) { return !K.some(function (p) { return p !== o && p.x >= o.x - 1 && p.y >= o.y - 1 && p.x + p.width <= o.x + o.width + 1 && p.y + p.height <= o.y + o.height + 1; }); });
    if (K.length < 2) return;
    odak(svg, { ipucu: cfg && cfg.ipucu, hedef: K.map(function (o) {
      var bas = ic(o).filter(function (x) { return x.k; }).sort(function (a, b) { return a.b.y - b.b.y; })[0];
      return { ad: bas ? bas.t.textContent.trim() : 'kutu', delik: [{ r: [o.x - 4, o.y - 4, o.width + 8, o.height + 8] }] };
    }) });
  }

  // ------------------------------------------------------------------ 1b · hücre: etiketler, bağlantı çizgileri ve zardan geçen oklar kendiliğinden bulunur
  function hucre(svg, cfg) {
    cfg = cfg || {};
    var vb = svg.viewBox.baseVal, at = function (e, k) { return parseFloat(e.getAttribute(k)); };
    var Z = [].filter.call(svg.querySelectorAll('line'), function (l) { return at(l, 'stroke-width') >= 4 && Math.abs(at(l, 'x1') - at(l, 'x2')) < 1 && Math.abs(at(l, 'y2') - at(l, 'y1')) > 150; })
      .map(function (l) { return at(l, 'x1'); }).filter(function (x, i, a) { return a.indexOf(x) === i; });
    var OK = [].filter.call(svg.querySelectorAll('line[marker-end]'), function (l) { return Math.abs(at(l, 'y1') - at(l, 'y2')) < 4; }).map(function (l) {
      var x1 = at(l, 'x1'), x2 = at(l, 'x2'), y = at(l, 'y1'), m = Z.filter(function (z) { return Math.min(x1, x2) < z && Math.max(x1, x2) > z; });
      return m.length ? { x1: x1, y1: y, x2: x2, y2: at(l, 'y2'), c: l.getAttribute('stroke'), mx: m[0], ms: m } : null;
    }).filter(Boolean);
    var hedef = cfg.hedef;
    if (!hedef) {
      var bag = [].filter.call(svg.querySelectorAll('line[stroke-dasharray="2 4"]'), function () { return true; });
      var sekil = [].filter.call(svg.querySelectorAll('ellipse, circle'), function (e) { return !e.closest('.etk-k'); }).map(function (e) { return e.getBBox(); });
      var etk = [].filter.call(svg.querySelectorAll('rect[rx="8"][stroke-width="1.5"]'), function (r) { return !r.closest('.etk-k'); });
      hedef = [];
      etk.forEach(function (r) {
        var b = r.getBBox(), bas = null;
        [].some.call(svg.querySelectorAll('text[font-weight="800"]'), function (t) { var q = t.getBBox(); if (q.x > b.x && q.x < b.x + b.width && q.y > b.y && q.y < b.y + 26) { bas = t; return true; } });
        if (!bas) return;
        var d = [{ r: [b.x - 4, b.y - 4, b.width + 8, b.height + 8] }], hp = null;
        bag.forEach(function (l) {
          var p = [[at(l, 'x1'), at(l, 'y1')], [at(l, 'x2'), at(l, 'y2')]];
          for (var k = 0; k < 2; k++) {
            var u = p[k], v = p[1 - k];
            if (u[0] >= b.x - 8 && u[0] <= b.x + b.width + 8 && u[1] >= b.y - 8 && u[1] <= b.y + b.height + 8 && !(v[0] >= b.x - 8 && v[0] <= b.x + b.width + 8 && v[1] >= b.y - 8 && v[1] <= b.y + b.height + 8)) hp = v;
          }
        });
        var hedefN = null;
        if (hp) {
          var o = OK.filter(function (o) { return Math.abs(o.y1 - hp[1]) < 14 && hp[0] >= Math.min(o.x1, o.x2) - 16 && hp[0] <= Math.max(o.x1, o.x2) + 16; })[0];
          if (o) { var mx = o.ms.reduce(function (a, z) { return Math.abs(z - hp[0]) < Math.abs(a - hp[0]) ? z : a; }, o.ms[0]); hedefN = [mx, o.y1, 40]; }
          else {
            var s = sekil.filter(function (q) { return hp[0] >= q.x - 12 && hp[0] <= q.x + q.width + 12 && hp[1] >= q.y - 12 && hp[1] <= q.y + q.height + 12; })[0];
            hedefN = s ? [s.x + s.width / 2, s.y + s.height / 2, Math.max(s.width, s.height) / 2 + 12] : [hp[0], hp[1], 30];
          }
        }
        if (hedefN) d.push({ c: hedefN });
        var tur = hedefN && [].some.call(svg.querySelectorAll('ellipse[fill="#1f8a4c"], circle[fill="#1f8a4c"]'), function (e) {
          var q = e.getBBox(); return Math.hypot(q.x + q.width / 2 - hedefN[0], q.y + q.height / 2 - hedefN[1]) < 48 && q.width < 30; }) ? 'a' : 'x';
        hedef.push({ ad: bas.textContent.trim(), delik: d, tur: tur });
      });
    }
    odak(svg, { renk: C.kirmizi, hedef: hedef, akis: OK, ipucu: cfg.ipucu });
  }

  // ------------------------------------------------------------------ 2 · plazma değişimi: kalan madde = e^(−n)
  function plazma(svg) {
    var X0 = 110, KX = (1020 - 110) / 3, Y0 = 196, KY = 172, n = 1, ilk = true;
    var egri = [].filter.call(svg.querySelectorAll('path'), function (p) { return p.getAttribute('stroke') === '#c0392b'; })[0];
    var ust = katman(svg), hit = katman(svg, true);
    var gv = el('line', { stroke: C.mor, 'stroke-width': 2, 'stroke-dasharray': '4 3', opacity: 0 }, ust);
    var gh = el('line', { stroke: C.mor, 'stroke-width': 2, 'stroke-dasharray': '4 3', opacity: 0 }, ust);
    var nk = el('circle', { r: 8, fill: C.mor, stroke: '#fff', 'stroke-width': 2, opacity: 0 }, ust);
    var ok = el('g', { opacity: 0 }, ust);
    el('rect', { x: 425, y: 34, width: 205, height: 50, rx: 9, fill: '#fff', stroke: C.mor, 'stroke-width': 1.6 }, ok);
    var t1 = yazi(ok, 527, 55, '', { 'font-size': 13.5, 'font-weight': 800, fill: C.mor, 'text-anchor': 'middle' });
    var t2 = yazi(ok, 527, 74, '', { 'font-size': 12.5, fill: '#3d4d5c', 'text-anchor': 'middle' });
    ipucu(ust, 1018, 16, '↔ eğri boyunca sürükleyin');
    function kur(m) {
      n = Math.max(0, Math.min(3, Math.round(m * 10) / 10));
      if (ilk) {
        ilk = false; var d = '';
        for (var k = 0; k <= 60; k++) { var q = k / 20; d += (k ? 'L' : 'M') + (X0 + q * KX).toFixed(1) + ' ' + (Y0 - KY * Math.exp(-q)).toFixed(1); }
        if (egri) egri.setAttribute('d', d);
        [gv, gh, nk, ok].forEach(function (e) { e.setAttribute('opacity', 1); });
        [].forEach.call(svg.querySelectorAll('circle[fill="#0b6e99"], line[stroke="#0b6e99"]'), function (e) {   // 1,0 ve 1,5 işaretlerini tam eğriye oturt
          if (e.closest('.etk-k')) return;
          if (e.tagName === 'circle') { var m = (+e.getAttribute('cx') - X0) / KX; e.setAttribute('cy', (Y0 - KY * Math.exp(-m)).toFixed(1)); }
          else {
            var x1 = +e.getAttribute('x1'), x2 = +e.getAttribute('x2'), xm = Math.max(x1, x2), yy = (Y0 - KY * Math.exp(-(xm - X0) / KX)).toFixed(1);
            if (x1 === x2) e.setAttribute('y1', yy); else { e.setAttribute('y1', yy); e.setAttribute('y2', yy); }
          }
        });
      }
      var x = X0 + n * KX, kal = Math.exp(-n), y = Y0 - KY * kal;
      nk.setAttribute('cx', x); nk.setAttribute('cy', y);
      gv.setAttribute('x1', x); gv.setAttribute('y1', y); gv.setAttribute('x2', x); gv.setAttribute('y2', Y0);
      gh.setAttribute('x1', X0); gh.setAttribute('y1', y); gh.setAttribute('x2', x); gh.setAttribute('y2', y);
      t1.textContent = tr(n, 1) + ' plazma hacmi';
      t2.textContent = 'kalan %' + Math.round(kal * 100) + ' · uzaklaştırılan %' + Math.round((1 - kal) * 100);
    }
    var alan = el('rect', { x: X0 - 10, y: 18, width: 1020 - X0 + 20, height: 186, fill: '#000', 'fill-opacity': 0 }, hit);
    alan.setAttribute('aria-label', 'Değiştirilen plazma hacmini seçin');
    surukle(svg, alan, function (x) { kur((x - X0) / KX); }, function (d) { kur(n + d * .1); });
  }

  // ------------------------------------------------------------------ 2b · ürik asit: protone oran = 1 / (1 + 10^(pH − 5,5))
  function urik(svg) {
    var X0 = 90, X1 = 760, Y0 = 320, Y1 = 40, pH = 5.5, ilk = true;
    var ust = katman(svg), hit = katman(svg, true);
    var gv = el('line', { stroke: C.mor, 'stroke-width': 2, 'stroke-dasharray': '4 3', opacity: 0 }, ust);
    var gh = el('line', { stroke: C.mor, 'stroke-width': 2, 'stroke-dasharray': '4 3', opacity: 0 }, ust);
    var nk = el('circle', { r: 8, fill: C.mor, stroke: '#fff', 'stroke-width': 2, opacity: 0 }, ust);
    var ok = el('g', { opacity: 0 }, ust);
    el('rect', { x: 474, y: 70, width: 284, height: 50, rx: 9, fill: '#fff', stroke: C.mor, 'stroke-width': 1.6 }, ok);
    var t1 = yazi(ok, 616, 91, '', { 'font-size': 13.5, 'font-weight': 800, fill: C.mor, 'text-anchor': 'middle' });
    var t2 = yazi(ok, 616, 110, '', { 'font-size': 12.5, fill: '#3d4d5c', 'text-anchor': 'middle' });
    ipucu(ust, 756, 30, '↔ pH’ı sürükleyin');
    function kur(v) {
      pH = Math.max(4.5, Math.min(7.5, Math.round(v * 10) / 10));
      if (ilk) { ilk = false; [gv, gh, nk, ok].forEach(function (e) { e.setAttribute('opacity', 1); }); }
      var f = 1 / (1 + Math.pow(10, pH - 5.5)), x = X0 + (pH - 4.5) / 3 * (X1 - X0), y = Y0 - f * (Y0 - Y1);
      nk.setAttribute('cx', x); nk.setAttribute('cy', y);
      gv.setAttribute('x1', x); gv.setAttribute('y1', y); gv.setAttribute('x2', x); gv.setAttribute('y2', Y0);
      gh.setAttribute('x1', X0); gh.setAttribute('y1', y); gh.setAttribute('x2', x); gh.setAttribute('y2', y);
      t1.textContent = 'pH ' + tr(pH, 1) + ' · protone %' + Math.round(f * 100);
      var kat = 1 + Math.pow(10, pH - 5.5);
      t2.textContent = 'çözünürlük, tam protone hâle göre ≈ ' + (kat < 10 ? tr(kat, 1) : Math.round(kat)) + ' kat';
    }
    var alan = el('rect', { x: X0 - 10, y: Y1 - 4, width: X1 - X0 + 20, height: Y0 - Y1 + 8, fill: '#000', 'fill-opacity': 0 }, hit);
    alan.setAttribute('aria-label', 'İdrar pH’ını seçin');
    surukle(svg, alan, function (x) { kur(4.5 + (x - X0) / (X1 - X0) * 3); }, function (d) { kur(pH + d * .1); });
  }

  // ------------------------------------------------------------------ 3 · renal perfüzyon basıncı = OAB − SVB (OAB sabit 75)
  function perfuzyon(svg) {
    var R = [].slice.call(svg.querySelectorAll('rect')), T = [].slice.call(svg.querySelectorAll('text'));
    var at = function (e, k) { return e.getAttribute(k); };
    var sR = R.filter(function (r) { return at(r, 'x') === '660' && at(r, 'y') === '132'; })[0];
    var eR = R.filter(function (r) { return at(r, 'x') === '794' && at(r, 'y') === '132'; })[0];
    var sT = T.filter(function (t) { return t.textContent.trim() === 'SVB 18'; })[0];
    var eT = T.filter(function (t) { return t.textContent.indexOf('Etkin basınç') === 0; })[0];
    if (!sR || !eR || !sT || !eT) return;
    var K = 5.2, X0 = 660, W = 390, OAB = 75, s = 18;
    var pR = R.filter(function (r) { return at(r, 'x') === '620' && at(r, 'y') === '48'; })[0];
    var pT = T.filter(function (t) { return t.textContent.trim() === 'KONJESYONU SÜREN HASTA'; })[0];
    eR.parentNode.insertBefore(sT, eR.nextSibling);   // SVB yazısı çubukların üstünde kalsın
    var ust = katman(svg), hit = katman(svg, true);
    ipucu(ust, 1082, 88, '↔ SVB çubuğunu sürükleyin');
    function kur(v) {
      s = Math.round(Math.max(0, Math.min(30, v)));
      var ws = s * K, xe = X0 + ws + (s > 0 ? 8 : 0), we = X0 + W - xe, iyi = s < 8;
      sR.setAttribute('width', Math.max(ws, .01)); eR.setAttribute('x', xe); eR.setAttribute('width', we);
      eR.setAttribute('fill', iyi ? '#b8ecc9' : '#f3b7ae'); eR.setAttribute('stroke', iyi ? C.yesil : C.kirmizi);
      eT.textContent = 'Etkin basınç ≈ ' + (OAB - s) + ' mmHg'; eT.setAttribute('fill', iyi ? '#12603a' : '#7b1f14');
      if (pR) { pR.setAttribute('fill', iyi ? '#e8f6ef' : '#fdeaea'); pR.setAttribute('stroke', iyi ? C.yesil : C.kirmizi); }
      if (pT) { pT.textContent = iyi ? 'KONJESYONU ÇÖZÜLMÜŞ HASTA' : 'KONJESYONU SÜREN HASTA'; pT.setAttribute('fill', iyi ? '#12603a' : '#7b1f14'); }
      sT.textContent = 'SVB ' + s;
      if (ws >= 58) { sT.setAttribute('x', X0 + ws / 2); sT.setAttribute('text-anchor', 'middle'); sT.setAttribute('fill', '#fff'); eT.setAttribute('x', xe + we / 2); }
      else { sT.setAttribute('x', xe + 8); sT.setAttribute('text-anchor', 'start'); sT.setAttribute('fill', C.kirmizi); eT.setAttribute('x', xe + 62 + (we - 62) / 2); }
    }
    var alan = el('rect', { x: 640, y: 90, width: 430, height: 78, fill: '#000', 'fill-opacity': 0 }, hit);
    alan.setAttribute('aria-label', 'Santral venöz basıncı değiştirin');
    surukle(svg, alan, function (x) { kur((x - X0) / K); }, function (d) { kur(s + d); });
  }

  // ------------------------------------------------------------------ zaman akışı (yalnız slayt açıkken ve oynarken çalışır)
  function saat(svg, adim) {
    var o = { oyn: false, t: 0, son: 0 };
    function kare(z) {
      if (!o.oyn) return;
      if (!acik(svg)) { o.dur(); return; }
      var dt = o.son ? Math.min(.05, (z - o.son) / 1000) : 0; o.son = z; o.t += dt; adim(o.t, dt);
      requestAnimationFrame(kare);
    }
    o.bas = function () { if (o.oyn) return; o.oyn = true; o.son = 0; requestAnimationFrame(kare); if (o.dg) o.dg(true); };
    o.dur = function () { o.oyn = false; if (o.dg) o.dg(false); };
    return o;
  }
  function yolNokta(P, u) {           // çoklu çizgi üzerinde 0–1 arası konum
    var L = [], top = 0;
    for (var i = 1; i < P.length; i++) { var l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); L.push(l); top += l; }
    var h = Math.max(0, Math.min(1, u)) * top;
    for (i = 0; i < L.length; i++) { if (h <= L[i]) { var k = L[i] ? h / L[i] : 0; return [P[i][0] + (P[i + 1][0] - P[i][0]) * k, P[i][1] + (P[i + 1][1] - P[i][1]) * k]; } h -= L[i]; }
    return P[P.length - 1];
  }
  function arada(t, a, b) { return Math.max(0, Math.min(1, (t - a) / (b - a))); }
  function yumusak(u) { return u * u * (3 - 2 * u); }

  // ------------------------------------------------------------------ 4 · AVP → V2 → cAMP → PKA → AQP2 → su (hareketli)
  function avp(svg) {
    var ust = katman(svg), hit = katman(svg, true), mod = 'normal';
    var durum = yazi(ust, 540, 54, '', { 'font-size': 12.5, 'font-weight': 800, fill: C.mor, 'text-anchor': 'middle' });
    var kb = ['Gs · adenilat siklaz', 'cAMP', 'PKA'].map(function (a) { var q = kutu(svg, a); return el('rect', { x: q.x - 2, y: q.y - 2, width: q.w + 4, height: q.h + 4, rx: 9, fill: C.mor, opacity: 0 }, ust); });
    var hor = el('circle', { cx: 740, cy: 96, r: 10, fill: 'none', stroke: C.mor, 'stroke-width': 3, opacity: 0 }, ust);
    var avpN = el('circle', { r: 7, fill: C.mor, stroke: '#fff', 'stroke-width': 1.5, opacity: 0 }, ust);
    var kes = el('g', { opacity: 0 }, ust);
    el('circle', { r: 15, fill: '#fff', stroke: C.mavi, 'stroke-width': 2.4 }, kes); el('rect', { x: -8, y: -6, width: 5, height: 12, rx: 2, fill: C.mavi }, kes); el('rect', { x: 3, y: -6, width: 5, height: 12, rx: 2, fill: C.mavi }, kes);
    var zar = el('circle', { cx: 340, cy: 110, r: 16, fill: 'none', stroke: C.mavi, 'stroke-width': 3, opacity: 0 }, ust);
    var carpi = el('g', { opacity: 0 }, ust);
    el('circle', { r: 13, fill: C.kirmizi }, carpi); el('path', { d: 'M-5 -5L5 5M5 -5L-5 5', stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round' }, carpi);
    var SU = [[236, 110], [340, 110], [600, 122], [728, 130], [728, 288], [740, 292], [866, 292]];
    var damla = []; for (var i = 0; i < 16; i++) damla.push(el('circle', { r: 4.6, fill: C.su, opacity: 0 }, ust));
    var BOY = { normal: 11, v2: 4.2, aqp2: 6.2 };
    var YAZI = { normal: 'AVP → V2 → cAMP → PKA → AQP2 zarda → su geçer',
      v2: 'V2 reseptörü bozuk: sinyal yok, su geçmez',
      aqp2: 'AQP2 bozuk: kanal zara ulaşmaz, su geçmez' };
    function koy(e, p) { e.setAttribute('transform', 'translate(' + p[0] + ' ' + p[1] + ')'); }
    var kanal = [].filter.call(svg.querySelectorAll('rect'), function (r) { if (r.closest('.etk-k')) return false; var q = r.getBBox(); return Math.abs(q.x + q.width / 2 - 340) < 12 && Math.abs(q.y + q.height / 2 - 110) < 14 && q.width < 20; });
    var kasR = ['Gs · adenilat siklaz', 'cAMP', 'PKA'].map(function (a) { var t = metin(svg, a); return t; }).filter(Boolean);
    function soluk() {
      kanal.forEach(function (r) { r.style.opacity = mod === 'aqp2' ? .25 : ''; });
      kasR.forEach(function (t) { t.style.opacity = mod === 'v2' ? .3 : ''; });
    }
    function ciz(t) {
      var T = t % BOY[mod], g;
      g = yumusak(arada(T, 0, 1)); avpN.setAttribute('cx', 852 - 100 * g); avpN.setAttribute('cy', 96); avpN.setAttribute('opacity', T < BOY[mod] - .3 ? 1 : 0);
      var hz = arada(T, 1, 1.4); hor.setAttribute('r', 10 + 22 * hz); hor.setAttribute('opacity', mod === 'v2' ? 0 : (hz > 0 && hz < 1 ? 1 - hz : 0));
      kb.forEach(function (r, k) { var a = 1.3 + k * .4; r.setAttribute('opacity', mod !== 'v2' && T > a && T < BOY[mod] - .3 ? .28 : 0); });
      var ky = mod === 'v2' ? -1 : (mod === 'aqp2' ? .55 : 1), u = yumusak(arada(T, 2.5, 3.5));
      if (ky < 0 || T < 2.5) kes.setAttribute('opacity', 0);
      else { var uu = Math.min(u, ky); koy(kes, [412 + (350 - 412) * uu, 226 + (124 - 226) * uu]); kes.setAttribute('opacity', mod === 'aqp2' && T > 3.6 ? Math.max(0, 1 - (T - 3.6) * 1.5) : 1); }
      zar.setAttribute('opacity', mod === 'normal' && T > 3.5 && T < BOY[mod] - .3 ? 1 : 0);
      var cx = mod === 'v2' ? [752, 74] : (mod === 'aqp2' ? [376, 176] : null), ct = mod === 'v2' ? 1.1 : 3.1;
      if (cx && T > ct) { koy(carpi, cx); carpi.setAttribute('opacity', T < BOY[mod] - .3 ? 1 : 0); } else carpi.setAttribute('opacity', 0);
      damla.forEach(function (d, k) {
        var b = 3.6 + k * .42;
        if (mod !== 'normal' || T < b) { d.setAttribute('opacity', 0); return; }
        var u2 = ((T - b) / 5.4) % 1; var p = yolNokta(SU, u2);
        d.setAttribute('cx', p[0]); d.setAttribute('cy', p[1]); d.setAttribute('opacity', T > BOY[mod] - .4 ? 0 : .9);
      });
    }
    // statik kırmızı ✗ işaretleri (AQP2 ve V2): oynarken gizlenir, durunca geri gelir
    var isa = []; [].forEach.call(svg.querySelectorAll('circle, ellipse'), function (c) {
      if (c.closest('.etk-k') || c.getAttribute('fill') !== '#c0392b') return;
      isa.push(c); var n = c.nextElementSibling; for (var k = 0; k < 2 && n && n.tagName === 'line'; k++) { isa.push(n); n = n.nextElementSibling; }
    });
    var s = saat(svg, function (t) { ciz(t); });
    s.dg = function (o) {
      durum.textContent = o ? YAZI[mod] : (s.t > 0 ? '❚❚ durdu · dokunun: devam' : '');
      isa.forEach(function (e) { e.style.opacity = o ? 0 : ''; });
    };
    function sec(m) { mod = (mod === m ? 'normal' : m); soluk(); s.t = 0; ciz(0); s.bas(); s.dg(true); }
    var vb = svg.viewBox.baseVal;
    dugme(seffaf(hit, { r: [vb.x, vb.y, vb.width, vb.height] }), 'Hareketi oynat ya da durdur', function () { if (s.oyn) s.dur(); else s.bas(); });
    var q90 = kutu(svg, 'Konjenital · yaklaşık %90'), q10 = kutu(svg, 'Konjenital · yaklaşık %10');
    if (q90) dugme(seffaf(hit, { r: [q90.x, q90.y, q90.w, q90.h] }), 'V2 reseptörü bozukluğunu göster', function () { sec('v2'); });
    if (q10) dugme(seffaf(hit, { r: [q10.x, q10.y, q10.w, q10.h] }), 'AQP2 bozukluğunu göster', function () { sec('aqp2'); });
    ipucu(ust, 1066, 344, '▶ şekle dokunun: oynat · kırmızı etiket: bozukluk');
  }

  // ------------------------------------------------------------------ 5 · difüzyon ve konveksiyon (hareketli)
  function tasima(svg) {
    var ust = katman(svg), hit = katman(svg, true), id = 'etk' + Math.random().toString(36).slice(2, 7);
    var def = el('defs', {}, ust);
    function kirp(x, y, w, h) { var c = el('clipPath', { id: id + x }, def); el('rect', { x: x, y: y, width: w, height: h }, c); return 'url(#' + id + x + ')'; }
    var stat = [].filter.call(svg.querySelectorAll('circle'), function (c) { var x = +c.getAttribute('cx'); return x < 740; });
    function rnd(a, b) { return a + Math.random() * (b - a); }
    // difüzyon: zar x=190; kan solda aşağı, diyalizat sağda yukarı akar (zıt akım)
    var gD = el('g', { 'clip-path': kirp(18, 92, 344, 116) }, ust), D = [];
    for (var i = 0; i < 17; i++) { var b = i >= 14; D.push({ b: b, e: el('circle', { r: b ? 10 : 5.5, fill: b ? C.mor : C.mavi, opacity: 0 }, gD) }); }
    function dKur() { D.forEach(function (p) { p.x = rnd(32, 180); p.y = rnd(112, 190); p.vx = 0; p.vy = 0; }); }
    // konveksiyon: zar x=558; su akımı soldan sağa; büyük molekül (albümin boyu) zarda kalır
    var gK = el('g', { 'clip-path': kirp(386, 92, 344, 116) }, ust), K = [];
    for (i = 0; i < 26; i++) { var tip = i < 14 ? 's' : (i < 23 ? (i % 2 ? 'k' : 'o') : 'b'); K.push({ t: tip, e: el('circle', { r: { s: 2.6, k: 5, o: 8.5, b: 13 }[tip], fill: { s: '#9dc9dd', k: C.mavi, o: C.yesil, b: C.mor }[tip], opacity: 0 }, gK) }); }
    function kKur() { K.forEach(function (p) { p.x = rnd(392, 720); if (p.t === 'b' && p.x > 540) p.x = rnd(400, 540); p.y = [118, 152, 186][Math.floor(Math.random() * 3)] + rnd(-10, 10); }); }
    function dAdim(dt) {
      D.forEach(function (p) {
        p.vx = p.vx * .9 + rnd(-1, 1) * 260 * dt; p.vy = p.vy * .9 + rnd(-1, 1) * 160 * dt;
        var sol = p.x < 190, nx = p.x + p.vx * dt * 60 * .5, ny = p.y + p.vy * dt * 60 * .5 + (sol ? 16 : -16) * dt;
        if ((p.x < 190) !== (nx < 190) && (p.b ? Math.random() > .04 : Math.random() > .7)) { nx = p.x; p.vx = -p.vx; }
        p.x = Math.max(28, Math.min(352, nx)); p.y = ny;
        if (sol && p.y > 192) { p.y = 112; p.x = rnd(32, 180); }
        if (!sol && p.y < 110) { p.y = 112; p.x = rnd(32, 180); }        // diyalizat taşıdı; yerine kandan yenisi gelir
        if (sol && p.y < 110) p.y = 112; if (!sol && p.y > 192) p.y = 190;
        p.e.setAttribute('cx', p.x.toFixed(1)); p.e.setAttribute('cy', p.y.toFixed(1));
      });
    }
    function kAdim(dt) {
      K.forEach(function (p) {
        var v = p.t === 's' ? 95 : 70;
        if (p.t === 'b' && p.x > 532) { p.x = 532 + rnd(-2, 1); } else p.x += v * dt;
        p.y += rnd(-1, 1) * 22 * dt;
        if (p.x > 726) { p.x = rnd(392, 410); p.y = [118, 152, 186][Math.floor(Math.random() * 3)] + rnd(-10, 10); }
        p.e.setAttribute('cx', p.x.toFixed(1)); p.e.setAttribute('cy', p.y.toFixed(1));
      });
    }
    function panel(ad, x0, kur, adim, gizle) {
      var ip = ipucu(ust, x0 + 340, 32, '▶ dokunun');
      var s = saat(svg, function (t, dt) { adim(dt); });
      s.dg = function (o) {
        ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun';
        gizle.forEach(function (c) { c.setAttribute('opacity', o ? 0 : 1); });
        (ad === 'd' ? D : K).forEach(function (p) { p.e.setAttribute('opacity', o ? (p.t === 's' ? .85 : 1) : 0); });
      };
      dugme(seffaf(hit, { r: [x0, 14, 352, 272] }), ad === 'd' ? 'Difüzyonu oynat' : 'Konveksiyonu oynat', function () { if (s.oyn) s.dur(); else { kur(); s.bas(); } });
    }
    panel('d', 14, dKur, dAdim, stat.filter(function (c) { return +c.getAttribute('cx') < 370; }));
    panel('k', 382, kKur, kAdim, stat.filter(function (c) { return +c.getAttribute('cx') > 370; }));
  }

  // ------------------------------------------------------------------ 6 · anatomi (Ders 26–27, 20 Kasım 2026): yardımcılar
  function ogeler(svg, ad) { return [].slice.call(svg.querySelectorAll('[data-etk="' + ad + '"]')); }
  function yolNoktalari(p, n) {        // görünmez yol → nokta listesi
    var L = p.getTotalLength(), P = [];
    for (var i = 0; i <= n; i++) { var q = p.getPointAtLength(L * i / n); P.push([q.x, q.y]); }
    return P;
  }
  function damla(par, r) { return el('circle', { r: r || 3.3, fill: '#f2c23a', stroke: '#a8780f', 'stroke-width': .9, opacity: 0 }, par); }
  function parilti(par, x, y, r, renk) {   // ağrı yeri: yumuşak ışıma
    var id = 'etkg' + Math.random().toString(36).slice(2, 7), d = el('defs', {}, par), g = el('radialGradient', { id: id }, d);
    el('stop', { offset: 0, 'stop-color': renk, 'stop-opacity': .62 }, g); el('stop', { offset: .55, 'stop-color': renk, 'stop-opacity': .28 }, g);
    el('stop', { offset: 1, 'stop-color': renk, 'stop-opacity': 0 }, g);
    return el('circle', { cx: x, cy: y, r: r, fill: 'url(#' + id + ')' }, par);
  }
  function opak(e, v) { if (e) e.style.opacity = v; }

  // ------------------------------------------------------------------ 6a · taş böbrekten iner, üç darlıkta durur (s26_yer)
  function tasInis(svg) {
    var yol = svg.querySelector('[data-etk="yol"]'); if (!yol) return;
    var P = yolNoktalari(yol, 240), DUR = yol.getAttribute('data-dur').split(' ').map(Number);
    var T = [1, 2, 3].map(function (n) { return svg.querySelector('[data-etk="tas' + n + '"]'); });
    var C = [0, 1, 2, 3].map(function (n) { return svg.querySelector('[data-etk="c' + n + '"]'); });
    var ust = katman(svg), hit = katman(svg, true);
    var AG = T.map(function (t) {
      var a = t.getAttribute('data-agri').split(','), g = el('g', { opacity: 0 }, ust);
      parilti(g, +a[0], +a[1], +a[2], '#e0533b');
      yazi(g, +a[0], +a[1] + 4, 'ağrı: ' + a[3], { 'font-size': 11.5, 'font-weight': 800, fill: '#9c2a1c', 'text-anchor': 'middle', stroke: '#fff', 'stroke-width': 3, 'paint-order': 'stroke' });
      return g;
    });
    var vurgu = C.map(function (c) {
      if (!c) return null; var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      [].forEach.call(c.querySelectorAll('text'), function (t) { var q = t.getBBox(); x0 = Math.min(x0, q.x); y0 = Math.min(y0, q.y); x1 = Math.max(x1, q.x + q.width); y1 = Math.max(y1, q.y + q.height); });
      var r = el('rect', { 'class': 'etk-k', x: x0 - 9, y: y0 - 6, width: x1 - x0 + 18, height: y1 - y0 + 12, rx: 9, fill: '#fff1c2', stroke: '#e0a92a', 'stroke-width': 1.4, opacity: 0, 'pointer-events': 'none' });
      c.parentNode.insertBefore(r, c); return r;
    });
    var c0 = T[0].getAttribute('data-c').split(',').map(Number);
    var m = T[0].cloneNode(true); m.removeAttribute('data-etk'); m.setAttribute('opacity', 0); ust.appendChild(m);
    var halka = el('circle', { r: 10, fill: 'none', stroke: '#e0533b', 'stroke-width': 2.6, opacity: 0 }, ust);
    var durum = yazi(ust, 330, 393, '', { 'font-size': 12.5, 'font-weight': 800, fill: '#9c2a1c' });
    var ip = yazi(ust, 330, 374, '▶ dokunun: taş iner', { 'font-size': 11.5, 'font-weight': 700, fill: C.gri });
    var AD = ['üreteropelvik bileşkede takıldı', 'iliyak damar çaprazında takıldı', 'üreterovezikal bileşkede takıldı'];
    // zaman çizelgesi: [başlangıç, bitiş, u0, u1, durak]
    var Z = [], t = .4, u = 0, h = [1.3, 1.5, 1.5], bek = 2.4;
    for (var i = 0; i < 3; i++) { Z.push([t, t + h[i], u, DUR[i], -1]); t += h[i]; Z.push([t, t + bek, DUR[i], DUR[i], i]); t += bek; u = DUR[i]; }
    Z.push([t, t + .9, u, 1, -1]); var SON = t + 1.4;
    function konum(uu) { return P[Math.max(0, Math.min(P.length - 1, Math.round(uu * (P.length - 1))))]; }
    function sifirla() {
      T.forEach(function (e) { opak(e, ''); }); C.forEach(function (e) { opak(e, ''); });
      AG.forEach(function (g) { g.setAttribute('opacity', 0); }); vurgu.forEach(function (r) { if (r) r.setAttribute('opacity', 0); });
      m.setAttribute('opacity', 0); halka.setAttribute('opacity', 0); durum.textContent = '';
    }
    var s = saat(svg, function (tt) {
      if (tt > SON) { s.dur(); s.t = 0; sifirla(); ip.textContent = '▶ dokunun: yeniden'; return; }
      var z = Z.filter(function (q) { return tt >= q[0] && tt < q[1]; })[0] || (tt < Z[0][0] ? [0, .4, 0, 0, -1] : Z[Z.length - 1]);
      var f = yumusak(arada(tt, z[0], z[1])), uu = z[2] + (z[3] - z[2]) * f, p = konum(uu);
      m.setAttribute('transform', 'translate(' + (p[0] - c0[0]).toFixed(1) + ' ' + (p[1] - c0[1]).toFixed(1) + ') rotate(' + (uu * 540).toFixed(0) + ' ' + c0[0] + ' ' + c0[1] + ')');
      m.setAttribute('opacity', tt < .4 ? tt / .4 : (tt > SON - .5 ? Math.max(0, (SON - tt) / .5) : 1));
      var d = z[4];
      AG.forEach(function (g, k) { g.setAttribute('opacity', k === d ? Math.min(1, (tt - z[0]) * 2.5) : 0); });
      vurgu.forEach(function (r, k) { if (r) r.setAttribute('opacity', d >= 0 && k === d + 1 ? 1 : 0); });
      C.forEach(function (c, k) { opak(c, d >= 0 && k !== d + 1 ? .3 : ''); });
      if (d >= 0) { var q = (tt - z[0]) % 1.1 / 1.1; halka.setAttribute('cx', p[0]); halka.setAttribute('cy', p[1]); halka.setAttribute('r', 9 + 14 * q); halka.setAttribute('opacity', 1 - q); durum.textContent = (d + 1) + ' · ' + AD[d]; }
      else { halka.setAttribute('opacity', 0); durum.textContent = tt > Z[Z.length - 1][0] ? 'mesaneye geçti' : ''; }
    });
    s.dg = function (o) { ip.textContent = o ? '❚❚ dokunun: durdur' : (s.t > 0 ? '▶ dokunun: devam' : ip.textContent); if (o) T.forEach(function (e) { opak(e, 0); }); };
    dugme(seffaf(hit, { r: [6, 42, 600, 404] }), 'Taşın inişini oynat ya da durdur', function () { if (s.oyn) s.dur(); else s.bas(); });
  }

  // ------------------------------------------------------------------ 6b · hidronefroz derecesi sürgüyle 0 → 4 (s27_us)
  function derece(svg) {
    var D = [0, 1, 2, 3, 4].map(function (i) { return svg.querySelector('[data-etk="d' + i + '"]'); }); if (!D[4]) return;
    var X = D.map(function (g) { return +g.getAttribute('data-c').split(',')[0]; }), Y0 = 248, sec = -1;
    var ust = katman(svg), hit = katman(svg, true), ray = el('g', { opacity: 1 }, ust);
    el('line', { x1: X[0], y1: Y0, x2: X[4], y2: Y0, stroke: '#c9d6e0', 'stroke-width': 4, 'stroke-linecap': 'round' }, ray);
    X.forEach(function (x) { el('circle', { cx: x, cy: Y0, r: 4, fill: '#fff', stroke: '#9aabba', 'stroke-width': 1.6 }, ray); });
    var dol = el('line', { x1: X[0], y1: Y0, x2: X[0], y2: Y0, stroke: C.mavi, 'stroke-width': 4, 'stroke-linecap': 'round' }, ray);
    var dg = el('circle', { cx: X[0], cy: Y0, r: 8.5, fill: C.mavi, stroke: '#fff', 'stroke-width': 2.4, opacity: 0 }, ray);
    var cer = el('rect', { x: 0, y: 46, width: 196, height: 194, rx: 12, fill: 'none', stroke: C.mavi, 'stroke-width': 2.4, opacity: 0 }, ust);
    var ip = yazi(ust, X[0] - 86, 252, '↔ sürükleyin', { 'font-size': 11.5, 'font-weight': 700, fill: C.gri });
    D.forEach(function (g) { g.style.transition = 'opacity .25s'; });
    function kur(x) {
      var i = 0; X.forEach(function (xx, k) { if (Math.abs(xx - x) < Math.abs(X[i] - x)) i = k; });
      if (i === sec) return; sec = i;
      dg.setAttribute('opacity', 1); ip.setAttribute('opacity', 0);
      D.forEach(function (g, k) { g.style.opacity = k === i ? 1 : .28; });
      cer.setAttribute('x', X[i] - 98); cer.setAttribute('opacity', 1);
      dg.setAttribute('cx', X[i]); dol.setAttribute('x2', X[i]);
    }
    var alan = el('rect', { x: 6, y: 42, width: 1068, height: 216, fill: '#000', 'fill-opacity': 0 }, hit);
    alan.setAttribute('aria-label', 'Hidronefroz derecesini seçin');
    surukle(svg, alan, function (x) { kur(x); }, function (d) { kur(X[Math.max(0, Math.min(4, (sec < 0 ? 0 : sec) + d))]); });
  }

  // ------------------------------------------------------------------ 6c · nefrostomi ve double-J stentte idrar akışı (s27_dren)
  function drenAkis(svg) {
    var ust = katman(svg), hit = katman(svg, true), A = [];
    function ekle(ad, n, hiz, durgun) {
      ogeler(svg, ad).forEach(function (p) {
        var P = yolNoktalari(p, 120), L = p.getTotalLength(), d = [];
        for (var k = 0; k < n; k++) d.push(damla(ust, durgun ? 3 : 3.3));
        A.push({ P: P, L: L, d: d, hiz: hiz, durgun: durgun });
      });
    }
    ekle('kaliks', 2, 26); ekle('akis', 11, 52); ekle('durgun', 4, 14, true);
    var ip = ipucu(ust, 526, 378, '▶ dokunun: idrar akışı');
    var s = saat(svg, function (t) {
      A.forEach(function (a) {
        a.d.forEach(function (c, k) {
          var u = ((t * a.hiz / a.L) + k / a.d.length) % 1;
          if (a.durgun) u = Math.min(u * 1.2, .93 + .02 * Math.sin(t * 5 + k));     // taşın üstünde birikir, geçemez
          var q = a.P[Math.round(u * (a.P.length - 1))];
          c.setAttribute('cx', q[0]); c.setAttribute('cy', q[1]);
          c.setAttribute('opacity', a.durgun ? .55 : (u < .04 ? u / .04 : (u > .96 ? (1 - u) / .04 : .95)));
        });
      });
    });
    s.dg = function (o) { ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: idrar akışı'; if (!o) A.forEach(function (a) { a.d.forEach(function (c) { c.setAttribute('opacity', 0); }); }); };
    var vb = svg.viewBox.baseVal;
    dugme(seffaf(hit, { r: [vb.x, vb.y, vb.width, 388] }), 'İdrar akışını oynat ya da durdur', function () { if (s.oyn) s.dur(); else s.bas(); });
  }

  // ------------------------------------------------------------------ 6d · tek ↔ çift taraflı tıkanma: zaman içinde (s27_tek)
  function tekCift(svg) {
    var N = ogeler(svg, 'n'), Dd = ogeler(svg, 'd'), ET = ogeler(svg, 'et'), TAS = svg.querySelector('[data-etk="tas"]'); if (N.length < 2 || Dd.length < 2) return;
    var ust = katman(svg), hit = katman(svg, true), A = [];
    function ak(ad, n, hiz) { return ogeler(svg, ad).map(function (p) { var d = []; for (var k = 0; k < n; k++) d.push(damla(ust, 3)); var o = { P: yolNoktalari(p, 100), L: p.getTotalLength(), d: d, hiz: hiz, k: 1, ad: ad }; A.push(o); return o; }); }
    var aS = ak('akis-s', 6, 40), aO = ak('akis-o', 6, 40), aDur = ak('durgun', 4, 14), aR = ak('akis-r', 6, 40), aU = ak('akis-u', 3, 30);
    function olcer(x, y, bas) {
      var g = el('g', { opacity: 0 }, ust);
      yazi(g, x, y, bas, { 'font-size': 11.5, 'font-weight': 800, fill: '#3d4d5c' });
      el('rect', { x: x, y: y + 6, width: 170, height: 9, rx: 4.5, fill: '#e6ecf1' }, g);
      var b = el('rect', { x: x, y: y + 6, width: 34, height: 9, rx: 4.5, fill: C.yesil }, g);
      var t = yazi(g, x + 176, y + 15, 'normal', { 'font-size': 11.5, 'font-weight': 800, fill: C.yesil });
      return { g: g, b: b, t: t };
    }
    var mS = olcer(306, 254, 'serum kreatinin'), mC = olcer(852, 66, 'serum kreatinin');
    var olay = [yazi(ust, 300, 58, '', { 'font-size': 12, 'font-weight': 800, fill: C.kirmizi }), yazi(ust, 852, 58 - 20, '', { 'font-size': 12, 'font-weight': 800, fill: C.kirmizi })];
    var ip = ipucu(ust, 1066, 340, '▶ dokunun: tıkanma zaman içinde');
    var SON = 9.5;
    function dur_(t) {
      var a = yumusak(arada(t, 1.6, 4.6)), b = yumusak(arada(t, 2.6, 6.2));
      opak(Dd[0], Math.min(1, a * 2.2)); opak(N[0], 1 - arada(a, .25, 1)); opak(Dd[1], Math.min(1, b * 2.2)); opak(N[1], 1 - arada(b, .25, 1));
      opak(TAS, arada(t, 1.5, 1.9)); ET.forEach(function (e, k) { opak(e, arada(t, k ? 3.2 : 2.6, k ? 3.8 : 3.2)); });
      olay[0].textContent = t > 1.5 ? 'taş üreteri tıkadı' : ''; olay[1].textContent = t > 1.5 ? 'prostat çıkışı tıkadı' : '';
      aS.forEach(function (o) { o.k = t > 3 ? 1.7 : 1; }); aO.forEach(function (o) { o.k = t < 1.6 ? 1 : 0; }); aDur.forEach(function (o) { o.k = t >= 1.6 ? 1 : 0; });
      aR.forEach(function (o) { o.k = Math.max(0, 1 - arada(t, 1.6, 5.2)); }); aU.forEach(function (o) { o.k = t < 1.6 ? 1 : 0; });
      var r = arada(t, 3.2, 7.6), w = 34 + 120 * yumusak(r);
      mC.b.setAttribute('width', w); mC.b.setAttribute('fill', r > .25 ? C.kirmizi : C.yesil); mC.t.setAttribute('x', 852 + Math.max(w, 170) + 6);
      mC.t.textContent = r > .25 ? '↑ ABH' : 'normal'; mC.t.setAttribute('fill', r > .25 ? C.kirmizi : C.yesil);
      mS.t.textContent = 'normal';
    }
    var s = saat(svg, function (t, dt) {
      dur_(Math.min(t, SON));
      if (t > SON) ip.textContent = '❚❚ dokunun: durdur · yeniden';
      A.forEach(function (a) {
        a.u0 = (a.u0 || 0) + dt * a.hiz * (a.k || 0) / a.L;
        a.d.forEach(function (c, k) {
          var u = (a.u0 + k / a.d.length) % 1, q;
          if (a.ad === 'durgun') { u = Math.min(u * 1.25, .94 + .02 * Math.sin(t * 5 + k)); }
          q = a.P[Math.round(u * (a.P.length - 1))]; c.setAttribute('cx', q[0]); c.setAttribute('cy', q[1]);
          c.setAttribute('opacity', a.k ? (a.ad === 'durgun' ? .55 : .95) : Math.max(0, +c.getAttribute('opacity') - dt * 2));
        });
      });
    });
    s.dg = function (o) {
      ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: yeniden';
      if (o) { mS.g.setAttribute('opacity', 1); mC.g.setAttribute('opacity', 1); }
      else { A.forEach(function (a) { a.d.forEach(function (c) { c.setAttribute('opacity', 0); }); }); }
    };
    dugme(seffaf(hit, { r: [6, 6, 1068, 340] }), 'Tıkanmanın zaman içindeki etkisini oynat', function () {
      if (s.oyn) { s.dur(); if (s.t > SON) { s.t = 0; dur_(SON); } return; }
      if (s.t === 0) { A.forEach(function (a) { a.u0 = 0; }); dur_(0); }
      s.bas();
    });
  }

  // ------------------------------------------------------------------ 6e · Goldblatt: klips → renin ↑, kan basıncı ↑; 2K-1C ve 1K-1C farkı (s23_gold)
  function goldblatt(svg) {
    var G = ogeler(svg, 'g'); if (G.length < 2) return;
    var ust = katman(svg), hit = katman(svg, true), SON = 9;
    function sayi(e, k) { return e.getAttribute(k).split(',').map(Number); }
    var P = G.map(function (g) {
      var tip = g.getAttribute('data-tip'), kl = sayi(g, 'data-klips'), bo = sayi(g, 'data-bob'), ao = sayi(g, 'data-ao'), ku = sayi(g, 'data-kut'), fz = sayi(g, 'data-faz');
      var o = { tip: tip, kl: kl, bo: bo, ao: ao, d: [], g: el('g', { opacity: 0 }, ust) };
      o.halka = el('circle', { cx: kl[0], cy: kl[1], r: 8, fill: 'none', stroke: C.kirmizi, 'stroke-width': 2.4, opacity: 0 }, ust);
      o.vx = ao[0] - 30; o.vy = bo[1] + 22; o.vt = Math.max(ao[1] + 40, 118);   // renin dolaşıma renal ven → vena kava yoluyla girer (arter yoluyla değil)
      o.ven = el('path', { d: 'M' + bo[0] + ',' + o.vy + ' H' + o.vx + ' M' + o.vx + ',' + (bo[1] + 70) + ' V' + o.vt, fill: 'none', stroke: '#4f78b0', 'stroke-width': 3.4, 'stroke-linecap': 'round', opacity: 0 }, ust);
      o.vyz = yazi(ust, (bo[0] + o.vx) / 2, o.vy + 17, 'renal ven', { 'font-size': 10.5, 'font-weight': 700, fill: '#4f78b0', 'text-anchor': 'middle', opacity: 0 });
      o.vkz = yazi(ust, o.vx + 4, o.vt - 7, 'v. kava', { 'font-size': 10.5, 'font-weight': 700, fill: '#4f78b0', 'text-anchor': 'end', opacity: 0 });
      for (var i = 0; i < 9; i++) o.d.push(el('circle', { r: 3.4, fill: '#e8b423', stroke: '#8a6400', 'stroke-width': .8, opacity: 0 }, ust));
      function bar(y, ad) {
        yazi(o.g, ku[0], y + 9, ad, { 'font-size': 11, 'font-weight': 800, fill: '#3d4d5c' });
        el('rect', { x: ku[0] + 74, y: y, width: 110, height: 10, rx: 5, fill: '#e6ecf1' }, o.g);
        return el('rect', { x: ku[0] + 74, y: y, width: 22, height: 10, rx: 5, fill: C.yesil }, o.g);
      }
      el('rect', { x: ku[0] - 8, y: ku[1] - 6, width: 204, height: 62, rx: 8, fill: '#fff', opacity: .88 }, o.g);
      o.b = [bar(ku[1], 'renin'), bar(ku[1] + 18, 'volüm'), bar(ku[1] + 36, 'kan basıncı')];
      o.f = [yazi(ust, fz[0], fz[1], '', { 'font-size': 11.6, 'font-weight': 800, fill: C.kirmizi }), yazi(ust, fz[0], fz[1] + 16, '', { 'font-size': 11.2, 'font-weight': 700, fill: '#3d4d5c' })];
      return o;
    });
    function dol(r, v, yuk) { r.setAttribute('width', 22 + 88 * v); r.setAttribute('fill', v > .45 ? (yuk || C.kirmizi) : C.yesil); }
    var ip = ipucu(ust, 1066, 376, '▶ dokunun: klips takılır');
    function an(t) {
      P.forEach(function (o) {
        var k = o.tip === '1k', ren = yumusak(arada(t, .8, 2.6)), vol = 0, bp = yumusak(arada(t, 1.6, 4.6));
        if (k) { ren = ren * (1 - .8 * yumusak(arada(t, 4.4, 7.6))); vol = yumusak(arada(t, 3.6, 7.2)); }
        else vol = .12 * Math.sin(Math.PI * arada(t, 2, 5));
        o.g.setAttribute('opacity', Math.min(1, t * 3));
        dol(o.b[0], ren); dol(o.b[1], vol, C.mavi); dol(o.b[2], bp);
        var q = (t % 1.2) / 1.2; o.ven.setAttribute('opacity', (.75 * ren).toFixed(2)); o.vyz.setAttribute('opacity', ren.toFixed(2)); o.vkz.setAttribute('opacity', ren.toFixed(2)); o.halka.setAttribute('r', 8 + 12 * q); o.halka.setAttribute('opacity', t < 7 ? (1 - q) * .9 : 0);
        o.d.forEach(function (c, i) {
          var u = ((t * .55) + i / o.d.length) % 1, x, y;
          if (u < .45) { var f = u / .45; x = o.bo[0] + (o.vx - o.bo[0]) * f; y = o.vy + 2 * Math.sin(f * 6); }
          else { var g = (u - .45) / .55; x = o.vx + (i % 2 ? 1.5 : -1.5); y = o.vy - g * (o.vy - o.vt); }
          c.setAttribute('cx', x.toFixed(1)); c.setAttribute('cy', y.toFixed(1)); c.setAttribute('opacity', (ren * (u < .06 ? u / .06 : u > .9 ? (1 - u) / .1 : 1)).toFixed(2));
        });
        var s1, s2;
        if (!k) { s1 = t < 1.6 ? 'klips: perfüzyon ↓' : 'renin ↑ · kan basıncı ↑'; s2 = t < 3.6 ? '' : 'karşı böbrek tuzu atar'; }
        else { s1 = t < 1.6 ? 'klips: perfüzyon ↓' : (t < 4.4 ? 'renin ↑ · kan basıncı ↑' : 'tuz ve su tutulur: volüm ↑'); s2 = t < 4.4 ? '' : 'renin iner, basınç yüksek'; }
        o.f[0].textContent = s1; o.f[1].textContent = s2;
      });
    }
    var s = saat(svg, function (t) { an(Math.min(t, SON)); if (t > SON + 1.5) s.dur(); });
    s.dg = function (o) {
      ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: yeniden';
      if (!o) P.forEach(function (p) { p.d.forEach(function (c) { c.setAttribute('opacity', 0); }); p.halka.setAttribute('opacity', 0); p.ven.setAttribute('opacity', 0); p.vyz.setAttribute('opacity', 0); p.vkz.setAttribute('opacity', 0); });
    };
    dugme(seffaf(hit, { r: [6, 42, 1068, 262] }), 'Klips takıldıktan sonraki değişimi oynat', function () {
      if (s.oyn) { s.dur(); return; }
      if (s.t > SON) s.t = 0;
      s.bas();
    });
  }

  // ------------------------------------------------------------------ 6f · orak hücre: vasa rektada inen eritrosit oraklaşır, papillada tıkar (s17_orak)
  function orak(svg) {
    var yol = svg.querySelector('[data-etk="yol"]'); if (!yol) return;
    var P = yolNoktalari(yol, 160), K = [1, 2, 3].map(function (n) { return svg.querySelector('[data-etk="k' + n + '"]'); });
    var ust = katman(svg), hit = katman(svg, true);
    var V = K.map(function (c) {
      var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      [].forEach.call(c.querySelectorAll('text'), function (t) { var q = t.getBBox(); x0 = Math.min(x0, q.x); y0 = Math.min(y0, q.y); x1 = Math.max(x1, q.x + q.width); y1 = Math.max(y1, q.y + q.height); });
      var r = el('rect', { 'class': 'etk-k', x: x0 - 8, y: y0 - 5, width: x1 - x0 + 16, height: y1 - y0 + 10, rx: 8, fill: '#fde3df', stroke: C.kirmizi, 'stroke-width': 1.2, opacity: 0, 'pointer-events': 'none' });
      c.parentNode.insertBefore(r, c); return r;
    });
    var g = el('g', { opacity: 0 }, ust);
    var disk = el('ellipse', { rx: 6.2, ry: 5, fill: '#d13a2c', stroke: '#7d1a12', 'stroke-width': 1 }, g);
    el('ellipse', { rx: 2.4, ry: 1.8, fill: '#a8261b', opacity: .7 }, g);
    var hilal = el('path', { d: 'M-8,1 Q0,-9 8,1 Q0,-4 -8,1 Z', fill: '#c0392b', stroke: '#7d1a12', 'stroke-width': 1, opacity: 0 }, g);
    var halka = el('circle', { r: 8, fill: 'none', stroke: C.kirmizi, 'stroke-width': 2.4, opacity: 0 }, ust);
    var ip = ipucu(ust, 440, 60, '▶ dokunun: eritrosit iner');
    var SON = 7.5;
    var s = saat(svg, function (t) {
      var u = Math.min(1, t / 5.5), p = P[Math.round(u * (P.length - 1))];
      g.setAttribute('transform', 'translate(' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + ')');
      g.setAttribute('opacity', Math.min(1, t * 3));
      var m = yumusak(arada(u, .3, .75)); disk.setAttribute('opacity', 1 - m); disk.nextSibling.setAttribute('opacity', .7 * (1 - m)); hilal.setAttribute('opacity', m);
      hilal.setAttribute('transform', 'rotate(' + (40 * m) + ')');
      V.forEach(function (r, k) { r.setAttribute('opacity', u > k / 3 + .05 ? 1 : 0); });
      if (u >= 1) { var q = ((t - 5.5) % 1.1) / 1.1; halka.setAttribute('cx', p[0]); halka.setAttribute('cy', p[1]); halka.setAttribute('r', 8 + 14 * q); halka.setAttribute('opacity', 1 - q); }
      else halka.setAttribute('opacity', 0);
      if (t > SON) s.dur();
    });
    s.dg = function (o) {
      ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: yeniden';
      if (!o) { g.setAttribute('opacity', 0); halka.setAttribute('opacity', 0); V.forEach(function (r) { r.setAttribute('opacity', 0); }); }
    };
    dugme(seffaf(hit, { r: [6, 42, 440, 336] }), 'Eritrositin vasa rektada inişini oynat', function () { if (s.oyn) { s.dur(); return; } s.t = 0; s.bas(); });
  }

  // ------------------------------------------------------------------ 6g · ADPKD: kistler yaşla büyür (s19_har, ilk kart)
  function kistYas(svg) {
    var A0 = svg.querySelector('[data-etk="adpkd"]'), Y = [0, 1, 2].map(function (i) { return svg.querySelector('[data-etk="yas' + i + '"]'); });
    if (!A0 || !Y[2]) return;
    var ust = katman(svg), hit = katman(svg, true), SON = 7;
    var yaz = yazi(ust, 142, 130, '', { 'font-size': 12, 'font-weight': 800, fill: C.kirmizi });
    var ip = ipucu(ust, 348, 136, '▶ dokunun: yaşla');
    function an(t) {
      var a = [arada(t, .2, .8) * (1 - arada(t, 1.8, 2.4)), arada(t, 1.8, 2.4) * (1 - arada(t, 3.6, 4.2)), arada(t, 3.6, 4.2)];
      Y.forEach(function (e, i) { e.style.opacity = a[i]; });
      A0.style.opacity = t > 0 ? 1 - arada(t, 0, .4) : 1;
      yaz.textContent = t < .2 ? '' : (t < 2.1 ? '20 yaş' : (t < 3.9 ? '40 yaş' : '60 yaş'));
    }
    var s = saat(svg, function (t) { an(Math.min(t, SON)); if (t > SON) s.dur(); });
    s.dg = function (o) {
      ip.textContent = o ? '❚❚' : '▶ dokunun: yaşla';
      if (!o) { Y.forEach(function (e) { e.style.opacity = 0; }); A0.style.opacity = 1; yaz.textContent = ''; }
    };
    dugme(seffaf(hit, { r: [6, 6, 350, 138] }), 'ADPKD böbreğinin yaşla büyümesini oynat', function () { if (s.oyn) { s.dur(); return; } s.t = 0; s.bas(); });
  }

  // ------------------------------------------------------------------ 6h · VUR: kontrast mesaneden yukarı kaçar, derece I → V (x21_31)
  function reflu(svg) {
    var U = [0, 1, 2, 3, 4].map(function (i) {
      var g = svg.querySelector('[data-etk="v' + i + '"]'), y = svg.querySelector('[data-etk="vy' + i + '"]');
      return g && y ? { g: g, e: svg.querySelector('[data-etk="ve' + i + '"]'), P: yolNoktalari(y, 90) } : null;
    });
    if (!U[4]) return;
    var ust = katman(svg), hit = katman(svg, true), SURE = 1.9, SON = SURE * 5 + .4;
    U.forEach(function (u) {
      u.d = [0, 1, 2, 3].map(function () { return el('circle', { r: 2.7, fill: '#fff', stroke: '#8a5a00', 'stroke-width': 1.3, opacity: 0 }, ust); });
      var b = u.g.getBBox(); u.cer = el('rect', { x: b.x - 6, y: b.y - 6, width: b.width + 12, height: 323 - b.y, rx: 10, fill: 'none', stroke: C.mavi, 'stroke-width': 2, opacity: 0 }, ust);
      u.g.style.transition = 'opacity .25s'; if (u.e) u.e.style.transition = 'opacity .25s';
    });
    var ip = ipucu(ust, 634, 22, '▶ dokunun: kontrast yukarı kaçar');
    function sifir() { U.forEach(function (u) { u.g.style.opacity = 1; if (u.e) u.e.style.opacity = 1; u.cer.setAttribute('opacity', 0); u.d.forEach(function (c) { c.setAttribute('opacity', 0); }); }); }
    var s = saat(svg, function (t) {
      var i = Math.min(4, Math.floor(t / SURE)), tl = t - i * SURE;
      U.forEach(function (u, k) {
        var a = k === i; u.g.style.opacity = a ? 1 : .3; if (u.e) u.e.style.opacity = a ? 1 : .35; u.cer.setAttribute('opacity', a ? 1 : 0);
        u.d.forEach(function (c, n) {
          if (!a) { c.setAttribute('opacity', 0); return; }
          var q = (tl / 1.5) - n * .14;                          // damlalar art arda, mesaneden ulaştığı yere
          if (q < 0 || q > 1.02) { c.setAttribute('opacity', q > 1.02 ? .9 : 0); if (q > 1.02) { var z = u.P[u.P.length - 1 - n * 3]; c.setAttribute('cx', z[0]); c.setAttribute('cy', z[1]); } return; }
          var z2 = u.P[Math.round(yumusak(Math.min(1, q)) * (u.P.length - 1 - n * 3))]; c.setAttribute('cx', z2[0]); c.setAttribute('cy', z2[1]); c.setAttribute('opacity', 1);
        });
      });
      if (t > SON) s.dur();
    });
    s.dg = function (o) { ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: yeniden'; if (!o) sifir(); };
    dugme(seffaf(hit, { r: [6, 28, 634, 286] }), 'Reflü derecelerini sırayla oynat', function () { if (s.oyn) { s.dur(); return; } s.t = 0; s.bas(); });
  }

  // ------------------------------------------------------------------ 6i · endovasküler fistül: üç aşama + akım (s38_eav)
  function endoAvf(svg) {
    var G = [0, 1, 2].map(function (i) { return svg.querySelector('[data-etk="e' + i + '"]'); });
    var y1 = svg.querySelector('[data-etk="ak1"]'), y2 = svg.querySelector('[data-etk="ak2"]'), kv = svg.querySelector('[data-etk="kv"]');
    if (!G[2] || !y1 || !y2) return;
    var P1 = yolNoktalari(y1, 80), P2 = yolNoktalari(y2, 110), ust = katman(svg), hit = katman(svg, true), SON = 9.5;
    G.forEach(function (g) { g.style.transition = 'opacity .3s'; });
    var kx = kv ? +kv.getAttribute('cx') : 0, ky = kv ? +kv.getAttribute('cy') : 0;
    var hal = el('circle', { cx: kx, cy: ky, r: 6, fill: 'none', stroke: '#ff9a2e', 'stroke-width': 3, opacity: 0 }, ust);
    var D1 = [0, 1, 2, 3, 4].map(function () { return el('circle', { r: 3, fill: '#fff', stroke: C.kirmizi, 'stroke-width': 1.4, opacity: 0 }, ust); });
    var D2 = [0, 1, 2, 3, 4, 5].map(function () { return el('circle', { r: 3, fill: '#fff', stroke: '#6a3ea1', 'stroke-width': 1.4, opacity: 0 }, ust); });
    var ip = ipucu(ust, 1074, 422, '▶ dokunun: adım adım');
    function sifir() { G.forEach(function (g) { g.style.opacity = 1; }); hal.setAttribute('opacity', 0); D1.concat(D2).forEach(function (c) { c.setAttribute('opacity', 0); }); }
    function akit(D, P, t, hiz) {
      D.forEach(function (c, n) {
        var q = ((t * hiz) + n / D.length) % 1, z = P[Math.round(q * (P.length - 1))];
        c.setAttribute('cx', z[0]); c.setAttribute('cy', z[1]); c.setAttribute('opacity', 1);
      });
    }
    var s = saat(svg, function (t) {
      var i = t < 2 ? 0 : (t < 4 ? 1 : 2);
      G.forEach(function (g, k) { g.style.opacity = k === i ? 1 : .3; });
      if (i === 1) { var q = ((t - 2) % .8) / .8; hal.setAttribute('r', 5 + 16 * q); hal.setAttribute('opacity', (1 - q).toFixed(2)); } else hal.setAttribute('opacity', 0);
      if (i === 2) { akit(D1, P1, t - 4, .35); akit(D2, P2, t - 4, .28); } else D1.concat(D2).forEach(function (c) { c.setAttribute('opacity', 0); });
      if (t > SON) s.dur();
    });
    s.dg = function (o) { ip.textContent = o ? '❚❚ dokunun' : '▶ dokunun: yeniden'; if (!o) sifir(); };
    dugme(seffaf(hit, { r: [6, 6, 1068, 372] }), 'Endovasküler fistül aşamalarını oynat', function () { if (s.oyn) { s.dur(); return; } s.t = 0; s.bas(); });
  }

  // ------------------------------------------------------------------ slayt kimliği → kurulum
  var K = {
    x30_5: function (svg) {
      odak(svg, { ipucu: [1134, 257, '☝ kutulara dokunun'], hedef: [
        { ad: 'Damar ve hemodinamik', delik: [{ k: '1 · Damar' }], satir: 'Afferent/efferent' },
        { ad: 'Glomerül', delik: [{ k: '2 · Glomerül' }], satir: 'Glomerül' },
        { ad: 'Proksimal tübül', delik: [{ k: '3 · Proksimal' }], satir: 'Proksimal tübül' },
        { ad: 'İnterstisyum', delik: [{ k: '4 · İnterstisyum' }], satir: 'İnterstisyum' },
        { ad: 'Distal tübül ve toplayıcı kanal', delik: [{ k: '5 · Distal' }], satir: 'Distal tübül' },
        { ad: 'Tübül lümeni ve kristal', delik: [{ k: '6 · Tübül lümeni' }], satir: 'Tübül lümeni' },
        { ad: 'Mikrovasküler ve ilaç ilişkili TMA', delik: [{ k: '7 · Mikrovasküler' }], satir: 'Glomerül' },
        { ad: 'Dolaylı hasar', delik: [{ k: '8 · Dolaylı' }] }] });
    },
    s21_tal: function (svg) {
      hucre(svg, { ipucu: [1066, 404, '☝ şekle dokunun: iyon akışı · etikete: bozukluk'], hedef: [
        { ad: 'Bartter tip 1: NKCC2', delik: [{ k: 'Bartter tip 1' }, { c: [340, 98, 46] }], etki: [[340, 98, 'x'], [340, 380, 'y']] },
        { ad: 'Bartter tip 2: ROMK', delik: [{ k: 'Bartter tip 2' }, { c: [340, 196, 46] }], etki: [[340, 196, 'x'], [340, 98, 'y'], [340, 380, 'y']] },
        { ad: 'Bartter tip 3: ClC-Kb', delik: [{ k: 'Bartter tip 3' }, { c: [740, 170, 46] }], etki: [[740, 170, 'x'], [340, 98, 'y']] },
        { ad: 'Bartter tip 4: barttin, ClC-Ka ve ClC-Kb', delik: [{ k: 'Bartter tip 4' }, { r: [704, 132, 72, 140] }], etki: [[740, 170, 'x'], [340, 98, 'y']] },
        { ad: 'Bartter tip 5: MAGE-D2', delik: [{ k: 'Bartter tip 5' }, { c: [440, 296, 52] }, { c: [340, 98, 46] }], etki: [[340, 98, 'y'], [340, 380, 'y']] },
        { ad: 'FHHNC: klodin 16 ve 19', delik: [{ k: 'FHHNC' }, { r: [340, 348, 400, 64] }] }] });
    },
    x39_8: plazma, x43_43: perfuzyon, s21_avp: avp, x36_4: tasima, s26_uri: urik,
    s26_yer: tasInis, s27_us: derece, s27_dren: drenAkis, s27_tek: tekCift, s23_gold: goldblatt, s17_orak: orak, s19_har: kistYas, x21_31: reflu, s38_eav: endoAvf
  };
  var IP = ['☝ şekle dokunun: iyon akışı · etikete: bozukluk'];
  function H_(ad, k, delik, etki) { return { ad: ad, delik: [{ k: k }].concat(delik || []), etki: etki }; }
  var ELLE = {
    s21_dkt: [H_('Gitelman sendromu: NCC', 'Gitelman sendromu', [{ c: [340, 98, 46] }], [[340, 98, 'x'], [340, 222, 'y']]),
      H_('Hipomagnezemi: TRPM6 azalır', 'Hipomagnezemi', [{ c: [340, 222, 46] }], [[340, 222, 'y']]),
      H_('EAST / SeSAME: Kir4.1', 'EAST / SeSAME', [{ c: [740, 184, 46] }], [[740, 184, 'x'], [340, 98, 'y']]),
      H_('Bartter tip 3: ClC-Kb', 'Bartter tip 3', [{ c: [740, 286, 46] }], [[740, 286, 'x'], [340, 98, 'y']])],
    s21_esas: [H_('Liddle sendromu: ENaC işlev kazanımı', 'Liddle sendromu', [{ c: [340, 100, 48] }, { c: [440, 178, 40] }], [[340, 100, 'a'], [340, 306, 'a']]),
      H_('PHA tip 1 resesif: ENaC işlev kaybı', 'PHA tip 1 · resesif', [{ c: [340, 100, 48] }], [[340, 100, 'x'], [340, 306, 'y']]),
      H_('PHA tip 1 dominant: MR işlev kaybı', 'PHA tip 1 · dominant', [{ r: [588, 192, 74, 50] }], [[340, 100, 'y'], [340, 306, 'y']]),
      H_('Geller sendromu: MR işlev kazanımı', 'Geller sendromu', [{ r: [588, 192, 74, 50] }], [[340, 100, 'a'], [340, 306, 'a']]),
      H_('AME: 11β-HSD2 eksikliği', 'AME', [{ r: [596, 282, 108, 46] }, { r: [588, 192, 74, 50] }], [[340, 100, 'a'], [340, 306, 'a']])],
    s21_gordon: [H_('Gordon sendromu: NCC aşırı etkin', 'Gordon sendromu', [{ c: [340, 108, 48] }], [[340, 108, 'a'], [340, 270, 'y']]),
      H_('Hiperkalemi ve asidoz: ROMK azalır', 'Hiperkalemi + asidoz', [{ c: [340, 270, 48] }], [[340, 270, 'y']]),
      H_('KLHL3 · CUL3 mutasyonu', 'KLHL3 · CUL3 mutasyonu', [{ r: [584, 56, 142, 96] }], [[340, 108, 'a'], [340, 270, 'y']]),
      H_('WNK1 · WNK4 mutasyonu', 'WNK1 · WNK4 mutasyonu', [{ r: [426, 146, 290, 44] }], [[340, 108, 'a'], [340, 270, 'y']]),
      H_('Takrolimus: kalsinörin baskılanır', 'Takrolimus', [{ r: [468, 218, 112, 40] }], [[340, 108, 'a'], [340, 270, 'y']])],
    s21_fanconi: [H_('Glukozüri: SGLT2', 'Glukozüri', [{ c: [340, 78, 40] }], [[340, 78, 'x']]),
      H_('Fosfatüri: NaPi-IIa/IIc', 'Fosfatüri', [{ c: [340, 150, 40] }], [[340, 150, 'x']]),
      H_('Aminoasidüri', 'Yaygın aminoasidüri', [{ c: [340, 222, 40] }], [[340, 222, 'x']]),
      H_('Bikarbonatüri: NHE3 ve NBCe1', 'Bikarbonatüri', [{ c: [340, 294, 40] }, { c: [740, 196, 40] }], [[340, 294, 'x'], [740, 196, 'x']]),
      H_('DMA proteinüri: megalin–kübilin', 'DMA proteinüri', [{ c: [340, 366, 40] }], [[340, 366, 'x']]),
      H_('Ortak yol: enerji ve pompa', 'Sık ortak yol', [{ c: [740, 92, 40] }, { c: [584, 160, 54] }], [[740, 92, 'y'], [340, 78, 'y'], [340, 150, 'y'], [340, 222, 'y'], [340, 294, 'y'], [340, 366, 'y']]),
      H_('Fanconi-Bickel sendromu: GLUT2', 'Fanconi-Bickel', [{ c: [740, 278, 40] }], [[740, 278, 'x']]),
      H_('Neden hepsi birlikte bozulur', 'Neden hepsi birlikte', [{ c: [740, 92, 40] }, { c: [584, 160, 54] }], [[740, 92, 'y'], [340, 78, 'y'], [340, 150, 'y'], [340, 222, 'y'], [340, 294, 'y'], [340, 366, 'y']])],
    s21_endo: [H_('OCRL: kesecik trafiği', 'OCRL', [{ c: [322, 122, 38] }]),
      H_('Dent-1: ClC-5', 'Dent-1', [{ r: [426, 150, 172, 62] }]),
      H_('Nefropatik sistinozis: sistinozin', 'Nefropatik sistinozis', [{ c: [814, 134, 32] }])]
  };
  Object.keys(ELLE).forEach(function (id) { K[id] = function (svg) { hucre(svg, { hedef: ELLE[id] }); }; });
  K.s21_sxl = function (svg) { hucre(svg); };
  K.s21_rta = function (svg) {
    odak(svg, { hedef: [{ ad: 'Tip 1 · distal RTA', delik: [{ r: [3, 3, 354, 394] }] }, { ad: 'Tip 2 · proksimal RTA', delik: [{ r: [363, 3, 354, 394] }] }, { ad: 'Tip 4 · hiperkalemik RTA', delik: [{ r: [723, 3, 354, 394] }] }] });
  };
  ('x05_6 x05_9 x05_24 x06_4 x06_8 x06_10 x06_35 x07_5 x08_4 x08_6 x09_5 x09_9 x10_6 x11_6 x12_5 x13_4 x14_4 x16_4 x16_10 x19_4 x21_4 x21_5 ' +
   'x22_6 x23_4 x24_4 x24_12 x24_26 x25_4 x26_4 x28_4 x31_5 x32_6 x33_5 x34_5 x35_4 x36_6 x36_69 x37_4 x38_4 x39_4 x39_26 x39_68 x39_80 ' +
   'x40_8 x40_9 x40_10 x41_24 x42_5 x43_5 x43_22 x43_41 x44_5 x44_39 x44_48 x44_66 s21_oksalat s26_gir s26_kri').split(' ').forEach(function (id) { if (!K[id]) K[id] = function (svg) { kartlar(svg); }; });
  function kur(s) {
    if (!s || s.__etk || !K[s.id]) return;
    var svg = s.querySelector('svg'); if (!svg || !svg.getBBox().width) return;   // görünür olunca kurulur
    s.__etk = 1;
    try { K[s.id](svg); } catch (e) { if (window.console) console.warn('etk', s.id, e); }
  }
  function hepsi() { Object.keys(K).forEach(function (id) { kur(document.getElementById(id)); }); }
  var st = document.createElement('style');
  st.textContent = 'tr.etk-satir td{background:#fff1c2!important}.etk-perde{transition:opacity .25s}.etk-k [role=button]:focus{outline:none}' +
    '.etk-k [role=button]:focus-visible{stroke:#d9603b;stroke-width:3;stroke-opacity:1}@media (prefers-reduced-motion:reduce){.etk-perde{transition:none}}';
  document.head.appendChild(st);
  function basla() {
    hepsi();
    var deck = document.getElementById('deck') || document.body;
    if (window.MutationObserver) new MutationObserver(function (m) { m.forEach(function (x) { if (x.target.classList && x.target.classList.contains('on')) kur(x.target); }); })
      .observe(deck, { attributes: true, subtree: true, attributeFilter: ['class'] });
    window.addEventListener('resize', hepsi);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', basla); else basla();
})();
