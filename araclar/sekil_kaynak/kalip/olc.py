#!/usr/bin/env python3
"""Kalıp görselinin (kullanıcının ChatGPT ile ürettiği 'Normal glomerüler yapı') ölçümü.
Lobül karosunda her kapillerin merkezini ve açıya göre GBM iç/dış yüzünü çıkarır; mezangiyum ve podosit bölgelerini bulur.
Çıktı: kalip/kalip.json + kalip/olc_bak.png (denetim görüntüsü)."""
import cv2, numpy as np, math, json
im = cv2.imread('/home/claude/kalip/t_lobul.png'); Hh, Ww = im.shape[:2]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); h2 = hsv[:, :, 0].astype(int) * 2; S = hsv[:, :, 1].astype(int); V = hsv[:, :, 2].astype(int)
mor = (h2 >= 262) & (h2 <= 306) & (S >= 28) & (V >= 95) & (V <= 242)             # GBM
kirm = ((h2 <= 16) | (h2 >= 338)) & (S >= 38)                                      # lümen + endotel
mavi = (h2 >= 190) & (h2 <= 250) & (S >= 18)                                       # podosit
yesil = (h2 >= 58) & (h2 <= 150) & (S >= 22)                                       # mezangiyum
u8 = lambda m: (m.astype(np.uint8) * 255)
# kapiller lümenleri: büyük kırmızı bileşenler
k = cv2.morphologyEx(u8(kirm), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(k, 8)
bil = sorted([i for i in range(1, n)], key=lambda i: -st[i, cv2.CC_STAT_AREA])[:3]
def ic_nokta(i):
    d = cv2.distanceTransform(u8(lab == i), cv2.DIST_L2, 5); y, x = np.unravel_index(d.argmax(), d.shape); return (int(x), int(y), float(d.max()))
caps = sorted([ic_nokta(i) for i in bil], key=lambda c: (c[1] > 600, c[0]))   # üst, sol-alt, sağ-alt
print('kapiller merkezleri', caps)
def isin(c, a):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); r = 30; rin = None; say = 0
    while True:
        x, y = int(round(c[0] + r * ca)), int(round(c[1] + r * sa))
        if not (0 <= x < Ww and 0 <= y < Hh): return None
        if rin is None:
            say = say + 1 if mor[y, x] else 0
            if say >= 5: rin = r - 4; say = 0
        else:
            say = say + 1 if not mor[y, x] else 0
            if say >= 4:
                rout = r - 4
                if not (7 <= rout - rin <= 70): return None
                ny = {'dis': 0, 'mez': 0, 'gbm': 0, 'bos': 0}
                for q in range(rout + 5, rout + 34):
                    xx, yy = int(round(c[0] + q * ca)), int(round(c[1] + q * sa))
                    if not (0 <= xx < Ww and 0 <= yy < Hh): break
                    if mavi[yy, xx]: ny['dis'] += 1
                    elif yesil[yy, xx]: ny['mez'] += 1
                    elif mor[yy, xx]: ny['gbm'] += 1
                    else: ny['bos'] += 1
                return (rin, rout, max(ny, key=ny.get))
        r += 1
        if r > 700: return None
K = []
for c in caps:
    R = [isin(c, a) for a in range(360)]
    # ortanca süzgeç
    def suz(j, idx):
        v = [R[(j + d) % 360][idx] for d in range(-4, 5) if R[(j + d) % 360]]
        return float(np.median(v)) if len(v) >= 4 else None
    yuz = []
    for j in range(360):
        if R[j] and suz(j, 0) is not None: yuz.append({'a': j, 'ri': round(suz(j, 0), 1), 'ro': round(suz(j, 1), 1), 't': R[j][2]})
    K.append({'c': [c[0], c[1]], 'r_lumen': round(c[2], 1), 'yuz': yuz})
    print('kapiller', c[:2], 'geçerli açı', len(yuz), {t: sum(1 for y in yuz if y['t'] == t) for t in ('dis', 'mez', 'gbm', 'bos')}, 'GBM kalınlığı ortanca', np.median([y['ro'] - y['ri'] for y in yuz]))
# mezangiyum bölgesi ve örnek noktalar
mz = cv2.morphologyEx(u8(yesil), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)); mz = cv2.morphologyEx(mz, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(mz, 8); i = max(range(1, n), key=lambda i: st[i, cv2.CC_STAT_AREA]); mz = u8(lab == i)
d = cv2.distanceTransform(mz, cv2.DIST_L2, 5)
dolu_ = np.zeros_like(mz); c0, _ = cv2.findContours(mz, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(dolu_, c0, -1, 255, -1)
ic_mz = cv2.erode(dolu_, np.ones((41, 41), np.uint8))
cekirdek = cv2.morphologyEx(u8(((h2 >= 250) & (h2 <= 310) & (S >= 40)) & (ic_mz > 0)), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))       # mezangiyal hücre çekirdekleri (mor)
n2, lab2, st2, cen2 = cv2.connectedComponentsWithStats(cekirdek, 8)
mh = [[float(cen2[j][0]), float(cen2[j][1])] for j in range(1, n2) if st2[j, cv2.CC_STAT_AREA] > 900]
rng = np.random.RandomState(3); pts = []
ys, xs = np.where(d > 16)
for _ in range(4000):
    j = rng.randint(len(xs)); p = (int(xs[j]), int(ys[j]))
    if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 46 for q in pts) and all(math.hypot(p[0] - q[0], p[1] - q[1]) > 62 for q in mh): pts.append(p)
