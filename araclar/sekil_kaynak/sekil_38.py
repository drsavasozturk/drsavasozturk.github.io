#!/usr/bin/env python3
"""Ders 38 · Hemodiyaliz damar erişimi — şekil tanımları (21 Kasım 2026). Resimler ChatGPT ile çizildi (yazısız); etiketler vektör."""
from sekil_ortak import *
import sekil_anat as AN

D = Ders('38')


def isaret(F, p, n, c=RED, dx=-16, dy=-16):
    """Darlık işareti: halkalı nokta + numara rozeti."""
    F.el(p[0], p[1], 12, 12, 'none', '#fff', 4.6, op=.9); F.el(p[0], p[1], 12, 12, 'none', c, 2.4)
    q = (p[0] + dx, p[1] + dy); F.el(q[0], q[1], 10, 10, c, '#fff', 1.6); F.t(q[0], q[1] + 4.2, str(n), 12, 800, '#fff', 'middle')


def madde_no(F, x, y, n, bas, satir, c=RED, w=230):
    F.el(x + 10, y - 4, 10, 10, c, '#fff', 1.4); F.t(x + 10, y + .2, str(n), 12, 800, '#fff', 'middle')
    F.t(x + 26, y, bas, 12.6, 800, INK)
    for i, s in enumerate(satir): F.t(x + 26, y + 17 + i * 15.5, s, 11.6, None, INK2)


# ============================================================================================== A · darlığın tipik yerleri
F = Fig('dar', 372, 'Damar erişiminde darlığın tipik yerleri: juksta-anastomotik ven, sefalik kemer, santral ven ve greftte venöz anastomoz', w=1080)
serit(F, 6, 6, 750, 'Fistül ve venöz çıkış yolu', BRAND); serit(F, 766, 6, 308, 'Greft', GOLD)
zemin(F, 6, 40, 750, 326); zemin(F, 766, 40, 308, 326)
S = 736 / 1538                                   # resim: ChatGPT ile çizildi (1538 × 520 px; sol kol, bilekte radiyosefalik fistül)
AN.resim(F, 'an_dar', 12, 42, 736, oran=520 / 1538)
def AP(px, py): return (12 + px * S, 42 + (py - 40) * S)
isaret(F, AP(1138, 366), 1, dx=-20, dy=20); isaret(F, AP(565, 193), 2, dx=16, dy=-18); isaret(F, AP(330, 282), 3, dx=22, dy=-14)
AN.ad(F, *AP(1262, 438), 'anastomoz', 10.6, '#7a2a20', 'middle', 700)
AN.ad(F, *AP(900, 300), 'sefalik ven', 10.6, '#2b4fa0', 'middle', 700)
AN.ad(F, *AP(212, 470), 'VKS', 10.6, '#2b4fa0', 'middle', 700)
madde_no(F, 16, 312, 1, 'Juksta-anastomotik ven', ['radiyosefalik AVF’de en sık;', 'olgunlaşmamanın başlıca nedeni'])
madde_no(F, 262, 312, 2, 'Sefalik kemer', ['brakiyosefalik AVF’de tipik', '(aksiller vene katıldığı kavis)'])
madde_no(F, 508, 312, 3, 'Santral ven', ['subklavyen, brakiyosefalik;', 'kateter öyküsü, kolda ödem'])
GW = 292                                         # greft resmi: Ders 38, üç erişim tipi şeklindeki uç-yan anastomozlu PTFE halka
AN.resim(F, 'an_eri1', 774, 50, GW, oran=188 / 486)
def GP(fx, fy): return (774 + fx * GW, 50 + fy * GW * 188 / 486)
isaret(F, GP(.1297, .4255), 4, c=GOLD, dx=-4, dy=-20)
AN.ad(F, *GP(.13, .86), 'arteriyel anastomoz', 10.4, '#7a2a20', 'start', 700)
madde_no(F, 776, 210, 4, 'Venöz anastomoz', ['greft darlığının en sık yeri;', 'neointimal hiperplazi'], c=GOLD)
F.tl(776, 280, ['Tromboz çoğunlukla bu darlıkların', 'sonucudur: pıhtı temizlenirken altta', 'yatan darlık da aynı seansta açılır.'], 11.6, 16, fill=INK, fw=700)
D.yeni('s38_dar', 'x38_16', 'Darlık · Şekil', 'Darlık Nerede Gelişir?', F,
       '<b>Okuma:</b> Radiyosefalik fistülde darlık en sık anastomozun hemen ardındaki venöz segmentte (juksta-anastomotik) gelişir ve olgunlaşmamanın başlıca nedenidir. '
       'Brakiyosefalik fistülde sefalik kemer, kateter öyküsü olan hastada santral venler (subklavyen, brakiyosefalik) tipik yerlerdir. Greftte darlık en sık venöz anastomozdadır.',
       'Şekil: solda göğüs ve yana açılmış sol kol; bilekte radiyosefalik fistül, genişlemiş sefalik ven omuza çıkıp sefalik kemer yaparak subklavyen vene, oradan brakiyosefalik ven ve vena kava süperiora ulaşıyor. '
       'Numaralı halkalar: 1 anastomozun hemen ardındaki ven, 2 sefalik kemer, 3 brakiyosefalik ven. Sağda ön kolda PTFE halka greft; 4 numara venöz anastomozu gösteriyor.')




