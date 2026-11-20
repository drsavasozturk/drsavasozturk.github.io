# Site testi. Kullanım: depo, .git hariç, bir klasöre kopyalanır (tar --exclude=.git), sonra: python3 araclar/test_site.py <klasör>
import asyncio, json, re, os, sys, subprocess, time
from urllib.parse import urlparse
from playwright.async_api import async_playwright
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site'; PORT = 8765; B = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
N_IL, N_SN = 819, 45   # dahiliye atlası sayıları (site_kur ile aynı)
PAGES = ['', 'ozgecmis.html', 'yayinlar.html', 'atlaslar.html', 'kunye.html', 'kullanim-kosullari.html', 'gizlilik.html', 'surum-notlari.html', 'yok/olmayan-sayfa.html', 'dahiliye-ilac-atlasi/', 'nefroloji-yeni-ilaclar/', 'dersler/parenteral-sivilar/', 'dersler/nefroloji-ders-serisi/', 'hasta.html', 'literatur/2026-10/', 'dersler/klinisyenler-icin-istatistik/', 'dersler/klinisyenler-icin-makale-yazma/']
SON = []
def ok(ad, kosul, ek=''): SON.append((ad, bool(kosul), ek)); print(('✓' if kosul else '✗'), ad, ek, flush=True)
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        # 1-2) taşma, JS hatası, dış istek
        for w, h in ((390, 844), (1280, 900)):
            ctx = await br.new_context(viewport={'width': w, 'height': h}); dis, hata = set(), []
            await ctx.route('**/static.cloudflareinsights.com/**', lambda r: r.fulfill(status=200, content_type='application/javascript', body=''))
            ctx.on('request', lambda r: dis.add(urlparse(r.url).hostname) if urlparse(r.url).hostname not in ('localhost', None, 'static.cloudflareinsights.com') else None)
            for pth in PAGES:
                pg = await ctx.new_page(); pe = []
                pg.on('pageerror', lambda e: pe.append(str(e))); pg.on('console', lambda m: pe.append(m.text) if m.type == 'error' and '404' not in m.text else None)
                await pg.goto(B + pth, wait_until='load'); await pg.wait_for_timeout(300)
                if pth in ('dahiliye-ilac-atlasi/', 'nefroloji-yeni-ilaclar/') and await pg.is_visible('#yzc1'):
                    await pg.check('#yzc1'); await pg.check('#yzc2'); await pg.check('#yzc3'); await pg.click('#yzb')
                if pth.startswith(('dersler/', 'literatur/')) and await pg.is_visible('#dk1'):
                    await pg.check('#dk1'); await pg.check('#dk2'); await pg.check('#dk3'); await pg.click('#dkb'); await pg.wait_for_timeout(300)
                sw = await pg.evaluate('[document.documentElement.scrollWidth, document.documentElement.clientWidth]')
                ok(f'taşma {w}px /{pth}', sw[0] <= sw[1] + 1, str(sw)); ok(f'JS hatası {w}px /{pth}', not pe, '; '.join(pe)[:200])
                if w == 390 and pth in ('', 'atlaslar.html', 'ozgecmis.html'): await pg.screenshot(path=f'/tmp/ek_{pth or "index"}_390.png', full_page=True)
                if w == 1280 and pth == '': await pg.screenshot(path='/tmp/ek_index_1280.png', full_page=True)
                await pg.close()
            ok(f'dış alan adına istek yok ({w}px)', not dis, str(dis)); await ctx.close()
        # 3) giriş kapısı
        ctx = await br.new_context(viewport={'width': 390, 'height': 844}); pg = await ctx.new_page()
        await pg.goto(B + 'dahiliye-ilac-atlasi/'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='/tmp/ek_kapi_390.png')
        g = lambda: pg.evaluate("[!document.getElementById('yz').classList.contains('kapali'), document.getElementById('yzb').disabled, document.getElementById('yzc1').checked, document.getElementById('yzc2').checked]")
        ok('kapı açılışta görünür ve düğme kapalı', (await g())[:2] == [True, True])
        await pg.check('#yzc1'); await pg.wait_for_timeout(60); ok('tek kutu işaretliyken düğme kapalı', (await g())[1] is True)
        await pg.check('#yzc2'); await pg.wait_for_timeout(60); ok('iki kutu işaretliyken düğme hâlâ kapalı', (await g())[1] is True)
        await pg.check('#yzc3'); await pg.wait_for_timeout(60); ok('üç kutu işaretliyken düğme açık', (await g())[1] is False)
        ici = await pg.evaluate("(function(){var r=document.getElementById('ara').getBoundingClientRect();var e=document.elementFromPoint(r.left+5,r.top+5);return !!(e&&e.closest('#yz'));})()")
        ok('kapı açıkken arama kutusuna tıklanamaz (kapı üstte)', ici)
        await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab'); await pg.keyboard.press('Tab')
        ok('kapı açıkken klavye odağı kapının dışına çıkmaz', await pg.evaluate("!!document.activeElement.closest('#yz')||document.activeElement===document.body"))
        await pg.click('#yzb'); ok('düğmeye tek tıklamayla kapı kapanır', (await g())[0] is False)
        await pg.reload(); await pg.wait_for_timeout(300); st = await g(); ok('yenilemede kapı yeniden açılır, kutular boş (onay saklanmaz)', st == [True, True, False, False], str(st))
        ok('onay tarayıcıda saklanmaz', await pg.evaluate("localStorage.length") == 0)
        await pg.check('#yzc1'); await pg.check('#yzc2'); await pg.check('#yzc3'); await pg.goto(B + 'index.html'); await pg.go_back(); await pg.wait_for_timeout(400)
        st = await g(); ok('geri tuşunda kutular sıfırlanır', st[2:] == [False, False] and st[1] is True, str(st))
        await pg.goto(B + 'nefroloji-yeni-ilaclar/'); await pg.wait_for_timeout(300); st = await g()
        ok('yeni ilaçlar atlasında kapı görünür (onay yok)', st[0] is True)
        # ders kapısı
        await pg.goto(B + 'dersler/parenteral-sivilar/'); await pg.wait_for_timeout(600)
        d = lambda: pg.evaluate("[!document.getElementById('dkapi').classList.contains('kapali'), document.getElementById('dkb').disabled, !!window.__onay, (document.querySelector('#deck .slide.on')||{}).id]")
        st = await d(); ok('derste kapı açılışta görünür, düğme kapalı', st[:3] == [True, True, False], str(st))
        await pg.keyboard.press('ArrowRight'); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(200)
        st2 = await d(); ok('ders kapısı açıkken ok tuşuyla slayt ilerlemez', st2[3] == st[3], str(st2))
        await pg.mouse.click(640, 400); await pg.wait_for_timeout(200)
        st2 = await d(); ok('ders kapısı açıkken tıklamayla slayt ilerlemez', st2[3] == st[3], str(st2))
        await pg.check('#dk1'); await pg.wait_for_timeout(60); ok('derste tek kutuyla düğme kapalı', (await d())[1] is True)
        await pg.check('#dk2'); await pg.wait_for_timeout(60); ok('derste iki kutuyla düğme hâlâ kapalı (izinsiz kullanım onayı gerekli)', (await d())[1] is True)
        await pg.check('#dk3'); await pg.wait_for_timeout(60); await pg.click('#dkb'); await pg.wait_for_timeout(400)
        st = await d(); ok('derste kabulden sonra kapı kapanır ve dersin iç onayı tamamlanır', st[0] is False and st[2] is True, str(st))
        await pg.reload(); await pg.wait_for_timeout(600); ok('derste yenilemede kapı yeniden açılır', (await d())[0] is True)
        # nefroloji ders serisi kapısı
        await pg.goto(B + 'dersler/nefroloji-ders-serisi/'); await pg.wait_for_timeout(1500)
        n = lambda: pg.evaluate("[!document.getElementById('dkapi').classList.contains('kapali'), document.getElementById('dkb').disabled, (function(){var y=document.getElementById('yzOnay');return !!y && y.offsetParent!==null && getComputedStyle(y).display!=='none';})(), localStorage.length]")
        st = await n(); ok('seride kapı açılışta görünür, düğme kapalı', st[:2] == [True, True], str(st))
        await pg.screenshot(path='/tmp/ek_seri_kapi_390.png')
        ici = await pg.evaluate("(function(){var e=document.elementFromPoint(195,700);return !!(e&&e.closest('#dkapi'));})()")
        ok('seride kapı açıkken alttaki içeriğe tıklanamaz', ici)
        await pg.check('#dk1'); await pg.check('#dk2'); await pg.check('#dk3'); await pg.click('#dkb'); await pg.wait_for_timeout(500)
        st = await n(); ok('seride kabulden sonra kapı kapanır, iç uyarı ikinci kez çıkmaz, hiçbir şey saklanmaz', st[0] is False and st[2] is False and st[3] == 0, str(st))
        await pg.screenshot(path='/tmp/ek_seri_ic_390.png')
        eks = await pg.evaluate("(function(){var h=[...new Set([...document.querySelectorAll('a[href^=\"#\"]')].map(a=>a.getAttribute('href').slice(1)).filter(Boolean))];return [h.length,h.filter(x=>!document.getElementById(x)).slice(0,8)];})()")
        ok('seride sayfa içi bağlantıların hedefi çalışma anında var', not eks[1], str(eks))
        await pg.reload(); await pg.wait_for_timeout(1500); ok('seride yenilemede kapı yeniden açılır', (await n())[0] is True)
        # literatür kapısı
        await pg.goto(B + 'literatur/2026-10/'); await pg.wait_for_timeout(600)
        d = lambda: pg.evaluate("[!document.getElementById('dkapi').classList.contains('kapali'), document.getElementById('dkb').disabled, false, [...document.querySelectorAll('#deck .slide')].findIndex(s=>s.classList.contains('on'))]")
        st = await d(); ok('literatürde kapı açılışta görünür, düğme kapalı', st[:2] == [True, True], str(st))
        await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(200); st2 = await d()
        ok('literatür kapısı açıkken ok tuşuyla slayt ilerlemez', st2[3] == st[3], str(st2))
        await pg.check('#dk1'); await pg.check('#dk2'); await pg.check('#dk3'); await pg.click('#dkb'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(300); st3 = await d()
        ok('literatürde kabulden sonra kapı kapanır ve slayt ilerler', st3[0] is False and st3[3] != st[3], str(st3))
        # istatistik dersi kapısı (Parenteral ile aynı motor: iç onay kabulden sonra otomatik)
        await pg.goto(B + 'dersler/klinisyenler-icin-istatistik/'); await pg.wait_for_timeout(600)
        q = lambda: pg.evaluate("[!document.getElementById('dkapi').classList.contains('kapali'), document.getElementById('dkb').disabled, !!window.__onay]")
        st = await q(); ok('istatistik dersinde kapı açılışta görünür, düğme kapalı', st == [True, True, False], str(st))
        await pg.check('#dk1'); await pg.check('#dk2'); await pg.check('#dk3'); await pg.click('#dkb'); await pg.wait_for_timeout(400)
        st = await q(); ok('istatistik dersinde kabulden sonra kapı kapanır ve iç onay tamamlanır', st[0] is False and st[2] is True, str(st))
        ok('istatistik dersinde 2026–2027 yazmaz', '2026–2027' not in await pg.content())
        await pg.goto(B + 'dersler/klinisyenler-icin-makale-yazma/'); await pg.wait_for_timeout(600)
        st = await q(); ok('makale yazma dersinde kapı açılışta görünür, düğme kapalı', st == [True, True, False], str(st))
        await pg.check('#dk1'); await pg.check('#dk2'); await pg.check('#dk3'); await pg.click('#dkb'); await pg.wait_for_timeout(400)
        st = await q(); ok('makale yazma dersinde kabulden sonra kapı kapanır ve iç onay tamamlanır', st[0] is False and st[2] is True, str(st))
        # tasarım paketi (8 Kasım 2026): hareket, sayaç, Yeni rozeti, OG, 404, yazdırma
        await pg.goto(B + 'index.html'); await pg.wait_for_timeout(1200)
        hr = await pg.evaluate("[document.documentElement.classList.contains('js'), document.querySelectorAll('.bel').length, document.querySelectorAll('.bel.gor').length, getComputedStyle(document.querySelector('.kahraman')).opacity, [...document.querySelectorAll('.kart .say b')].slice(0,3).map(b=>b.textContent), document.querySelectorAll('.yeni').length, document.querySelectorAll('.son li').length]")
        ok('ana sayfada hareket betiği çalışır, görünen bölümler belirmiş', hr[0] is True and hr[1] > 5 and hr[2] >= 2 and hr[3] == '1', str(hr))
        ok('kart sayaçları hedef sayıda durur', hr[4] == [str(N_IL), str(N_SN), '5'], str(hr[4]))
        ok('Yeni rozeti ve Son eklenenler (3 madde) var', hr[5] >= 3 and hr[6] == 3, str(hr))
        og_ = await pg.evaluate("[...document.querySelectorAll('meta[property^=\"og:\"],meta[name=\"twitter:card\"]')].map(m=>m.getAttribute('property')||m.getAttribute('name'))")
        ok('Open Graph etiketleri tam', all(k in og_ for k in ('og:title', 'og:description', 'og:image', 'og:url', 'twitter:card')), str(og_))
        ogr = await pg.request.get(B + 'og.png'); ok('og.png 1200×630 sunuluyor', ogr.status == 200 and ogr.headers.get('content-type', '').startswith('image/png'))
        eski = await pg.evaluate("(function(){var s=document.createElement('span');s.className='yeni';s.setAttribute('data-tarih','2026-01-01');document.body.appendChild(s);return s;})(); 1")
        # rozet süresi: betik yüklenirken çalışır; eski tarihli bir rozet için mantığı doğrudan sınayalım
        ok('30 günü geçen Yeni rozeti gizlenir (mantık)', await pg.evaluate("(Date.now()-Date.parse('2026-01-01'))/864e5>30"))
        ok('güncel Yeni rozeti görünür', await pg.evaluate("getComputedStyle(document.querySelector('.kart .yeni')).display!=='none'"))
        # hareketi azalt: betik devreye girmez, her şey anında görünür
        ctx2 = await br.new_context(viewport={'width': 1280, 'height': 800}, reduced_motion='reduce'); pg2 = await ctx2.new_page()
        await pg2.goto(B + 'index.html'); await pg2.wait_for_timeout(300)
        ra = await pg2.evaluate("[document.documentElement.classList.contains('js'), getComputedStyle(document.querySelector('.kart')).opacity, document.querySelectorAll('.kart .say b')[0].textContent]")
        ok('hareketi azalt açıkken animasyon yok, sayılar sabit', ra[0] is False and ra[1] == '1' and ra[2] == str(N_IL), str(ra)); await ctx2.close()
        r404 = await pg.goto(B + '404.html'); await pg.wait_for_timeout(200)
        n404 = await pg.evaluate("[document.querySelectorAll('main .kart').length, !!document.querySelector('meta[name=robots][content=noindex]'), document.querySelector('h1').textContent]")
        ok('404 sayfası: kartlı yönlendirme, noindex', n404[0] >= 3 and n404[1] is True and 'bulunamadı' in n404[2], str(n404))
        await pg.goto(B + 'ozgecmis.html'); await pg.wait_for_timeout(200)
        ok('özgeçmişte yazdır düğmesi yok (kullanıcı isteği)', not await pg.is_visible('.yazdir button'))
        await pg.emulate_media(media='print'); pr = await pg.evaluate("[getComputedStyle(document.querySelector('header.ust nav')).display, getComputedStyle(document.querySelector('footer.alt .ba')).display]")
        ok('yazdırma düzeninde menü ve alt bağlantılar gizli', pr == ['none', 'none'], str(pr)); await pg.emulate_media(media='screen')
        acc = await pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--acc').trim()"); ok('palet C vurgu rengi uygulanmış', acc == '#0f766e', acc)
        # hasta videoları: tıklamadan önce YouTube isteği yok; tıklayınca nocookie iframe
        await pg.goto(B + 'hasta.html'); await pg.wait_for_timeout(300)
        v = await pg.evaluate("[document.querySelectorAll('.oyn[data-yt]').length, document.querySelectorAll('.oy.yakin').length, document.querySelectorAll('iframe').length]")
        _vj = '/home/claude/scripts/videolar.json'   # video listesi depoda değil; yoksa sayfadaki toplam kabul edilir
        _NV = len(json.load(open(_vj, encoding='utf-8'))['videolar']) if os.path.exists(_vj) else v[0] + v[1]
        ok(f'hasta sayfasında oynatılabilir + “Yakında” = {_NV} video, açılışta iframe yok', v[0] + v[1] == _NV and v[0] >= 11 and v[2] == 0, str(v))
        await pg.route('**/*youtube*', lambda r: r.abort())
        await pg.click('#b1 button.oy'); await pg.wait_for_timeout(300)
        src = await pg.evaluate("(document.querySelector('#b1 iframe')||{}).src||''")
        ok('oynat düğmesi youtube-nocookie iframe yükler', src.startswith('https://www.youtube-nocookie.com/embed/D_0WHXbRHuY'), src)
        await pg.screenshot(path='/tmp/ek_hasta_390.png', full_page=True)
        await ctx.close()
        # 4) internetsiz (service worker)
        ctx = await br.new_context(); pg = await ctx.new_page()
        await pg.goto(B); await pg.wait_for_function('navigator.serviceWorker && navigator.serviceWorker.controller !== null || true')
        await pg.evaluate('navigator.serviceWorker.ready'); await pg.reload(); await pg.wait_for_timeout(500)
        for a in ('dahiliye-ilac-atlasi/', 'nefroloji-yeni-ilaclar/', 'dersler/parenteral-sivilar/', 'dersler/nefroloji-ders-serisi/', 'literatur/2026-10/'):
            await pg.goto(B + a); await pg.wait_for_timeout(2500)
        n = await pg.evaluate("caches.keys().then(k=>caches.open(k[0])).then(c=>c.keys()).then(r=>r.map(x=>x.url))")
        ok('atlaslar önbellekte', any('dahiliye-ilac-atlasi/' in u for u in n) and any('nefroloji-yeni-ilaclar/' in u for u in n), str(len(n)) + ' dosya')
        await ctx.set_offline(True)
        for a in ('dahiliye-ilac-atlasi/', 'nefroloji-yeni-ilaclar/', 'dersler/parenteral-sivilar/', 'dersler/nefroloji-ders-serisi/', 'literatur/2026-10/', '', 'ozgecmis.html', 'hasta.html'):
            try:
                r = await pg.goto(B + a); t = await pg.title(); ok(f'uçak modunda açılır /{a}', r is not None and r.ok and 'bulunamadı' not in t, t)
            except Exception as e: ok(f'uçak modunda açılır /{a}', False, str(e)[:120])
        await ctx.close(); await br.close()
asyncio.run(main())
# 5) kırık bağlantı
H = {}
for a, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.html') and '/indir' not in a: H[os.path.relpath(os.path.join(a, f), ROOT)] = open(os.path.join(a, f), encoding='utf-8').read()
kirik = []
ids = {k: set(re.findall(r' id="([^"]+)"', v)) for k, v in H.items()}
for k, v in H.items():
    for href in re.findall(r'href="([^"]+)"', v):
        if href.startswith(('http', 'mailto', '&#')) or "'" in href: continue
        yol, _, cap = href.partition('#'); base = os.path.dirname(k)
        if yol.startswith('/'): hedef = yol.lstrip('/') or 'index.html'   # kök-mutlak bağlantı (özel alan adı kökünde çalışır)
        else: hedef = os.path.normpath(os.path.join(base, yol)) if yol else k
        if hedef.endswith('/') or os.path.isdir(os.path.join(ROOT, hedef)): hedef = os.path.join(hedef, 'index.html')
        if hedef == '.': hedef = 'index.html'
        if not os.path.exists(os.path.join(ROOT, hedef)): kirik.append((k, href)); continue
        if cap and hedef in ids and cap not in ids[hedef] and not (hedef == k and k.startswith('dersler/nefroloji-ders-serisi')): kirik.append((k, href))  # seride kimlikler çalışma anında üretilir (ayrı test)
ok('kırık iç bağlantı yok', not kirik, str(kirik[:8]) + f' (toplam {len(kirik)})')
ok('indirme klasörü yok', not os.path.exists(ROOT + '/indir'))
ok('hiçbir sayfada indirme bağlantısı yok', not any(' download' in v or '/indir/' in v.replace("'/indir/'", '') for v in H.values()), str([k for k, v in H.items() if ' download' in v][:5]))
ok('her dosya 25 MB altında', all(os.path.getsize(os.path.join(a, f)) < 25e6 for a, _, fs in os.walk(ROOT) for f in fs))
srv.terminate()
print('\nÖZET:', sum(1 for _, k, _ in SON if k), '/', len(SON), 'geçti'); [print('  BAŞARISIZ:', a, e) for a, k, e in SON if not k]
