#!/usr/bin/env python3
"""GK önizleme: python3 gk_onizle.py kalip | lezyon  →  /home/claude/sekil_is/gor/gk_*.png"""
import sys
import sekil_gk as G
from sekil_gk import *
from playwright.sync_api import sync_playwright
G.KOK = 'file:///home/claude/kalip/'

def cek(F, out, w=1500, olcek=1.5):
    open('/home/claude/kalip/onizle.html', 'w', encoding='utf-8').write(f'<html><body style="margin:0;background:#fff;font-family:Inter,Arial,sans-serif"><div style="width:{w}px">{F.svg()}</div></body></html>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=olcek)
        pg.goto('file:///home/claude/kalip/onizle.html'); pg.wait_for_timeout(400)
        pg.locator('svg').first.screenshot(path=out); b.close()
    print(out, UYARI or '')

mod = sys.argv[1] if len(sys.argv) > 1 else 'kalip'
Z = '#f7f3ea'
if mod == 'kalip':
    F = Fig('kalip', 1330, 'Glomerül kalıbı', w=1000)
    F.r(4, 4, 992, 1322, Z, None, rx=14)
    F.t(500, 36, '1 · Bütün glomerül', 18, 800, BRANDD, 'middle')
    Y = GK(F, 'yumak', 265, 52, 470)
    Y.etiket('afferent', 245, 84, ['Afferent arteriyol'], sag=False, fs=14)
    Y.etiket('efferent', 755, 84, ['Efferent arteriyol'], fs=14)
    Y.etiket('damar_kutbu', 755, 150, ['Damar kutbu'], fs=14)
    Y.etiket(Y.kapsul(200, 'duvar'), 245, 250, ['Bowman kapsülü', 'pariyetal epitel'], sag=False, fs=14)
    Y.etiket(Y.kapsul(165, 'bosluk'), 245, 400, ['Bowman boşluğu'], sag=False, fs=14)
    Y.etiket((470, 330), 755, 300, ['Glomerül yumağı', 'kapiller halkalar', '+ podositler'], fs=14)
    Y.etiket('idrar_kutbu', 755, 500, ['İdrar kutbu'], fs=14)
    Y.etiket('tubul', 755, 584, ['Proksimal tübül', 'başlangıcı'], fs=14)
    F.t(500, 668, '2 · Lobül yakın planı', 18, 800, BRANDD, 'middle')
    L = GK(F, 'lobul', 215, 686, 600, cerceve=LINE)
    L.etiket('podosit', 830, 740, ['Podosit', 'viseral epitel'], fs=14)
    L.etiket(L.duvar(0, 330, 'ayak'), 830, 830, ['Ayaksı', 'çıkıntılar'], fs=14)
    L.etiket(L.duvar(0, 5, 'gbm'), 830, 920, ['Glomerül bazal', 'membranı'], fs=14)
    L.etiket(L.duvar(0, 25, 'endotel'), 830, 1000, ['Pencereli', 'endotel'], fs=14)
    L.etiket('lumen', 200, 800, ['Kapiller lümeni'], sag=False, fs=14)
    L.etiket('eritrosit', 200, 900, ['Eritrosit'], sag=False, fs=14)
    L.etiket('matriks', 830, 1090, ['Mezangiyal', 'matriks'], fs=14)
    L.etiket('mez_hucre2', 830, 1200, ['Mezangiyal', 'hücre'], fs=14)
    cek(F, '/home/claude/sekil_is/gor/gk_kalip.png', 1000, 1.3)
elif mod == 'lezyon':
    W, GEN, DY = 500, 468, 536
    F = Fig('lez', 4 * DY + 10, 'Kalıp üstünde lezyon örnekleri', w=2 * W + 12)
    F.r(4, 4, 2 * W + 4, 4 * DY + 2, Z, None, rx=14)
    def kutu(i, baslik, alt, ad='lobul', kirp=None):
        x, y = 22 + (i % 2) * W, 16 + (i // 2) * DY
        F.t(x + GEN / 2, y + 20, baslik, 16.5, 800, BRANDD, 'middle'); F.t(x + GEN / 2, y + 40, alt, 13, None, INK2, 'middle')
        return GK(F, ad, x, y + 50, GEN, kirp=kirp, cerceve=LINE)
    YK = (10, 60, 650, 700)
    g = kutu(0, 'Subepitelyal birikim + diken', 'membranöz nefropati')
    for k, n in ((0, 14), (1, 7), (2, 6)):
        A = g.dagit(k, n); g.subepitelyal(k, A); g.diken(k, g.aralar(A))
    g = kutu(1, 'Mezangiyal birikim + hücre artışı', 'IgA nefropatisi')
    g.mezangiyal(9); g.paramezangiyal(0, 3); g.mez_hucre(3)
    g = kutu(2, 'Subendotelyal birikim + çift kontur', 'membranoproliferatif patern')
    g.cift_kontur(0, 165, 262); g.subendotelyal(0, g.dagit(0, 4, 'dis', 280, 30)); g.subendotelyal(2, g.dagit(2, 3)); g.mez_hucre(3); g.mezangiyal(4)
    g = kutu(3, 'Hörgüç + lümende nötrofil', 'enfeksiyonla ilişkili GN')
    g.hump(0, g.dagit(0, 4)); g.hump(2, g.dagit(2, 2)); g.lumende(0, 'notrofil', 3); g.lumende(2, 'notrofil', 2); g.lumende(1, 'monosit', 1)
    g = kutu(4, 'Ayaksı çıkıntı silinmesi', 'minimal değişiklik hastalığı')
    g.silinme(0, 158, 36); g.silinme(1, 272, 80); g.silinme(2, 176, 303)
    g = kutu(5, 'İntramembranöz yoğun bant', 'yoğun birikim hastalığı')
    g.intramembranoz(0, 170, 30); g.intramembranoz(1, 280, 70); g.intramembranoz(2, 180, 300); g.mezangiyal(4, 12)
    g = kutu(6, 'Hücresel kresent + fibrinoid nekroz', 'kresentik GN', 'yumak', YK)
    g.kresent(305, 140); g.fibrinoid(30, .72)
    g = kutu(7, 'Segmental skleroz + sineşi', 'FSGS', 'yumak', YK)
    g.skleroz(118, 178)
    cek(F, '/home/claude/sekil_is/gor/gk_lezyon.png', 2 * W + 12, 1.0)