# ============================================================================================== B · endovasküler fistül (hareketli)
F = Fig('eav', 430, 'Endovasküler arteriyovenöz fistül: komşu ülnar arter ve vende hizalanan kateterler, radyofrekans enerjisiyle anastomoz ve arteriyelleşen yüzeyel ven', w=1080)
ES = 344 / 500; EX = (12, 368, 724)              # resimler: ChatGPT ile çizildi (yazısız; her biri 500 × 450 px)
def EP(j, px, py): return (EX[j] + px * ES, 44 + py * ES)
BAS = (('1 · Kateterler karşı karşıya', BRAND), ('2 · Radyofrekans enerjisi', GOLD), ('3 · Anastomoz: akım yüzeye çıkar', PUR))
for j, (b, c) in enumerate(BAS):
    serit(F, EX[j], 6, 344, b, c)
    F.a(f'<g data-etk="e{j}">')
    F.a(f'<clipPath id="eav_k{j}"><rect x="{EX[j]}" y="44" width="344" height="{450 * ES:.1f}" rx="10"/></clipPath>')
    F.a(f'<image href="/dersler/nefroloji-ders-serisi/gorsel/an_eav{j}.webp" x="{EX[j]}" y="44" width="344" height="{450 * ES:.1f}" clip-path="url(#eav_k{j})" preserveAspectRatio="none"/>')
    if j == 0:
        AN.ad(F, *EP(0, 420, 318), 'ülnar arter', 11, '#7a2a20'); AN.ad(F, *EP(0, 420, 252), 'ülnar ven', 11, '#2b4fa0')
        AN.ad(F, *EP(0, 400, 124), 'yüzeyel ven', 11, '#2b4fa0'); AN.ad(F, *EP(0, 330, 196), 'perforan ven', 10.6, '#2b4fa0', 'start')
        AN.cagri(F, EP(0, 270, 288), EX[0] + 150, 378, ['mıknatıslı uçlar hizalanır'], fs=11.4, renk='#56677a')
    elif j == 1:
        AN.cagri(F, EP(1, 282, 288), EX[1] + 160, 378, ['iki duvar arasında kanal açılır'], fs=11.4, c='#8a5a00', renk='#8a5a00')
    else:
        AN.cagri(F, EP(2, 262, 292), EX[2] + 150, 378, ['arter → ven anastomozu'], fs=11.4, c=PUR, renk=PUR)
        AN.ad(F, *EP(2, 400, 124), 'yüzeyel ven: kanülasyon', 10.8, PUR); AN.ad(F, *EP(2, 340, 196), 'perforan ven', 10.6, PUR, 'start')
    F.a('</g>')
