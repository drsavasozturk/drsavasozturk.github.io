#!/usr/bin/env python3
"""Aktarılan metni kaynak belgedeki paragraf parmak izleriyle (sha256 ilk 8 hane) karşılaştırır.
Kullanım: python3 -I dogrula.py NN [NN ...]   (metin: ../metin/NN.md, izler: NN.h; izler Claude belgesindeki paragrafların h değerleridir)"""
import hashlib, re, sys
from pathlib import Path
K = Path(__file__).resolve().parent
def paragraflar(md):
    for s in md.splitlines():
        s = s.rstrip("\n")
        if not s.strip(): continue
        s = re.sub(r"^(#{1,3} |\d+\. |- )", "", s, count=1)
        yield s.replace("**", "")
def iz(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()[:8]
tamam = True
for no in sys.argv[1:]:
    no = int(no)
    kaynak = K.parent / "metin" if (K.parent / "metin").exists() else K.parent / "araclar" / "metin"
    ps = list(paragraflar((kaynak / f"{no:02d}.md").read_text(encoding="utf-8")))
    hs = [x.strip() for x in (K / f"{no:02d}.h").read_text().split() if x.strip()]
    bizim = [iz(p) for p in ps]
    if bizim == hs:
        print(f"{no:02d} TAMAM  {len(ps)} paragraf birebir"); continue
    tamam = False
    print(f"{no:02d} FARK  metin {len(ps)} paragraf, kaynak {len(hs)} iz")
    kume = set(hs)
    for i, (p, b) in enumerate(zip(ps, bizim)):
        if b not in kume: print(f"   uymayan #{i+1}: {p[:90]}")
    eksik = [h for h in hs if h not in set(bizim)]
    if eksik: print("   metinde karşılığı olmayan izler:", " ".join(eksik))
sys.exit(0 if tamam else 1)
