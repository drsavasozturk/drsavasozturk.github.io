#!/usr/bin/env python3
"""drsavasozturk.com · sunumlara ve atlaslara sahiplik ibaresi (19.11.2026, kullanıcı isteği).

Kullanım:  python3 -I imza_ekle.py <sunum.html | atlas.html> [...]     (tekrar çalıştırmak güvenlidir)

Atlaslarda (kapı kimliği yz…) yalnız giriş kapısına üçüncü onay kutusu (yzc3) eklenir; sayfa içine ibare konmaz.

Ne yapar:
  1. Giriş kapısına üçüncü onay kutusu (dk3) ekler: sunumun Prof. Dr. Savaş Öztürk'e ait olduğu,
     kaynak gösterilmeden ve izin alınmadan kullanılamayacağı. Üç kutu da işaretlenmeden sunum açılmaz.
  2. Her slaytın (section.slide) üst kenarına "Prof. Dr. Savaş Öztürk tarafından hazırlanmıştır" ibaresi koyar.
     Metin CSS içeriğidir; sesli anlatım okumaz, slayt içi arama ve ölçekleme etkilenmez.
"""
import re, sys

DK2 = '<label><input type="checkbox" id="dk2" autocomplete="off"> Yapay zekâ uyarısını okudum ve kabul ediyorum.</label>'
DK3 = ('<label><input type="checkbox" id="dk3" autocomplete="off"> Bu sunumun Prof. Dr. Savaş Öztürk tarafından hazırlandığını; '
       'kaynak gösterilmeden ve kendisinden izin alınmadan kopyalanamayacağını, çoğaltılamayacağını, değiştirilemeyeceğini '
       've başka bir ad altında sunulamayacağını kabul ediyorum. İzin için: savasozturkdr@gmail.com</label>')
JS_ESKI = [("C=[document.getElementById('dk1'),document.getElementById('dk2')]",
            "C=[document.getElementById('dk1'),document.getElementById('dk2'),document.getElementById('dk3')]"),
           ("b.disabled=!(C[0].checked&&C[1].checked);", "b.disabled=!C.every(function(c){return c.checked;});"),
           ("if(C[0].checked&&C[1].checked)kapat();", "if(C.every(function(c){return c.checked;}))kapat();")]
YZ2 = '<label><input type="checkbox" id="yzc2" autocomplete="off"> Yapay zekâ uyarısını okudum ve kabul ediyorum.</label>'
YZ3 = DK3.replace('id="dk3"', 'id="yzc3"').replace('Bu sunumun', 'Bu atlasın')
YZ_JS = [("C=[document.getElementById('yzc1'),document.getElementById('yzc2')]",
          "C=[document.getElementById('yzc1'),document.getElementById('yzc2'),document.getElementById('yzc3')]"),
         ("function hep(){return C[0].checked&&C[1].checked;}", "function hep(){return C.every(function(c){return c.checked;});}")]


def atlas(h):
    if 'id="yzc3"' not in h:
        assert h.count(YZ2) == 1, 'yzc2 etiketi bulunamadı'
        h = h.replace(YZ2, YZ2 + YZ3)
        for eski, yeni in YZ_JS:
            assert h.count(eski) == 1, eski
            h = h.replace(eski, yeni)
    return h


IMZA = '<i class="soimza" aria-hidden="true"></i>'
CSS = ('<style id="soimza-stil">.slide>.soimza{position:absolute;left:54px;top:10px;z-index:6;pointer-events:none;'
       'font:600 10.5px/1.5 "Source Sans 3","Segoe UI",system-ui,-apple-system,Arial,sans-serif;font-style:normal;letter-spacing:.02em;'
       'color:#4a5a66;background:rgba(255,255,255,.82);border-radius:999px;padding:1px 9px;white-space:nowrap;text-transform:none}'
       '.slide>.soimza::after{content:"Prof. Dr. Savaş Öztürk tarafından hazırlanmıştır"}'
       '@media print{.slide>.soimza{position:static;order:-1;align-self:flex-start;flex:none;margin:-24px 0 8px}}</style>')
# Yer: slaytların alt kenarında kaynak ve kısaltma dipnotları (.fn, .foot) bulunduğu için ibare üst kenarda durur.
#   Parenteral / İstatistik / Makale: sol üst (sağ üstte YZ notu var) · Nefroloji Ders Serisi ve aylık literatür: sağ üst.


def isle(h):
    if 'id="yzc2"' in h:               # atlas: yalnız kapı
        return atlas(h)
    # 1) kapı
    if 'id="dk3"' not in h:
        assert h.count(DK2) == 1, 'dk2 etiketi bulunamadı'
        h = h.replace(DK2, DK2 + DK3)
        for eski, yeni in JS_ESKI:
            assert h.count(eski) == 1, eski
            h = h.replace(eski, yeni)
    # 2) slayt ibaresi
    css = CSS
    if 'class="slide ek"' in h:        # Nefroloji Ders Serisi
        css = css.replace('</style>', '@media screen{.slide>.soimza{left:auto;right:54px;top:11px}}</style>')
    elif 'class="slide art"' in h:     # aylık literatür (dar ekranda akışkan düzen: kısa metin)
        css = css.replace('</style>', '@media screen{.slide>.soimza{left:auto;right:60px;top:12px}}'
                          '@media screen and (max-width:700px),screen and (max-height:500px){.slide>.soimza{right:10px;top:9px}'
                          '.slide>.soimza::after{content:"Prof. Dr. Savaş Öztürk tarafından hazırlanmıştır"}}</style>')
    h = re.sub(r'<style id="soimza-stil">.*?</style>', '', h, flags=re.S)
    i = h.index('</head>'); h = h[:i] + css + h[i:]
    if IMZA not in h:
        n_ac = len(re.findall(r'<section\b[^>]*\bclass="slide[ "]', h))
        assert n_ac == h.count('<section') == h.count('</section>') and n_ac > 0, (n_ac, h.count('<section'), h.count('</section>'))
        h = h.replace('</section>', IMZA + '</section>')
        assert h.count(IMZA) == n_ac
    return h


if __name__ == '__main__':
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8').read(); y = isle(t)
        if y != t: open(p, 'w', encoding='utf-8').write(y)
        print(p, 'değişti' if y != t else 'aynı', '| slayt ibaresi:', y.count(IMZA), '| dk3:', y.count('id="dk3"'), '| yzc3:', y.count('id="yzc3"'))