cnt, _ = cv2.findContours(mz, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cn = max(cnt, key=cv2.contourArea)
cn = cv2.approxPolyDP(cn, 2.5, True).reshape(-1, 2).tolist()
print('mezangiyum alanı', int((mz > 0).sum()), 'örnek nokta', len(pts), 'mezangiyal hücre çekirdeği', mh)
json.dump({'lobul': {'w': Ww, 'h': Hh, 'kap': K, 'mez_nokta': pts, 'mez_hucre': mh, 'mez_kontur': cn}}, open('/home/claude/kalip/kalip.json', 'w'))
# denetim görüntüsü
bak = im.copy()
for kp in K:
    c = kp['c']; cv2.circle(bak, tuple(c), 6, (0, 0, 0), -1)
    for y in kp['yuz']:
        ca, sa = math.cos(math.radians(y['a'])), math.sin(math.radians(y['a']))
        renk = {'dis': (255, 255, 0), 'mez': (0, 140, 255), 'gbm': (255, 0, 255), 'bos': (120, 120, 120)}[y['t']]
        cv2.circle(bak, (int(c[0] + y['ro'] * ca), int(c[1] + y['ro'] * sa)), 2, renk, -1)
        cv2.circle(bak, (int(c[0] + y['ri'] * ca), int(c[1] + y['ri'] * sa)), 2, (0, 255, 255), -1)
for p in pts: cv2.circle(bak, p, 7, (40, 40, 40), -1)
cv2.drawContours(bak, [np.array(cn)], -1, (0, 90, 0), 2)
cv2.imwrite('/home/claude/kalip/olc_bak.png', cv2.resize(bak, None, fx=.75, fy=.75))

# ================================================================= bütün glomerül karosu
im2 = cv2.imread('/home/claude/kalip/t_yumak.png'); H2, W2 = im2.shape[:2]
hs = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV); g2 = hs[:, :, 0].astype(int) * 2; S2 = hs[:, :, 1].astype(int); V2 = hs[:, :, 2].astype(int)
sari = (g2 >= 26) & (g2 <= 52) & (S2 >= 70) & (V2 >= 150)                                   # Bowman boşluğu (sarı-bej, doygun)
sr = cv2.morphologyEx(u8(sari), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
ys, xs = np.where(sr[:640] > 0)                                                               # tübül boynunun üstü
(cx, cy), rad = cv2.minEnclosingCircle(np.stack([xs, ys], 1).astype(np.float32))
print('kapsül iç daire', round(cx), round(cy), round(rad))
ic = np.zeros((H2, W2), np.uint8); cv2.circle(ic, (int(cx), int(cy)), int(rad) - 30, 255, -1)   # kapsül duvarı dışarıda kalsın
yum = ((ic > 0) & (sr == 0) & (S2 >= 45)).astype(np.uint8) * 255                              # kapsül içinde, sarı olmayan = yumak
yum = cv2.morphologyEx(cv2.morphologyEx(yum, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(yum, 8); i = max(range(1, n), key=lambda i: st[i, cv2.CC_STAT_AREA]); yum = u8(lab == i)
cnt, _ = cv2.findContours(yum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cy_ = max(cnt, key=cv2.contourArea)
yk = cv2.approxPolyDP(cy_, 2.0, True).reshape(-1, 2).tolist()
M = cv2.moments(cy_); tc = [M['m10'] / M['m00'], M['m01'] / M['m00']]
print('yumak alanı', int(cv2.contourArea(cy_)), 'merkez', [round(v) for v in tc], 'kontur noktası', len(yk))
D = json.load(open('/home/claude/kalip/kalip.json'))
D['yumak'] = {'w': W2, 'h': H2, 'kapsul': {'c': [float(cx), float(cy)], 'r': float(rad), 'duvar': 26.0}, 'yumak_kontur': yk, 'yumak_c': tc}
json.dump(D, open('/home/claude/kalip/kalip.json', 'w'))
b2 = im2.copy(); cv2.circle(b2, (int(cx), int(cy)), int(rad), (255, 0, 0), 2); cv2.drawContours(b2, [np.array(yk)], -1, (0, 255, 0), 2); cv2.circle(b2, (int(tc[0]), int(tc[1])), 6, (0, 0, 0), -1)
cv2.imwrite('/home/claude/kalip/olc_bak2.png', b2)
# karoları web için kaydet
from PIL import Image
for ad in ('lobul', 'yumak', 'bariyer'):
    Image.open(f'/home/claude/kalip/t_{ad}.png').save(f'/home/claude/kalip/glom_{ad}.webp', quality=88, method=6)
import os; print({ad: os.path.getsize(f'/home/claude/kalip/glom_{ad}.webp') // 1024 for ad in ('lobul', 'yumak', 'bariyer')}, 'KB')
