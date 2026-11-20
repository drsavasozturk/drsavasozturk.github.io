"""Şekil betiklerinde blok değiştirme yardımcıları (GK dönüşümü)."""
import re
def oku(p): return open(p, encoding='utf-8').read()
def yaz(p, s): open(p, 'w', encoding='utf-8').write(s)
def ice_al(p):
    s = oku(p)
    if 'from sekil_gk import *' not in s:
        s = s.replace('from sekil_ortak import *\n', 'from sekil_ortak import *\nfrom sekil_gk import *\n', 1); yaz(p, s)
def blok(p, fid, kod):
    """F = Fig('fid' satırından sonraki D.yeni/yeni/D.ic/ic çağrısına kadar olan bölümü değiştirir."""
    s = oku(p); m = re.search(r"^F = Fig\('%s'.*$" % re.escape(fid), s, re.M); assert m, fid
    n = re.search(r"^(D\.yeni|yeni|D\.ic|ic)\(", s[m.start():], re.M); assert n, fid
    s = s[:m.start()] + kod.strip('\n') + '\n' + s[m.start() + n.start():]; yaz(p, s)
def metin(p, eski, yeni):
    s = oku(p); assert s.count(eski) == 1, (p, eski[:60]); yaz(p, s.replace(eski, yeni))
