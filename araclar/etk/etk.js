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
    x39_8: plazma, x43_43: perfuzyon, s21_avp: avp, x36_4: tasima
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
   'x40_8 x40_9 x40_10 x41_24 x42_5 x43_5 x43_22 x43_41 x44_5 x44_39 x44_48 x44_66 s21_oksalat').split(' ').forEach(function (id) { if (!K[id]) K[id] = function (svg) { kartlar(svg); }; });
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