F.a('<path data-etk="ak1" d="M%s" fill="none" stroke="none"/>' % ' L'.join('%.1f,%.1f' % EP(2, *q) for q in ((60, 322), (200, 320), (255, 314), (262, 290), (250, 264), (120, 262), (55, 262))))
F.a('<path data-etk="ak2" d="M%s" fill="none" stroke="none"/>' % ' L'.join('%.1f,%.1f' % EP(2, *q) for q in ((60, 322), (200, 320), (255, 314), (275, 280), (286, 240), (288, 180), (290, 140), (260, 128), (150, 128), (60, 132))))
F.a('<circle data-etk="kv" cx="%.1f" cy="%.1f" r="1" fill="none"/>' % EP(1, 282, 288))
F.tl(12, 410, ['Cilt kesisi yapılmadan, floroskopi eşliğinde ön kolun derin damarları arasında oluşturulur; akım perforan ven yoluyla yüzeyel vene çıkar ve iğneleme orada yapılır.'], 11.6, 16, fill=INK2)
D.yeni('s38_eav', 'x38_17', 'Endovasküler Fistül · Şekil', 'Endovasküler Fistül — Üç Adımda', F,
       '<b>Okuma:</b> Ön kolda komşu seyreden ülnar arter ve vene birer kateter yerleştirilir; uçlardaki mıknatıslar kateterleri karşı karşıya hizalar. '
       'Radyofrekans enerjisi iki damar duvarı arasında kanal açar ve anastomoz oluşur. Arteriyel kan perforan ven aracılığıyla yüzeyel venlere çıkar; yüzeyel ven genişler ve iğneleme orada yapılır.',
       'Şekil: ön kolun yarı saydam kesitinde üç aşama. Birincide ülnar arter ve ülnar vende iki kateter, uçları karşı karşıya. İkincide uçlar arasında radyofrekans enerjisi parıltısı. '
       'Üçüncüde kateterler çekilmiş, arter ile ven arasında kısa bir anastomoz var; derin ven, perforan ven ve yüzeyel ven genişlemiş ve arteriyelleşmiş. Dokununca aşamalar sırayla öne çıkar ve akım yolu gösterilir.')


# ============================================================================================== C · çalma sendromu (HAIDI)
F = Fig('cal', 352, 'Erişime bağlı distal iskemi (çalma sendromu): yeterli distal perfüzyon ile soluk, siyanotik el karşılaştırması', w=1080)
CK = 520 / 746; CX, CO = (12, 548), (12, 780)    # resimler: ChatGPT ile çizildi (yazısız; her biri 746 × 300 px)
def CP(j, px, py): return (CX[j] + (px - CO[j]) * CK, 44 + (py - 240) * CK)
serit(F, 12, 6, 520, 'Yeterli distal perfüzyon', GREEN); serit(F, 548, 6, 520, 'Erişime bağlı distal iskemi (HAIDI)', RED)
for j in range(2):
    AN.resim(F, f'an_cal{j}', CX[j], 44, 520, oran=300 / 746)
