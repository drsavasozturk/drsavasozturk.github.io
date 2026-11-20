#!/usr/bin/env python3
"""GK — Glomerül Kalıbı.
Taban: Prof. Öztürk'ün verdiği "Normal glomerüler yapı" görseli (yazıları temizlenmiş üç karo: yumak, lobul, bariyer).
Lezyonlar bu karoların ÜSTÜNE vektörle bindirilir; konumlar kalip.json ölçümünden gelir (elle koordinat verilmez).

Karo pikseli = ölçü birimi. Açılar ekran yönünde: 0 = sağ, 90 = aşağı, 180 = sol, 270 = yukarı.
  lobul  : kap 0 = üst kapiller (tam halka), kap 1 = sol alt, kap 2 = sağ alt (yarım görünür)
           yüz tipi 'dis' = podosite bakan çevresel duvar, 'mez' = mezangiyuma bakan duvar
  yumak  : merkez = Bowman kapsülü merkezi; damar kutbu ~270°, idrar (tübül) kutbu ~90°
"""
import json, math, os, random
from contextlib import contextmanager
from sekil_kit import *
from sekil_glom import etk, notrofil, monosit, eritrosit, elips
from shapely.geometry import Polygon, Point

_BURASI = os.path.dirname(os.path.abspath(__file__))
_KJ = next(p for p in (os.path.join(_BURASI, 'kalip', 'kalip.json'), '/home/claude/kalip/kalip.json') if os.path.exists(p))
KAL = json.load(open(_KJ))
KAL.setdefault('bariyer', {'w': 388, 'h': 312})
KOK = '/dersler/nefroloji-ders-serisi/gorsel/'      # yayında kök göreli yol. Önizlemede gk_onizle.py bunu file:// yapar.

GBM, GBM_K = '#ac80bb', '#76518f'
POD, POD_K = '#b9c7f3', '#5d659c'
MEZ, MEZ_H, MEZ_K = '#cadcb3', '#8eb46b', '#5f8a45'
ENDO, ENDO_K = '#fab6bd', '#d9606e'
CEK, CEK_K = '#7e62a8', '#523c78'
DEP, DEP_K = '#3a3148', '#1c1727'           # elektron yoğun birikim
SKL, SKL_K = '#c08aa3', '#8d5873'           # skleroz (PAS pembe)
FIB = '#e2476c'                             # fibrin / fibrinoid nekroz
KRS, KRS_K = '#e6d6f0', '#8a6aa8'           # kresent hücresi

# Etiket için hazır noktalar (karo pikseli)
NOKTA = {
    'lobul': {'podosit': (553, 87), 'pod_govde': (600, 150), 'mez_hucre': (382, 754), 'mez_hucre2': (448, 871), 'matriks': (560, 640),
              'eritrosit': (430, 475), 'lumen': (300, 330)},
    'yumak': {'afferent': (150, 58), 'efferent': (540, 58), 'tubul': (318, 760), 'yumak': (320, 406),
              'damar_kutbu': (318, 150), 'idrar_kutbu': (318, 672)},
    'bariyer': {'endotel': (150, 46), 'pencere': (190, 47), 'gbm': (190, 112), 'ayak': (150, 255), 'yarik': (200, 240), 'lumen': (190, 12), 'bowman': (238, 290)},
}


def _d(pts, kapali=True):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + (' Z' if kapali else '')


