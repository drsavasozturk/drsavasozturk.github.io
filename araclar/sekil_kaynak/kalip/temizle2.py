#!/usr/bin/env python3
"""İkinci temizlik: yazı/çizgi silinen yerlerde kalan beyazımsı izleri gider (t_*_v1.png → t_*.png)."""
import cv2, numpy as np, json, math
u8 = lambda m: (m.astype(np.uint8) * 255)
def maskeli_bulanik(im, m, sig):
    f = m.astype(np.float32)[..., None]
    pay = cv2.GaussianBlur(im.astype(np.float32) * f, (0, 0), sig); payda = cv2.GaussianBlur(f[..., 0], (0, 0), sig)[..., None]
    return pay / np.maximum(payda, 1e-3)
# ---------- yumak: kapsül içinde beyaz olmaz → beyazımsı pikselleri çevreden doldur
im = cv2.imread('t_yumak_v1.png'); H, W = im.shape[:2]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); S = hsv[..., 1].astype(int); V = hsv[..., 2].astype(int)
yy, xx = np.mgrid[:H, :W]; ic = (np.hypot(xx - 318, yy - 406) < 286) | ((np.abs(xx - 318) < 62) & (yy > 600) & (yy < 770))
mk = u8(ic & (S < 46) & (V > 205)); mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); mk = cv2.dilate(mk, np.ones((7, 7), np.uint8))
print('yumak maske %', round(100 * (mk > 0).mean(), 2))
cv2.imwrite('t_yumak.png', cv2.inpaint(im, mk, 6, cv2.INPAINT_TELEA)); cv2.imwrite('mk2_yumak.png', mk)
# ---------- lobül: (a) lümenlerde yazı izi → maskeli bulanıklaştırma; (b) mezangiyumda beyaz leke → doldur
im = cv2.imread('t_lobul_v1.png'); H, W = im.shape[:2]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); h2 = hsv[..., 0].astype(int) * 2; S = hsv[..., 1].astype(int); V = hsv[..., 2].astype(int)
K = json.load(open('kalip.json'))['lobul']; yy, xx = np.mgrid[:H, :W]
lum = np.zeros((H, W), bool)
for kp in K['kap']:
    c = kp['c']; A = (np.degrees(np.arctan2(yy - c[1], xx - c[0])) % 360).astype(int); Rr = np.hypot(xx - c[0], yy - c[1])
    ri = np.full(360, np.nan)
    for y_ in kp['yuz']: ri[y_['a']] = y_['ri']
    ok = ~np.isnan(ri); ri = np.interp(np.arange(360), np.where(ok)[0], ri[ok], period=360)
    lum |= (Rr < ri[A] - 46) & (np.isin(A, np.where(ok)[0]))
duz = lum & (S < 150)                                   # eritrosit dışı lümen
duz = cv2.erode(u8(duz), np.ones((5, 5), np.uint8)) > 0
b = maskeli_bulanik(im, duz, 22); out = im.astype(np.float32)
agir = cv2.GaussianBlur(duz.astype(np.float32), (0, 0), 4)[..., None]
out = out * (1 - agir) + b * agir; out = np.clip(out, 0, 255).astype(np.uint8)
mz = np.zeros((H, W), np.uint8); cv2.drawContours(mz, [np.array(K['mez_kontur'])], -1, 255, -1); mz = cv2.dilate(mz, np.ones((31, 31), np.uint8))
mk = u8((mz > 0) & (S < 16) & (V > 236)); mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); mk = cv2.dilate(mk, np.ones((9, 9), np.uint8))
print('lobul mez maske %', round(100 * (mk > 0).mean(), 2))
yesil = (mz > 0) & (h2 >= 58) & (h2 <= 150) & (S >= 14) & (mk == 0)
dolgu = maskeli_bulanik(out, yesil, 26); agir = cv2.GaussianBlur((mk > 0).astype(np.float32), (0, 0), 5)[..., None]
out = np.clip(out.astype(np.float32) * (1 - agir) + dolgu * agir, 0, 255).astype(np.uint8)
cv2.imwrite('t_lobul.png', out)
# renk örnekleri: parmak (açık) ve parmak arası (gövde)
c = K['kap'][0]['c']; ac, ko = [], []
for y_ in K['kap'][0]['yuz']:
    if y_['t'] != 'dis': continue
    for r in range(int(y_['ro']) + 8, int(y_['ro']) + 40):
        x = int(c[0] + r * math.cos(math.radians(y_['a']))); y = int(c[1] + r * math.sin(math.radians(y_['a'])))
        if 0 <= x < W and 0 <= y < H and 190 <= h2[y, x] <= 250: (ac if V[y, x] > 232 else ko).append(im[y, x])
f = lambda L: '#%02x%02x%02x' % tuple(int(v) for v in np.median(np.array(L), axis=0)[::-1])
print('parmak', f(ac), len(ac), 'parmak arası', f(ko), len(ko))