AN.ad(F, *CP(0, 200, 318), 'sefalik ven (fistül)', 11, '#2b4fa0')
AN.cagri(F, CP(0, 415, 425), 300, 274, ['anastomoz'], fs=11.4, c='#7a2a20', renk='#7a2a20')
AN.ad(F, *CP(0, 600, 470), 'pembe, sıcak el', 11, '#7a2a20')
AN.ad(F, *CP(1, 950, 318), 'genişlemiş, yüksek akımlı fistül', 11, '#2b4fa0')
AN.cagri(F, CP(1, 1480, 470), 950, 274, ['soluk, soğuk el;', 'siyanotik parmak uçları'], fs=11.4, c=RED, renk=RED)
AN.cagri(F, CP(1, 1270, 410), 760, 274, ['distal yatağa', 'akım yetmez'], fs=11.4, c='#7a2a20', renk='#7a2a20')
F.r(12, 302, 1056, 44, '#f2f5f8', LINE, 1.2, 10)
F.t(26, 320, ['Evreler: ', ('I', 'b'), ' soluk–soğuk, yakınma yok · ', ('II', 'b'), ' yalnız diyalizde ağrı ya da uyuşma · ', ('III', 'b'), ' istirahatte ağrı · ', ('IV', 'b'), ' ülser, nekroz'], 11.8, None, INK)
F.t(26, 338, 'Distal radiyal arterde ters akım fistüllerde sıktır; tek başına tanı koydurmaz. Tanı klinik bulgu ve distal perfüzyon ölçümüyle konur.', 11.4, None, INK2)
D.yeni('s38_cal', 'x38_25', 'Komplikasyon · Şekil', 'Çalma Sendromu — El Neden Soluk?', F,
       '<b>Okuma:</b> Erişim arteriyel kanı düşük dirençli venöz yatağa yönlendirir. Distal arteriyel yatak bu kaybı karşılayamazsa el iskemik kalır: soluk ve soğuk el, siyanotik parmak uçları, diyalizde artan ağrı. '
       'Distal radiyal arterde ters akım birçok fistülde görülür ve tek başına tanı değildir; tanı klinik ve distal perfüzyon ölçümüyle konur.',
       'Şekil: iki panel, avuç yukarı ön kol ve el, bilekte radiyosefalik fistül. Solda el pembe, parmak arterleri dolgun. Sağda fistül ve sefalik ven daha geniş; el soluk, parmak uçları morumsu, parmak arterleri ince. Altta dört klinik evre.')


# ============================================================================================== D · santral ven darlığı
F = Fig('svd', 356, 'Santral ven darlığı: sol brakiyosefalik vende darlık, erişim kolunda ödem ve göğüs duvarında kollateral venler', w=1080)
VK = 740 / 1538                                  # resim: ChatGPT ile çizildi (yazısız; 1538 × 620 px; erişim kolu resmin sağında, hastanın solu)
def VP(px, py): return (12 + px * VK, 44 + py * VK)
serit(F, 12, 6, 740, 'Erişim tarafında santral darlık', BRAND); serit(F, 764, 6, 304, 'Klinik ve tanı', RED)
AN.resim(F, 'an_svd', 12, 44, 740, oran=620 / 1538)
isaret(F, VP(786, 168), 1, dx=22, dy=-16); isaret(F, VP(905, 245), 2, c='#2b4fa0', dx=20, dy=-18); isaret(F, VP(1135, 315), 3, c='#7a2a20', dx=24, dy=-12)
AN.ad(F, *VP(676, 226), 'VKS', 10.6, '#2b4fa0', 'end')
AN.ad(F, *VP(300, 520), 'karşı kol normal', 10.8, INK2)
zemin(F, 764, 40, 304, 310)
madde_no(F, 776, 66, 1, 'Brakiyosefalik ven darlığı', ['darlığın erişim tarafında', 'venler genişler'])
madde_no(F, 776, 124, 2, 'Göğüs duvarı kollateralleri', ['kan darlığın çevresinden döner'], c='#2b4fa0')
madde_no(F, 776, 166, 3, 'Erişim tarafında ödem', ['kol, meme, yüz; yüksek venöz', 'basınç, uzayan iğne yeri kanaması'], c='#7a2a20')
F.t(778, 236, 'Tanı: venografi (altın standart);', 11.6, 800, BRANDD); F.t(778, 252, 'BT ya da MR venografi', 11.6, None, INK)
F.t(778, 276, 'Risk: kateter sayısı ve süresi', 11.6, 800, RED); F.t(778, 292, '(subklavyen girişim en riskli)', 11.6, None, INK)
F.tl(778, 318, ['Kateter dururken darlık sessiz kalabilir;', 'erişim açılıp akım artınca belirti verir.'], 11.2, 15, fill=INK2, fw=700)
D.yeni('s38_svd', 'x38_26', 'Komplikasyon · Şekil', 'Santral Ven Darlığı — Nasıl Görünür?', F,
       '<b>Okuma:</b> Kateter öyküsü olan hastada santral venlerde (subklavyen, brakiyosefalik) darlık gelişebilir. Kateter dururken sessiz kalan darlık, aynı tarafa erişim açılıp akım artınca belirti verir: '
       'kolda, memede ve yüzde ödem, göğüs duvarında kollateral venler, yüksek venöz basınç ve uzayan kanama. Tanı venografiyle konur.',
       'Şekil: önden üst gövde ve iki kol. Hastanın sol kolunda (resmin sağı) ön kolda fistül veni ve tüm kolda ödem; sol brakiyosefalik vende vena kavaya katılmadan önce kısa bir darlık, '
       'darlığın erişim tarafında genişlemiş subklavyen ve aksiller ven; aynı tarafta göğüs duvarında çok sayıda kıvrımlı kollateral ven. Karşı kol normal.')