class GK:
    def __init__(s, F, ad, x, y, w, kirp=None, rx=12, cerceve=None):
        """ad: 'yumak' | 'lobul' | 'bariyer'.  (x, y) sol üst, w genişlik.  kirp=(x0, y0, x1, y1) karo pikselinde kesim."""
        T = KAL[ad]; s.F, s.ad, s.T = F, ad, T
        x0, y0, x1, y1 = kirp or (0, 0, T['w'], T['h'])
        s.x, s.y, s.k, s.x0, s.y0, s.x1, s.y1 = x, y, w / (x1 - x0), x0, y0, x1, y1
        s.w, s.h = w, (y1 - y0) * s.k
        s.cid = f'gk{F.fid}_{len(F.p)}'
        F.a(f'<clipPath id="{s.cid}"><rect x="{x:g}" y="{y:g}" width="{s.w:.1f}" height="{s.h:.1f}" rx="{rx:g}"/></clipPath>')
        F.a(f'<image href="{KOK}glom_{ad}.webp" x="{x - x0 * s.k:.2f}" y="{y - y0 * s.k:.2f}" width="{T["w"] * s.k:.2f}" height="{T["h"] * s.k:.2f}" '
            f'preserveAspectRatio="none" clip-path="url(#{s.cid})"/>')
        F.a(f'<filter id="{s.cid}b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{max(1.2, 5 * s.k):.1f}"/></filter>')
        if cerceve: F.r(x, y, s.w, s.h, 'none', cerceve, 1.4, rx)
        s.rg = random.Random(7); s._mzk = set()
        if ad == 'lobul':
            s.Y = [{y_['a']: (y_['ri'], y_['ro'], y_['t']) for y_ in kp['yuz']} for kp in T['kap']]
            s.C = [kp['c'] for kp in T['kap']]
        if ad == 'yumak':
            s.kc, s.kr = T['kapsul']['c'], T['kapsul']['r']; s.ki = s.kr - T['kapsul']['duvar'] - 3      # Bowman boşluğunun dış sınırı
            s.tuft = Polygon(T['yumak_kontur']).buffer(0)

    # ------------------------------------------------------------------ koordinat
    def xy(s, px, py=None):
        """Karo pikseli → şekil koordinatı."""
        if py is None: px, py = px
        return (s.x + (px - s.x0) * s.k, s.y + (py - s.y0) * s.k)

    def icinde(s, px, py, pay=0):
        return s.x0 + pay <= px <= s.x1 - pay and s.y0 + pay <= py <= s.y1 - pay

    @contextmanager
    def g(s, op=None):
        s.F.a(f'<g clip-path="url(#{s.cid})"' + (f' opacity="{op}"' if op else '') + '>')
        yield
        s.F.a('</g>')

    def R(s, kap, a):
        """(iç yüz yarıçapı, dış yüz yarıçapı, tip) — GBM'nin lümen ve podosit yüzleri."""
        Y = s.Y[kap]; a = a % 360; a0 = int(math.floor(a)) % 360; a1 = (a0 + 1) % 360
        if a0 in Y and a1 in Y:
            t = a - math.floor(a); return (Y[a0][0] * (1 - t) + Y[a1][0] * t, Y[a0][1] * (1 - t) + Y[a1][1] * t, Y[a0][2])
        for d in range(0, 9):
            for q in ((a0 - d) % 360, (a1 + d) % 360):
                if q in Y: return Y[q]
        return None

    def ri_tam(s, kap, a):
        """Lümen yüzü yarıçapı; ölçüm yoksa (karo dışında) çevre ölçümlerin ortancası. Lümeni dolduran çizimler için."""
        Y = s.Y[kap]; a = int(round(a)) % 360
        for d in range(0, 13):
            for q in ((a - d) % 360, (a + d) % 360):
                if q in Y: return Y[q][0]
        if not hasattr(s, '_rimed'): s._rimed = {}
        if kap not in s._rimed: s._rimed[kap] = sorted(v[0] for v in Y.values())[len(Y) // 2]
        return s._rimed[kap]

    def kp(s, kap, a, r):
        c = s.C[kap]; return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))

    def duvar(s, kap, a, kat='gbm'):
        """Duvardaki adlı katmanın karo pikseli. kat: lumen | endotel | subendo | gbm | subepi | ayak | podosit."""
        ri, ro, _ = s.R(kap, a)
        r = {'lumen': ri - 70, 'endotel': ri - 14, 'subendo': ri - 3, 'gbm': (ri + ro) / 2, 'subepi': ro + 5, 'ayak': ro + 26, 'podosit': ro + 62}[kat]
        return s.kp(kap, a, r)

    def acilar(s, kap, tip='dis', a0=None, a1=None):
        """Geçerli (ölçülmüş ve kesim içinde kalan) açıların sıralı listesi; a0→a1 saat yönünde."""
        if a0 is None: L = list(range(360))
        else:
            n = int((a1 - a0) % 360) or 360; L = [(a0 + i) % 360 for i in range(n + 1)]
        return [a for a in L if a in s.Y[kap] and (tip is None or s.Y[kap][a][2] == tip) and s.icinde(*s.kp(kap, a, s.Y[kap][a][1]), pay=4)]

    def dagit(s, kap, n, tip='dis', a0=None, a1=None, oyna=.25):
        """Duvar boyunca n adet, aralıklı ve hafif düzensiz açı seç."""
        L = s.acilar(kap, tip, a0, a1)
        if not L: return []
        ad_ = len(L) / n
        return [L[min(len(L) - 1, int(ad_ * (i + .5) + s.rg.uniform(-oyna, oyna) * ad_))] for i in range(n)]

    @staticmethod
    def aralar(A, enfazla=30):
        """Ardışık açıların orta noktaları (dikenleri birikimlerin arasına koymak için)."""
        return [A[i] + ((A[i + 1] - A[i]) % 360) / 2 for i in range(len(A) - 1) if 0 < (A[i + 1] - A[i]) % 360 <= enfazla]

    def _serit(s, kap, L, fi, fo):
        """L açı dizisi boyunca iki yarıçap işlevi arasındaki kapalı şerit (şekil koordinatı)."""
        ic, dis = [], []
        for i, a in enumerate(L):
            q = s.R(kap, a)
            if not q: continue
            t = i / max(1, len(L) - 1)
            ic.append(s.xy(s.kp(kap, a, fi(q[0], q[1], t)))); dis.append(s.xy(s.kp(kap, a, fo(q[0], q[1], t))))
        return ic + dis[::-1]

    def _kosular(s, kap, tip, a0, a1):
        """Geçerli açıları ardışık koşulara böl (ölçüm boşluğunda şerit kopsun)."""
        L = s.acilar(kap, tip, a0, a1); K, c = [], []
        for a in L:
            if c and (a - c[-1]) % 360 > 2: K.append(c); c = []
            c.append(a)
        if c: K.append(c)
        return [k_ for k_ in K if len(k_) >= 3]

    # ------------------------------------------------------------------ LOBÜL: birikimler
    def _kubbe(s, kap, a, gen, yuk, yon, renk, kenar, taban=1.0, op=None):
        n = 14; L = [a - gen / 2 + gen * i / n for i in range(n + 1)]
        if yon > 0: pts = s._serit(kap, L, lambda ri, ro, t: ro - taban, lambda ri, ro, t: ro + yuk * math.sin(math.pi * t) ** .7)
        else:       pts = s._serit(kap, L, lambda ri, ro, t: ri - yuk * math.sin(math.pi * t) ** .7, lambda ri, ro, t: ri + taban)
        s.F.yol(_d(pts), kenar, max(.6, 1.6 * s.k), renk, op=op)

    def subepitelyal(s, kap, A, gen=8, yuk=17, renk=DEP, kenar=DEP_K):
        """GBM'nin podosit yüzünde (dış yüz) kubbe biçimli birikimler. A: açı listesi (dagit ile seçilir)."""
        with s.g():
            for a in A: s._kubbe(kap, a, gen, yuk, +1, renk, kenar)

    def hump(s, kap, A, gen=13, yuk=34, renk=DEP, kenar=DEP_K):
        """İri subepitelyal 'hörgüç' (enfeksiyonla ilişkili GN)."""
        s.subepitelyal(kap, A, gen, yuk, renk, kenar)

    def diken(s, kap, A, yuk=24, gen=3.4):
        """Birikimlerin arasına uzanan GBM çıkıntıları (membranöz nefropati 'spike')."""
        with s.g():
            for a in A:
                q = s.R(kap, a)
                if not q or q[2] != 'dis': continue
                pts = [s.xy(s.kp(kap, a - gen / 2, q[1] - 2)), s.xy(s.kp(kap, a - gen * .18, q[1] + yuk)), s.xy(s.kp(kap, a + gen * .18, q[1] + yuk)), s.xy(s.kp(kap, a + gen / 2, q[1] - 2))]
                s.F.yol(_d(pts), GBM_K, max(.5, 1.1 * s.k), GBM)

    def subendotelyal(s, kap, A, gen=15, yuk=13, renk=DEP, kenar=DEP_K):
        """Endotel ile GBM arasında (GBM'nin lümen yüzü) uzun birikimler; endotel lümene doğru itilir."""
        with s.g():
            for a in A:
                n = 14; L = [a - gen / 2 - 1 + (gen + 2) * i / n for i in range(n + 1)]
                dud = s._serit(kap, L, lambda ri, ro, t: ri - 9 - (yuk + 1) * math.sin(math.pi * t) ** .7, lambda ri, ro, t: ri - 9 - (yuk + 1) * math.sin(math.pi * t) ** .7)
                s.F.yol(_d(dud[:n + 1], False), ENDO_K, max(2.4, 7 * s.k))                                     # itilen endotel
                s._kubbe(kap, a, gen, yuk, -1, renk, kenar)

    def intramembranoz(s, kap, a0, a1, pay=.26, renk=DEP, kenar=DEP_K, tip='dis'):
        """GBM'nin içinde kesintisiz yoğun bant (yoğun birikim hastalığı)."""
        with s.g():
            for L in s._kosular(kap, tip, a0, a1):
                pts = s._serit(kap, L, lambda ri, ro, t: ri + pay * (ro - ri), lambda ri, ro, t: ro - pay * (ro - ri))
                s.F.yol(_d(pts), kenar, max(.6, 1.4 * s.k), renk)

    def mez_noktalar(s, n, uzak=0):
        """Mezangiyum içinden daha önce kullanılmamış n nokta (karo pikseli)."""
        P = [tuple(p) for p in s.T['mez_nokta'] if s.icinde(p[0], p[1], 14) and tuple(p) not in s._mzk]
        s.rg.shuffle(P); sec = []
        for p in P:
            if all(math.hypot(p[0] - q[0], p[1] - q[1]) >= uzak for q in sec): sec.append(p)
            if len(sec) == n: break
        s._mzk.update(sec); return sec

    def mezangiyal(s, n=8, r=15, renk=DEP, kenar=DEP_K):
        """Mezangiyal matrikste birikimler."""
        P = s.mez_noktalar(n)
        with s.g():
            for p in P:
                x, y = s.xy(p); rr = r * s.k * s.rg.uniform(.8, 1.2)
                elips(s.F, x, y, rr, rr * s.rg.uniform(.55, .8), s.rg.uniform(0, 180), renk, kenar, max(.6, 1.4 * s.k))
        return P

    def paramezangiyal(s, kap=0, n=3, gen=12, yuk=13, renk=DEP, kenar=DEP_K):
        """Mezangiyuma bakan duvarda, GBM'nin altında birikimler (IgA nefropatisi için tipik yer)."""
        with s.g():
            A = s.dagit(kap, n, 'mez')
            for a in A: s._kubbe(kap, a, gen, yuk, +1, renk, kenar)
        return A

    # ------------------------------------------------------------------ LOBÜL: duvar değişiklikleri
    def silinme(s, kap, a0, a1, h=24, tip='dis'):
        """Ayaksı çıkıntı silinmesi: parmaklar tamamen örtülür; GBM'ye yapışık, kesintisiz, kalın podosit sitoplazması bandı."""
        with s.g():
            for L in s._kosular(kap, tip, a0, a1):
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ro + 1, lambda ri, ro, t: ro + 54)), None, 0, '#b3c1ef')
                d = _d(s._serit(kap, L, lambda ri, ro, t: ro + 40, lambda ri, ro, t: ro + 66))
                s.F.a(f'<path d="{d}" fill="#b3c1ef" filter="url(#{s.cid}b)"/>')
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ro + 1, lambda ri, ro, t: ro + h)), POD_K, max(.8, 1.9 * s.k), '#8597de')

    def gbm_kalin(s, kap, a0, a1, ic=6, dis=16, tip='dis'):
        """GBM kalınlaşması (her iki yüze doğru)."""
        with s.g():
            for L in s._kosular(kap, tip, a0, a1):
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - ic, lambda ri, ro, t: ro + dis)), GBM_K, max(.6, 1.5 * s.k), GBM)

    def lamel(s, kap, a0, a1, tip='dis'):
        """GBM'de lamelleşme / sepet örgüsü (Alport)."""
        with s.g():
            for L in s._kosular(kap, tip, a0, a1):
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - 3, lambda ri, ro, t: ro + 6)), None, 0, '#d9c3e6')
                for f, faz in ((.2, 0), (.5, 1.7), (.8, 3.1)):
                    pts = [s.xy(s.kp(kap, a, s.R(kap, a)[0] + (s.R(kap, a)[1] - s.R(kap, a)[0]) * (f + .22 * math.sin(i * .9 + faz)))) for i, a in enumerate(L)]
                    s.F.yol(_d(pts, False), GBM_K, max(.6, 1.6 * s.k))

    def cift_kontur(s, kap, a0, a1, d=20, tip='dis'):
        """Çift kontur ('tramvay rayı'): mezangiyal araya girme + endotel altında yeni GBM tabakası."""
        with s.g():
            for L in s._kosular(kap, tip, a0, a1):
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - d - 22, lambda ri, ro, t: ri - d - 6)), ENDO_K, max(.5, 1.1 * s.k), ENDO)   # endotel (içe itilmiş)
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - d, lambda ri, ro, t: ri + 1)), MEZ_K, max(.4, .9 * s.k), MEZ)              # araya giren mezangiyum
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - d - 9, lambda ri, ro, t: ri - d)), GBM_K, max(.5, 1.2 * s.k), '#9566b0')          # yeni GBM

    # ------------------------------------------------------------------ LOBÜL: hücreler
    def lumen_noktalar(s, kap, n, r=30):
        if not hasattr(s, '_lum'): s._lum = []
        P = []
        for _ in range(6000):
            a = s.rg.uniform(0, 360); q = s.R(kap, a)
            if not q: continue
            p = s.kp(kap, a, math.sqrt(s.rg.random()) * max(0, q[0] - 34 - r))
            if s.icinde(p[0], p[1], r + 2) and all(math.hypot(p[0] - u[0], p[1] - u[1]) > 2.1 * r for u in P + s._lum): P.append(p)
            if len(P) == n: break
        s._lum += P; return P

    def lumende(s, kap, tip='notrofil', n=3, r=30):
        """Kapiller lümeninde hücre: notrofil | monosit (endokapiller hiperselülarite)."""
        with s.g():
            P = s.lumen_noktalar(kap, n, r)
            for p in P:
                x, y = s.xy(p); (notrofil if tip == 'notrofil' else monosit)(s.F, x, y, r * s.k)
        return P

    def trombus(s, kap, renk=FIB):
        """Lümeni dolduran hiyalin / fibrin trombüs."""
        L = list(range(0, 360, 6))
        with s.g():
            s.F.yol(_d([s.xy(s.kp(kap, a, (s.ri_tam(kap, a) - 40) * (.9 + .06 * math.sin(a * .11)))) for a in L]), '#a82447', max(.6, 1.6 * s.k), renk, op=.93)

    def mez_hucre(s, n=3, r=30):
        """Ek mezangiyal hücreler (mezangiyal hiperselülarite)."""
        P = s.mez_noktalar(n, uzak=2.3 * r)
        with s.g():
            for p in P:
                x, y = s.xy(p); rr = r * s.k; ac = s.rg.uniform(0, 180)
                elips(s.F, x, y, rr * 1.25, rr * .8, ac, MEZ_H, MEZ_K, max(.6, 1.5 * s.k)); elips(s.F, x, y, rr * .62, rr * .44, ac, CEK, CEK_K, max(.5, 1.2 * s.k))
        return P

    def nodul(s, p, r=70):
        """Mezangiyal nodül (Kimmelstiel–Wilson): katmanlı, hücreden fakir matriks birikimi. p: karo pikseli."""
        x, y = s.xy(p); rr = r * s.k
        with s.g():
            s.F.el(x, y, rr, rr * .92, '#d9a9c6', SKL_K, max(.7, 1.8 * s.k))
            for f in (.72, .46, .22): s.F.el(x, y, rr * f, rr * f * .92, 'none', '#b77a9c', max(.5, 1.2 * s.k))

    def matriks_artisi(s, op=.5):
        """Mezangiyal matriks genişlemesi (PAS pembe ton)."""
        with s.g(): s.F.yol(_d([s.xy(p) for p in s.T['mez_kontur']]), None, 0, '#cf8fb3', op=op)

    # ------------------------------------------------------------------ YUMAK (bütün glomerül)
    def _dilim(s, a0, a1, r0, r1):
        if (a1 - a0) % 360 >= 358 or a1 - a0 >= 358: return Point(s.kc).buffer(r1).difference(Point(s.kc).buffer(r0)) if r0 > 0 else Point(s.kc).buffer(r1)
        n = max(2, int((a1 - a0) % 360) // 3); A = [a0 + ((a1 - a0) % 360) * i / n for i in range(n + 1)]
        pt = lambda a, r: (s.kc[0] + r * math.cos(math.radians(a)), s.kc[1] + r * math.sin(math.radians(a)))
        return Polygon([pt(a, r1) for a in A] + [pt(a, r0) for a in A[::-1]]).buffer(0)

    def _ciz(s, geo, kenar, sw, fill, op=None):
        for g_ in (geo.geoms if hasattr(geo, 'geoms') else [geo]):
            if g_.is_empty or g_.geom_type != 'Polygon': continue
            s.F.yol(_d([s.xy(p) for p in g_.exterior.coords]), kenar, sw, fill, op=op)

    def _sac(s, geo, aralik, pay=0):
        """Bölge içine aralıklı noktalar."""
        if geo.is_empty: return []
        x0, y0, x1, y1 = geo.bounds; P = []; ic = geo.buffer(-pay)
        for _ in range(6000):
            p = (s.rg.uniform(x0, x1), s.rg.uniform(y0, y1))
            if ic.contains(Point(p)) and all(math.hypot(p[0] - q[0], p[1] - q[1]) >= aralik for q in P): P.append(p)
        return P

    def kresent(s, a0, a1, tip='hucresel', bas=24):
        """Bowman boşluğunda kresent (a0→a1 saat yönünde). tip: hucresel | fibroz. bas: yumağı sıkıştırma payı (piksel)."""
        bolge = s._dilim(a0, a1, 0, s.ki).difference(s.tuft.buffer(-bas)).buffer(-9).buffer(9)
        with s.g():
            if tip == 'hucresel':
                s._ciz(bolge, KRS_K, max(.6, 1.4 * s.k), '#d9c4ea')
                for p in s._sac(bolge, 21, 9):
                    x, y = s.xy(p); ac = s.rg.uniform(0, 180)
                    elips(s.F, x, y, 11.5 * s.k, 8.5 * s.k, ac, KRS, KRS_K, max(.4, .9 * s.k)); elips(s.F, x, y, 5.2 * s.k, 3.8 * s.k, ac, CEK)
            elif tip == 'fibroselular':
                s._ciz(bolge, '#8a6aa8', max(.6, 1.4 * s.k), '#e3d3cf')
                for i, p in enumerate(s._sac(bolge, 22, 8)):
                    x, y = s.xy(p); ac = math.degrees(math.atan2(p[1] - s.kc[1], p[0] - s.kc[0])) + 90
                    if i % 2: elips(s.F, x, y, 11 * s.k, 8 * s.k, ac, KRS, KRS_K, max(.4, .9 * s.k)); elips(s.F, x, y, 5 * s.k, 3.6 * s.k, ac, CEK)
                    else: elips(s.F, x, y, 13 * s.k, 2.4 * s.k, ac, '#a98a62')
            else:
                s._ciz(bolge, '#9a7b54', max(.6, 1.4 * s.k), '#dcc7a2')
                for p in s._sac(bolge, 30, 8):
                    x, y = s.xy(p); ac = math.degrees(math.atan2(p[1] - s.kc[1], p[0] - s.kc[0])) + 90
                    elips(s.F, x, y, 13 * s.k, 2.2 * s.k, ac, '#a98a62');
                for p in s._sac(bolge, 70, 10):
                    x, y = s.xy(p); elips(s.F, x, y, 6 * s.k, 2.6 * s.k, math.degrees(math.atan2(p[1] - s.kc[1], p[0] - s.kc[0])) + 90, CEK)
        return bolge

    def tr(s, a):
        """Yumağın a açısındaki dış sınırının merkeze uzaklığı."""
        from shapely.geometry import LineString
        uc = (s.kc[0] + 400 * math.cos(math.radians(a)), s.kc[1] + 400 * math.sin(math.radians(a)))
        k_ = LineString([s.kc, uc]).intersection(s.tuft)
        P = [q for g_ in (k_.geoms if hasattr(k_, 'geoms') else [k_]) for q in g_.coords]
        return max(math.hypot(x - s.kc[0], y - s.kc[1]) for x, y in P)

    def skleroz(s, a0, a1, derin=.4, sinesi=True, hiyalin=2):
        """Segmental skleroz: yumağın a0→a1 arasındaki çevresel bölümü (derin: merkeze doğru derinlik, 0–1)."""
        acik = (a1 - a0) % 360; n = max(2, round(acik / 28)); D = []
        for i in range(n):
            a = a0 + acik * (i + .5) / n; R_ = s.tr(a); rr = R_ * derin * (.92 + .16 * ((i * 7) % 3) / 2)
            D.append(Point(s.kc[0] + (R_ - rr * .78) * math.cos(math.radians(a)), s.kc[1] + (R_ - rr * .78) * math.sin(math.radians(a))).buffer(rr))
        seg = D[0]
        for d_ in D[1:]: seg = seg.union(d_)
        seg = seg.buffer(14).buffer(-14).intersection(s.tuft.buffer(3)).buffer(-3).buffer(3)
        am = a0 + acik / 2
        with s.g():
            if sinesi:
                pt = lambda a, r: (s.kc[0] + r * math.cos(math.radians(a)), s.kc[1] + r * math.sin(math.radians(a))); t0 = s.tr(am) - 26
                kop = Polygon([pt(am - 10, t0), pt(am + 10, t0), pt(am + 4.5, s.ki + 5), pt(am - 4.5, s.ki + 5)])
                s._ciz(kop.buffer(10, join_style=1).buffer(-6, join_style=1), SKL_K, max(.7, 1.5 * s.k), SKL)
            s._ciz(seg, SKL_K, max(.7, 1.6 * s.k), SKL, op=.84)
            for p in s._sac(seg, 30, 12)[:12]:
                x, y = s.xy(p); ac = math.degrees(math.atan2(p[1] - s.kc[1], p[0] - s.kc[0])) + 90 + s.rg.uniform(-30, 30)
                s.F.yol(f'M{x - 15 * s.k * math.cos(math.radians(ac)):.1f},{y - 15 * s.k * math.sin(math.radians(ac)):.1f} q{6 * s.k:.1f},{-5 * s.k:.1f} {30 * s.k * math.cos(math.radians(ac)):.1f},{30 * s.k * math.sin(math.radians(ac)):.1f}', '#9c6682', max(.6, 1.5 * s.k))
            for p in s._sac(seg, 55, 20)[:hiyalin]:
                x, y = s.xy(p); s.F.el(x, y, 14 * s.k, 12 * s.k, '#f4bccf', '#b8587c', max(.5, 1.1 * s.k))
            for p in s._sac(seg, 48, 14)[:5]:
                x, y = s.xy(p); elips(s.F, x, y, 6 * s.k, 4 * s.k, s.rg.uniform(0, 180), CEK)
        return seg

    def global_skleroz(s):
        with s.g():
            s._ciz(s.tuft.buffer(-3), SKL_K, max(.7, 1.6 * s.k), SKL, op=.95)
            for p in s._sac(s.tuft, 44, 16):
                x, y = s.xy(p); elips(s.F, x, y, 17 * s.k, 2.6 * s.k, s.rg.uniform(0, 180), '#a56d88')

    def cekirdekler(s, n=40, a0=0, a1=359, r=10, renk=CEK):
        """Yumağa ek çekirdekler (hiperselülarite). a0→a1 ile bir dilime sınırlanabilir."""
        bolge = s.tuft.intersection(s._dilim(a0, a1, 0, s.kr))
        with s.g():
            for p in s._sac(bolge, 2.6 * r, r + 2)[:n]:
                x, y = s.xy(p); elips(s.F, x, y, r * s.k, r * .78 * s.k, s.rg.uniform(0, 180), renk, CEK_K, max(.4, .8 * s.k))

    def fibrinoid(s, a, uz=.7, r=34):
        """Fibrinoid nekroz odağı: yumakta a açısında, merkezden kenara uz (0–1) oranında."""
        R_ = s.tr(a); p = (s.kc[0] + R_ * uz * math.cos(math.radians(a)), s.kc[1] + R_ * uz * math.sin(math.radians(a)))
        T_ = [i * math.pi / 18 for i in range(36)]
        pts = [s.xy((p[0] + r * (1 + .14 * math.sin(3 * t + 1)) * math.cos(t), p[1] + r * .86 * (1 + .12 * math.cos(2 * t + .5)) * math.sin(t))) for t in T_]
        with s.g():
            s.F.yol(_d(pts), '#a31f44', max(.6, 1.4 * s.k), FIB, op=.9)
            for i in range(5):
                t = i * 1.3; x, y = s.xy((p[0] + r * .45 * math.cos(t), p[1] + r * .4 * math.sin(t))); s.F.el(x, y, 2.6 * s.k + .6, 2.6 * s.k + .6, '#7a1232')
        return p

    def kapsul(s, a, kat='duvar'):
        """Kapsülde adlı nokta: duvar (pariyetal epitel) | bosluk (Bowman boşluğu)."""
        r = {'duvar': s.kr - 14, 'bosluk': s.ki - 16}[kat]
        return (s.kc[0] + r * math.cos(math.radians(a)), s.kc[1] + r * math.sin(math.radians(a)))

    # ------------------------------------------------------------------ BARİYER (düz kesit: üstte endotel, ortada GBM, altta ayaksı çıkıntılar)
    BAR = {'endo': (28, 66), 'gbm': (76, 150), 'ayak': (152, 300), 'yarik_x': (92, 200, 265, 350)}

    def bar_birikim(s, yer, X, gen=34, yuk=20, renk=DEP, kenar=DEP_K):
        """yer: subepi (GBM altı, podosit yüzü) | subendo (GBM üstü, endotel yüzü) | intra (GBM içi). X: karo x listesi."""
        y0, y1 = s.BAR['gbm']
        with s.g():
            for x in X:
                if yer == 'intra':
                    px, py = s.xy(x, (y0 + y1) / 2); elips(s.F, px, py, gen * .75 * s.k, (y1 - y0) * .2 * s.k, 0, renk, kenar, max(.6, 1.4 * s.k)); continue
                yon = 1 if yer == 'subepi' else -1; yb = (y1 + 2) if yer == 'subepi' else (y0 - 2)
                pts = [s.xy(x - gen / 2 + gen * i / 14, yb + yon * yuk * math.sin(math.pi * i / 14) ** .7) for i in range(15)]
                s.F.yol(_d(pts), kenar, max(.6, 1.4 * s.k), renk)

    def bar_silinme(s, x0=0, x1=388, h=30):
        """Ayaksı çıkıntı silinmesi: yarıklar kapanır, GBM altında kesintisiz sitoplazma."""
        y1 = s.BAR['gbm'][1]
        with s.g():
            ax, ay = s.xy(x0, y1 + 3); bx, by = s.xy(x1, s.BAR['ayak'][1])
            s.F.a(f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{bx - ax:.1f}" height="{by - ay:.1f}" fill="#b4c4f2" filter="url(#{s.cid}b)"/>')
            s.F.r(ax, ay - 1, bx - ax, h * s.k, '#93a6ea', POD_K, max(.7, 1.6 * s.k), 0)

    # ------------------------------------------------------------------ EK İŞLEVLER (Opus, 19.11.2026)
    def yakin(s, L, p, boy=46, c=INK2):
        """Yumak küçük resminde p (karo pikseli) çevresine kutu, kutudan hedef GK çerçevesine kesikli çizgiler."""
        x, y = s.xy(p); b = boy * s.k / 2
        s.F.r(x - b, y - b, 2 * b, 2 * b, 'none', c, 1.3, 2)
        if L is None: return
        hx = L.x if L.x > x else L.x + L.w
        kx = x + b if L.x > x else x - b
        s.F.ln(kx, y - b, hx, L.y, c, 1.1, '4 3'); s.F.ln(kx, y + b, hx, L.y + L.h, c, 1.1, '4 3')

    def kose(s, w=50, p=(430, 330), boy=74):
        """Lobül karosunun boş sol üst köşesine yerini gösteren küçük bütün glomerül."""
        assert s.ad == 'lobul'
        s.F.r(s.x + 3, s.y + 3, w + 6, w * 1.2 + 6, '#fff', LINE, 1, 6)
        Y = GK(s.F, 'yumak', s.x + 6, s.y + 6, w, kirp=(40, 60, 640, 780)); Y.yakin(None, p, boy, RED); return Y

    def vakuol(s, n=4):
        """Podosit gövdesinde vakuoller."""
        P = [(500, 150), (566, 168), (628, 148), (590, 128), (532, 128)][:n]
        with s.g():
            for (px, py) in P:
                x, y = s.xy(px, py); s.F.el(x, y, 15 * s.k + 1.2, 12 * s.k + 1.2, '#ffffff', POD_K, max(.8, 1.6 * s.k))

    def mikrovillus(s, adim=2, boy=16):
        """Podositin Bowman boşluğuna bakan yüzünde mikrovillus dönüşümü (ince, sık çıkıntılar)."""
        K = [p for p in s.T['dis_kontur'] if p[1] < 820 and s.icinde(p[0], p[1], 10)]
        with s.g():
            for i in range(0, len(K) - 2, adim):
                (x0, y0), (x1, y1) = K[i], K[i + 2]
                dx, dy = x1 - x0, y1 - y0; L_ = math.hypot(dx, dy) or 1; nx, ny = dy / L_, -dx / L_      # dışa dik
                a, b = s.xy(x0, y0), s.xy(x0 + nx * boy, y0 + ny * boy)
                s.F.ln(a[0], a[1], b[0], b[1], POD_K, max(1.0, 3.2 * s.k))
                s.F.el(b[0], b[1], max(.7, 2.2 * s.k), max(.7, 2.2 * s.k), '#a9b8ee')

    def ayrilma(s, kap, a0, a1, hucre=True):
        """Podosit ayrılması: ayaksı çıkıntılar ve podosit kalkar, GBM çıplak kalır; ayrılan hücre Bowman boşluğunda."""
        with s.g():
            for L in s._kosular(kap, 'dis', a0, a1):
                d = _d(s._serit(kap, L, lambda ri, ro, t: ro + 1.5, lambda ri, ro, t: ro + 90 * math.sin(math.pi * t) ** .5 + 8))
                s.F.a(f'<path d="{d}" fill="#f7f8fa" filter="url(#{s.cid}b)"/>')
                s.F.yol(d, None, 0, '#f7f8fa')
                s.F.yol(_d([s.xy(s.kp(kap, a, s.R(kap, a)[1] + .5)) for a in L], False), GBM_K, max(.8, 2.2 * s.k))
            if hucre:
                am = a0 + ((a1 - a0) % 360) / 2; q = s.R(kap, am); x, y = s.xy(s.kp(kap, am, q[1] + 105))
                elips(s.F, x, y, 62 * s.k, 36 * s.k, am + 100, POD, POD_K, max(.8, 1.8 * s.k)); elips(s.F, x, y, 24 * s.k, 16 * s.k, am + 100, '#7e62a8')

    def endotel_sis(s, kap, a0=None, a1=None, kalin=38):
        """Endotel şişmesi: endotel lümene doğru kalınlaşır, lümen daralır."""
        with s.g():
            for L in s._kosular(kap, None, a0, a1) if a0 is not None else [list(range(0, 360))]:
                L = [a for a in L if s.R(kap, a)]
                s.F.yol(_d(s._serit(kap, L, lambda ri, ro, t: ri - kalin, lambda ri, ro, t: ri + 1)), ENDO_K, max(.5, 1.1 * s.k), '#f6a9b3')
            for a in range(10, 360, 40):
                q = s.R(kap, a)
                if q and s.icinde(*s.kp(kap, a, q[0] - kalin / 2), 6):
                    x, y = s.xy(s.kp(kap, a, q[0] - kalin / 2)); elips(s.F, x, y, 11 * s.k, 5 * s.k, a + 90, '#c45a6c')

    def tri(s, kap, a):
        """Tübüloretiküler inklüzyon: endotel sitoplazmasında küçük tübül kümesi. Döndürür: karo pikseli."""
        q = s.R(kap, a); p = s.kp(kap, a, q[0] - 26); x, y = s.xy(p); r = 21 * s.k + 1.2
        with s.g():
            s.F.el(x, y, r, r * .8, '#fdf3e3', '#7a4b2a', max(.5, 1.1 * s.k))
            for dx, dy in ((-.4, -.2), (.1, -.35), (.4, .1), (-.1, .3), (-.45, .25), (.3, .4)):
                s.F.el(x + dx * r, y + dy * r, r * .17, r * .17, 'none', '#7a4b2a', max(.4, .8 * s.k))
        return p

    def lipo(s, kap, katman=4):
        """Lipoprotein tıkacı: lümeni dolduran soluk, katmanlı (lameller) madde."""
        L = list(range(0, 360, 5))
        with s.g():
            for j in range(katman):
                f = 1 - j * .2
                pts = [s.xy(s.kp(kap, a, max(6, (s.ri_tam(kap, a) - 20) * f * (1 + .035 * math.sin(a * .09 + j))))) for a in L]
                s.F.yol(_d(pts), '#c9a75a', max(.5, 1.1 * s.k), ('#fbf0cf', '#f6e4b0', '#fbf0cf', '#f3dc9e')[j % 4], op=.97)

    def kriyo(s, kap):
        """Kriyoglobulin 'yalancı trombüsü': lümeni dolduran PAS pozitif, hiyalin görünümlü madde."""
        L = list(range(0, 360, 6))
        with s.g():
            s.F.yol(_d([s.xy(s.kp(kap, a, (s.ri_tam(kap, a) - 26) * (.78 + .1 * math.sin(a * .13)))) for a in L]), '#9c5d8a', max(.6, 1.5 * s.k), '#ecc8e0', op=.96)

    def cift_nokta(s, kap, a, kat='yeni_gbm', d=20):
        """cift_kontur katmanlarının karo pikseli: yeni_gbm | interpoz | endotel."""
        ri = s.R(kap, a)[0]; return s.kp(kap, a, {'yeni_gbm': ri - d - 4.5, 'interpoz': ri - d / 2, 'endotel': ri - d - 14}[kat])

    # ------------------------------------------------------------------ EK İŞLEVLER: yumak
    HILUS = (318, 178)

    def mez_agac(s, kalin=30, op=.72, cek=34):
        """Mezangiyal genişleme: damar kutbundan dallanan mezangiyal sapların kalınlaşması (lobüler görünüm)."""
        h = s.HILUS; m = (s.kc[0] + 2, s.kc[1] - 30); yollar = []
        for a in (150, 115, 80, 45, 10, 335, 205):
            R_ = s.tr(a); u = (s.kc[0] + R_ * .72 * math.cos(math.radians(a)), s.kc[1] + R_ * .72 * math.sin(math.radians(a)))
            o = ((m[0] + u[0]) / 2 + 22 * math.cos(math.radians(a + 90)), (m[1] + u[1]) / 2 + 22 * math.sin(math.radians(a + 90)))
            yollar.append((m, o, u))
        with s.g():
            d = f'M{s.xy(h)[0]:.1f},{s.xy(h)[1]:.1f} L{s.xy(m)[0]:.1f},{s.xy(m)[1]:.1f}'
            for (a_, o, u) in yollar:
                A, O, U = s.xy(a_), s.xy(o), s.xy(u); d += f' M{A[0]:.1f},{A[1]:.1f} Q{O[0]:.1f},{O[1]:.1f} {U[0]:.1f},{U[1]:.1f}'
            s.F.a(f'<path d="{d}" fill="none" stroke="#b8649a" stroke-width="{kalin * s.k:.1f}" stroke-linecap="round" opacity="{op}"/>')
            for (a_, o, u) in yollar:
                for t in (.35, .6, .85):
                    px = (1 - t) ** 2 * a_[0] + 2 * (1 - t) * t * o[0] + t * t * u[0]; py = (1 - t) ** 2 * a_[1] + 2 * (1 - t) * t * o[1] + t * t * u[1]
                    if cek: x, y = s.xy(px + s.rg.uniform(-6, 6), py + s.rg.uniform(-6, 6)); elips(s.F, x, y, 7 * s.k, 5.4 * s.k, s.rg.uniform(0, 180), CEK, CEK_K, max(.4, .8 * s.k))

    def lobuler(s, kalin=9, op=.8, renk='#a24a86', acilar=(150, 115, 80, 45, 10, 335, 205)):
        """Lobüler görünüm ve kalın kapiller duvar: her lobülün çevresel kapiller ilmeklerini kalın PAS pembe yay olarak vurgular (mez_agac ile birlikte kullan)."""
        from shapely.geometry import LineString
        with s.g():
            for a in acilar:
                R_ = s.tr(a); m = (s.kc[0] + R_ * .63 * math.cos(math.radians(a)), s.kc[1] + R_ * .63 * math.sin(math.radians(a))); r = R_ * .34
                yay = LineString([(m[0] + r * math.cos(math.radians(a + t)), m[1] + r * math.sin(math.radians(a + t))) for t in range(-105, 106, 7)]).intersection(s.tuft.buffer(-10).difference(Point(s.HILUS).buffer(95)))
                for g_ in (yay.geoms if hasattr(yay, 'geoms') else [yay]):
                    if g_.is_empty or g_.geom_type != 'LineString': continue
                    s.F.a(f'<path d="{_d([s.xy(p) for p in g_.coords], False)}" fill="none" stroke="{renk}" stroke-width="{kalin * s.k + .8:.1f}" stroke-linecap="round" opacity="{op}"/>')

    def kollaps(s, a0=0, a1=359, n=40, pod=None):
        """Kollapsing: yumak büzülür (kapiller lümenler kapanır, GBM kıvrılır), üstünü büyümüş ve çoğalmış podositler örter (yalancı kresent)."""
        from shapely import affinity
        bolge = s._dilim(a0, a1, 0, s.kr)
        cek = affinity.scale(s.tuft, .64, .64, origin=(s.kc[0] + 4, s.kc[1] + 6)).buffer(8).buffer(-8)
        hal = s.tuft.buffer(16).difference(cek.buffer(-2)).intersection(s._dilim(pod[0], pod[1], 0, s.kr) if pod else bolge).intersection(Point(s.kc).buffer(s.ki - 2))
        bos = s.tuft.buffer(16).difference(cek.buffer(-2)).difference(hal).intersection(Point(s.kc).buffer(s.ki - 2)) if pod else None
        with s.g():
            if bos is not None: s._ciz(bos.buffer(-1), None, 0, '#f3d8a4')
            s._ciz(hal, None, 0, '#e4e6f7', op=.95)
            s._ciz(cek.intersection(bolge), '#7a4a80', max(.7, 1.6 * s.k), '#b78bb7', op=.92)
            for p in s._sac(cek.intersection(bolge), 30, 12)[:24]:
                x, y = s.xy(p)
                s.F.yol(f'M{x - 14 * s.k:.1f},{y:.1f} q{7 * s.k:.1f},{-9 * s.k:.1f} {14 * s.k:.1f},0 t{14 * s.k:.1f},0', '#5e3366', max(.7, 2.0 * s.k))
            for p in s._sac(hal, 40, 9)[:n]:
                x, y = s.xy(p); ac = math.degrees(math.atan2(p[1] - s.kc[1], p[0] - s.kc[0])) + 90
                elips(s.F, x, y, 21 * s.k, 16 * s.k, ac, '#c3ccf3', POD_K, max(.6, 1.3 * s.k)); elips(s.F, x, y, 9 * s.k, 7.5 * s.k, ac, '#5f479a')
        return hal

    def kopuk(s, n=6, a0=0, a1=359, r=22):
        """Köpük hücreleri: lümende soluk, ince köpüklü sitoplazmalı makrofajlar."""
        bolge = s.tuft.intersection(s._dilim(a0, a1, 0, s.kr)).buffer(-10)
        P = s._sac(bolge, 3 * r, 4)[:n]
        with s.g():
            for p in P:
                x, y = s.xy(p); rr = r * s.k
                s.F.el(x, y, rr, rr * .9, '#fbf7ee', '#a08c6a', max(.5, 1.1 * s.k))
                for dx, dy in ((-.35, -.3), (.3, -.25), (0, .3), (-.3, .25), (.35, .25)): s.F.el(x + dx * rr, y + dy * rr, rr * .18, rr * .18, 'none', '#c2b08c', max(.3, .7 * s.k))
                s.F.el(x + .1 * rr, y - .05 * rr, rr * .22, rr * .2, '#6a5a8a')
        return P

    def hiyalinoz(s):
        """Arteriyolde hiyalinoz: afferent arteriyol duvarında camsı pembe birikim."""
        with s.g():
            for (px, py, r) in ((168, 66, 15), (205, 80, 15), (238, 104, 14), (262, 132, 13)):
                x, y = s.xy(px, py); s.F.el(x, y, r * s.k + .6, r * .7 * s.k + .6, '#f6c6da', '#b8587c', max(.5, 1.1 * s.k))
        return (205, 80)

    def noduller(s, n=6, r=46):
        """Yumakta mezangiyal nodüller (Kimmelstiel–Wilson benzeri). Döndürür: nodül merkezleri (karo pikseli)."""
        P = []
        for i in range(n):
            a = 200 + i * 360 / n; R_ = s.tr(a); P.append((s.kc[0] + R_ * .55 * math.cos(math.radians(a)), s.kc[1] + R_ * .55 * math.sin(math.radians(a))))
        for p in P: s.nodul(p, r)
        return P

    def kapsul_yirtik(s, a, gen=22):
        """Bowman kapsülünde yırtık; interstisyumdan fibroblast girişi."""
        bol = s._dilim(a - gen / 2, a + gen / 2, s.ki - 8, s.kr + 16)
        with s.g():
            s._ciz(bol, None, 0, '#f1e4d0')
            for i in range(5):
                t = -gen / 2 + gen * (i + .5) / 5; r = s.ki + (i % 3) * 12
                x, y = s.xy(s.kc[0] + r * math.cos(math.radians(a + t)), s.kc[1] + r * math.sin(math.radians(a + t)))
                elips(s.F, x, y, 13 * s.k, 2.8 * s.k, a + t + 8, '#9a7b54')

    def podosit_isaret(s, n=8, r=15):
        """Yumak yüzeyinde (kapiller ilmeklerin dış yüzü) n podosit işareti; damar kutbu dışlanır."""
        ic = s.tuft.buffer(-r * 1.6).difference(Point(s.HILUS).buffer(120)); P = []
        for i in range(n):
            a = 315 + i * 270 / (n - 1)
            R_ = s.tr(a) * .84
            while R_ > 20 and not ic.contains(Point(s.kc[0] + R_ * math.cos(math.radians(a)), s.kc[1] + R_ * math.sin(math.radians(a)))): R_ -= 4
            P.append((s.kc[0] + R_ * math.cos(math.radians(a)), s.kc[1] + R_ * math.sin(math.radians(a))))
        with s.g():
            for p in P:
                x, y = s.xy(p); rr = max(4.5, r * s.k)
                s.F.el(x, y, rr, rr * .82, '#e9e3ff', '#3b2a73', 1.6); s.F.el(x, y, rr * .45, rr * .38, '#3b2a73')
        return P

    def lokosit(s, n=14, a0=0, a1=359, r=13):
        """Kapiller lümenlerde lökosit (endokapiller hiperselülarite): soluk sitoplazma, koyu loblu çekirdek."""
        bolge = s.tuft.intersection(s._dilim(a0, a1, 0, s.kr)).buffer(-8).difference(Point(s.HILUS).buffer(80))
        P = s._sac(bolge, 2.4 * r, 4)[:n]
        with s.g():
            for p in P:
                x, y = s.xy(p); rr = max(2.6, r * s.k)
                s.F.el(x, y, rr, rr, '#f4f0fb', '#5b3f8a', max(.5, 1.1 * s.k))
                for dx, dy in ((-.32, -.1), (.08, .26), (.34, -.16)): s.F.el(x + dx * rr, y + dy * rr, rr * .3, rr * .26, '#3a2466')
        return P

    # ------------------------------------------------------------------ etiket
    def etiket(s, hedef, tx, ty, lines, sag=True, **k):
        """hedef: karo pikseli (px, py) ya da NOKTA anahtarı. (tx, ty) şekil koordinatında yazı başlangıcı."""
        p = NOKTA[s.ad][hedef] if isinstance(hedef, str) else hedef
        etk(s.F, s.xy(p), tx, ty, lines, sag, **k)
