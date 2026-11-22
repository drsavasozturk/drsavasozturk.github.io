#!/usr/bin/env python3
"""drsavasozturk.com · ders sunumlarında tam ekranda alt çubukların gizlenmesi (22.11.2026).

Sorun: tam ekranda slayt bütün ekranı kaplıyor; alt gezinme çubuğu (#hud) ve kısayol satırı (#help)
yalnız soluklaşıyor, slaytın alt kısmının (kaynak satırı) üstünde kalıyordu.

Çözüm (motordan bağımsız, aynı #hud/#help kimliklerini kullanan bütün derslerde çalışır):
  - Tam ekranda (tam ekran düğmesi, F tuşu ya da tarayıcının F11 kipi) çubuklar 2 sn sonra tamamen gizlenir.
  - Fare ekranın alt kenarına (alt 110 piksel) ya da sol üstteki ana sayfa düğmesine gelince geri çıkar;
    çubuktan ayrıldıktan 2,5 sn sonra yine gizlenir. Dokunmatik ekranda dokununca 3,5 sn görünür.
  - Ok tuşları, tekerlek ve tıklama çubukları çağırmaz (sunum sırasında ekran temiz kalır).
  - Tam ekrandan çıkınca eski davranış (hareketsizlikte soluklaşma) sürer.
  - F11 kipinde de slayt bütün ekranı kullanır (fit işlevindeki tam ekran denetimi genişletilir).

Kullanım:  python3 -I araclar/tamekran.py dersler/<ad>/index.html [...]   (yineleme yapmaz; eski sürümü yenisiyle değiştirir)
ders_guncelle.py her aktarımın sonunda ekle() işlevini çağırır.
"""
import re, sys

BAS, SON = '<!--tamekran:bas-->', '<!--tamekran:son-->'

CSS = ("body.tekr #hud,body.tekr #help,body.tekr #dkev{transition:opacity .3s ease}"
       "body.tekr.cgizli #hud,body.tekr.cgizli #help,body.tekr.cgizli #dkev{opacity:0!important;pointer-events:none!important}")

JS = r"""(function(){
  var B=document.body;
  if(!document.getElementById('hud')||window.__tamEkran) return;
  var t=null, ince=!!(window.matchMedia&&matchMedia('(pointer:fine)').matches);
  function tam(){
    if(document.fullscreenElement||document.webkitFullscreenElement) return true;
    return ince&&innerWidth>=1000&&innerHeight>=600&&innerHeight>=screen.height-2&&innerWidth>=screen.width-2;
  }
  window.__tamEkran=tam;
  function gizle(){
    if(!B.classList.contains('tekr')) return;
    if(document.querySelector('#hud:hover,#help:hover,#dkev:hover')){ planla(1500); return; }
    B.classList.add('cgizli');
  }
  function planla(ms){ clearTimeout(t); t=setTimeout(gizle,ms); }
  function goster(ms){ B.classList.remove('cgizli'); planla(ms||2500); }
  function durum(){
    var f=tam(), d=B.classList.contains('tekr');
    if(f&&!d){ B.classList.add('tekr'); goster(2000); }
    else if(!f&&d){ B.classList.remove('tekr','cgizli'); clearTimeout(t); }
    else return;
    window.dispatchEvent(new Event('resize'));
  }
  document.addEventListener('fullscreenchange',function(){ setTimeout(durum,80); });
  document.addEventListener('webkitfullscreenchange',function(){ setTimeout(durum,80); });
  window.addEventListener('resize',function(){ setTimeout(durum,150); });
  document.addEventListener('mousemove',function(e){
    if(!B.classList.contains('tekr')) return;
    if(e.clientY>innerHeight-110||(e.clientY<60&&e.clientX<300)) goster(2500);
  },{passive:true});
  document.addEventListener('touchstart',function(){ if(B.classList.contains('tekr')) goster(3500); },{passive:true});
  durum();
})();"""

BLOK = f'{BAS}<style>{CSS}</style><script>{JS}</script>{SON}'

# fit(): F11 kipinde de slayt bütün ekranı kullansın (çubuklar zaten gizli)
FIT = [('if(w>=1000&&h>=600&&!document.fullscreenElement){',
        'if(w>=1000&&h>=600&&!(document.fullscreenElement||(window.__tamEkran&&window.__tamEkran()))){'),
       ('if(buyuk && !document.fullscreenElement){',
        'if(buyuk && !(document.fullscreenElement||(window.__tamEkran&&window.__tamEkran()))){')]


def ekle(h):
    if 'id="hud"' not in h:
        return h
    h = re.sub(re.escape(BAS) + r'.*?' + re.escape(SON), '', h, flags=re.S)
    for eski, yeni in FIT:
        h = h.replace(eski, yeni)
    i = h.rindex('</body>')
    return h[:i] + BLOK + '\n' + h[i:]


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    for yol in sys.argv[1:]:
        s = open(yol, encoding='utf-8').read(); y = ekle(s)
        if y != s: open(yol, 'w', encoding='utf-8').write(y)
        print(yol, '| blok:', y.count(BAS), '| fit yaması:', sum(y.count(b) for _, b in FIT))