# ============================================================================================== E · kateter disfonksiyonu
F = Fig('kat', 452, 'Tünelli kaflı hemodiyaliz kateterinde doğru uç konumu, fibrin kılıfı ve lümen içi trombüs', w=1080)
KX, KO, KW = (12, 368, 724), (10, 524, 1036), (492, 490, 492)   # resimler: ChatGPT ile çizildi (yazısız; 3 panel)
def KP(j, px, py): k = 344 / KW[j]; return (KX[j] + (px - KO[j]) * k, 44 + (py - 24) * k)
BAS = (('Doğru uç konumu', GREEN), ('Fibrin kılıfı', GOLD), ('Lümen içi trombüs', RED))
for j, (b, c) in enumerate(BAS):
    serit(F, KX[j], 6, 344, b, c)
    AN.resim(F, f'an_kat{j}', KX[j], 44, 344, oran=377 / 400)
AN.cagri(F, KP(0, 238, 112), KX[0] + 250, 66, ['sağ internal', 'juguler ven'], fs=11, c='#2b4fa0', renk='#2b4fa0')
AN.cagri(F, KP(0, 128, 183), KX[0] + 68, 236, ['tünel kafı'], fs=11, c='#5a4a2a', renk='#5a4a2a', sol=True)
AN.cagri(F, KP(0, 282, 352), KX[0] + 236, 300, ['uç: kavoatriyal', 'bileşke / sağ atriyum'], fs=11, c=GREEN, renk=GREEN)
AN.cagri(F, KP(1, 905, 335), KX[1] + 200, 330, ['uçta kapak gibi sarkar'], fs=11.2, c='#8a5a00', renk='#8a5a00')
AN.cagri(F, KP(1, 640, 215), KX[1] + 60, 74, ['kateteri dıştan saran kılıf'], fs=11.2, c='#8a5a00', renk='#8a5a00')
AN.cagri(F, KP(2, 1330, 290), KX[2] + 200, 330, ['lümeni tıkayan pıhtı'], fs=11.2, c=RED, renk=RED)
NOT = (('Önce mekanik: pozisyon, kink, dikiş;', 'akciğer grafisi ile uç konumu'),
       ('Emme bozuk, verme iyi: tek yönlü tıkanma;', 'sıyırma ya da tel üzerinden değişim'),
       ('İlk girişim: lümen içi fibrinolitik', 'kilit (doku plazminojen aktivatörü)'))
for j, (a, b) in enumerate(NOT):
    F.r(KX[j], 380, 344, 64, TINT.get(BAS[j][1], '#f2f5f8'), BAS[j][1], 1.2, 10)
    F.t(KX[j] + 172, 404, a, 11.6, 700, INK, 'middle'); F.t(KX[j] + 172, 422, b, 11.6, None, INK2, 'middle')
D.yeni('s38_kat', 'x38_30', 'Kateter · Şekil', 'Kateter Akımı Neden Düşer?', F,
       '<b>Okuma:</b> Kateter ucu kavoatriyal bileşkede ya da sağ atriyumun üst kısmında olmalıdır. Akım düşünce önce mekanik nedenler (pozisyon, kink, uç konumu) dışlanır. '
       'Fibrin kılıfı kateteri dıştan sarar ve uçta kapak gibi davranır: verme çoğu kez iyi, emme bozuktur; sıyırma ya da tel üzerinden değişim gerekir. Lümen içi trombüste ilk girişim fibrinolitik kilittir.',
       'Şekil: üç panel. Solda sağ internal juguler venden giren tünelli kateter, kafı cilt altı tünelde, ucu sağ atriyumun üst kısmında. Ortada kateter ucunu dıştan saran, uçta kapak gibi sarkan ince fibrin kılıfı. '
       'Sağda kateter lümenlerinden birini tıkayan koyu kırmızı trombüs. Her panelin altında ilk yaklaşım.')


# ============================================================================================== F · iğneleme teknikleri
F = Fig('ign', 440, 'Fistül iğneleme teknikleri: ip merdiveni, düğme deliği ve alan tekniğinde anevrizma', w=1080)
IX, IO, IW = (12, 368, 724), (12, 524, 1036), 490  # resimler: ChatGPT ile çizildi (yazısız; 3 panel)
def IP_(j, px, py): k = 344 / IW; return (IX[j] + (px - IO[j]) * k, 44 + (py - 26) * k)
BAS = (('İp merdiveni', GREEN), ('Düğme iliği', BRAND), ('Alan tekniği', RED))
for j, (b, c) in enumerate(BAS):
    serit(F, IX[j], 6, 344, b, c)
    AN.resim(F, f'an_ign{j}', IX[j], 44, 344, oran=374 / 400)
AN.cagri(F, IP_(0, 210, 222), IX[0] + 40, 92, ['her seansta farklı nokta'], fs=11.2, c=GREEN, renk=GREEN)
AN.cagri(F, IP_(1, 645, 205), IX[1] + 18, 80, ['aynı nokta, aynı açı'], fs=11.2, c=BRAND, renk=BRAND)
AN.cagri(F, IP_(1, 652, 352), IX[1] + 150, 238, ['epitelize tünel'], fs=11.2, c=BRAND, renk=BRAND)
AN.cagri(F, IP_(2, 1210, 205), IX[2] + 40, 92, ['anevrizma; ince, parlak deri'], fs=11.2, c=RED, renk=RED)
NOT = (('Çoğu merkezde varsayılan yöntem;', 'uzun ve düz segment gerektirir'),
       ('Tünel oluşunca künt iğne; enfeksiyon', 'riski: sıkı asepsi. Greftte uygulanmaz'),
       ('Önerilmez: anevrizma, deri incelmesi', 've kanama riskini en çok artırır'))
for j, (a, b) in enumerate(NOT):
    F.r(IX[j], 370, 344, 62, TINT.get(BAS[j][1], '#f2f5f8'), BAS[j][1], 1.2, 10)
    F.t(IX[j] + 172, 394, a, 11.6, 700, INK, 'middle'); F.t(IX[j] + 172, 412, b, 11.6, None, INK2, 'middle')
D.yeni('s38_ign', 'x38_34', 'Kanülasyon · Şekil', 'Üç İğneleme Tekniği — Fistülde Ne Bırakır?', F,
       '<b>Okuma:</b> İp merdiveninde her seansta fistül boyunca farklı bir noktaya girilir; yük tüm segmente dağılır. Düğme iliğinde hep aynı nokta ve açı kullanılır; oluşan epitelize tünelde künt iğne kullanılır, '
       'enfeksiyonu önlemek için sıkı asepsi gerekir ve greftte uygulanmaz. Alan tekniğinde dar bir bölgeye tekrar tekrar girilir; anevrizma, deri incelmesi ve kanama riski en yüksektir.',
       'Şekil: üç panel, avuç yukarı ön kol ve deri altında fistül veni. Solda fistül boyunca eşit aralıklı, tek sıra iğne izleri. Ortada iki sabit giriş noktasına yerleşmiş iğneler: arteriyel iğne anastomoza yakın, venöz iğne proksimalde; '
       'altta kesit büyütmede deriden vene uzanan eğik tünel. Sağda dar bir alanda çok sayıda iğne izi ve o bölgede balon gibi genişlemiş anevrizma, üzerinde incelmiş deri.')
