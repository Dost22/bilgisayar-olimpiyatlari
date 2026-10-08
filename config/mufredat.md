# Müfredat — Bilgisayar Olimpiyatlarına Hazırlık

## Kitap Kimliği

- **Hedef sınav:** TÜBİTAK Bilgisayar Olimpiyatı 1. Aşama
- **Okuyucu:** Kombinatorik ve bilgisayar önbilgisi **olmayan** biri
- **Hedef uzunluk:** sabit sınır yok; **tam donanımlı ~430 sayfa** (aşağıdaki bütçeler tahminî, ±10% kabul)
- **Anlatım ilkesi:** somuttan soyuta; her bölüm kendi konusunu elle hesaplanmış küçük bir örnekle açar ve genelleşir. Okuyucu yalnızca **önkoşul** bölümlerini bilir: önceki bölümlere metinle atıf yapılır, sonraki bölümlerin kavramları kullanılmaz. Bol çözümlü örnek; klasik problemler uyarlanır; alıştırma + tam çözüm ile pekiştirme.

## Öncelik Etiketleri (1. Aşama perspektifi)

Bölüm başlıklarının sonundaki `öncelik` alanı, konunun TÜBİTAK 1. Aşama için taşıdığı önemi üç düzeyde işaretler (yalnızca Bölüm 1–32; 33–38 alıştırma/başvuru bölümleri işaretsizdir):

- **Temel:** Sınavın omurgası; bunlar olmadan başarı neredeyse imkânsız. İlk dalgada bitirilmeli.
- **Orta:** Sınavda düzenli çıkar; Temel'ler bittikten sonra çalışılmalı, derinleşme isteğe bağlı.
- **İleri:** Nadir/dolaylı çıkar; zaman kalırsa veya 2. Aşama hedefleniyorsa.

Bu alan **tek kaynaktır**: kitaptaki **fihrist etiketi** (bölüm dosyalarında `\chapter[Başlık · \textit{X}]{Başlık}` biçimi — İçindekiler'de başlığın yanında görünür) ve sitedeki içindekiler rozetleri buradan beslenir (`scripts/oncelik_etiketle.py` ve `scripts/build_site.py`). Öncelik değişecekse önce bu dosyada düzeltin, sonra `python3 scripts/oncelik_etiketle.py` ile kitaba işleyin.

## Dosya ve Bölüm Düzeni

- Kitap **7 KISIM**, **38 BÖLÜM (chapter)** ve bölüm başına birden çok **alt konu (section)** içerir.
- **Her BÖLÜM = bir `.tex` dosyası:** `/output/{NN}_{slug}.tex` (NN = 2 haneli bölüm numarası).
- Bölüm dosyası `\chapter{...}` ile başlar; alt konular ardışık `\section{...}` olur.
- Bir ajan, kendisine verilen **bölümün tamamını** yazar.
- Sayfa bütçeleri bölümün derinliğini belirtir; `AGENTS.md` + `topic_prompt.md` yazım kurallarını tanımlar.

## Bölüm Haritası (özet)

| Kısım | Bölümler | Sayfa |
|---|---|---|
| I. Sıfırdan Temeller | 1–2 | 17 |
| II. Sayma (Kombinatorik) | 3–10 | 110 |
| III. Sayılar Teorisi | 11–16 | 59 |
| IV. Düşünme Teknikleri | 17–19 | 26 |
| V. Algoritmik Düşünce | 20–28 | 105 |
| VI. C Programlama | 29–32 | 42 |
| VII. Alıştırma ve Ekler | 33–38 + ekler | ~70 |
| **Toplam** | | **~429** |

---

## KISIM I — Sıfırdan Temeller (17 sayfa)
*Amaç:* Kitabın geri kalanında kullanılacak dili ve ispat alışkanlığını kazandırmak.

### Bölüm 1 — Matematiğin Dili (8 sayfa · önkoşul: yok · öncelik: Temel)
- **1.1 Kümeler ve gösterim (3s)** — eleman (`∈`), boş küme, alt küme (`⊆`), birleşim/kesişim, eleman sayısı `|A|`. ▶ Venn sezgisi.
- **1.2 Mantık: önermeler (3s)** — ve (`∧`), veya (`∨`), değil (`¬`), gerektirme (`⇒`), karşıt pozitif. ▶ doğruluk tabloları.
- **1.3 Niceleyiciler (2s)** — "her" (`∀`), "vardır" (`∃`) ve bunların olumsuzu.

### Bölüm 2 — İspat Nasıl Yapılır (9 sayfa · önkoşul: 1 · öncelik: Temel)
- **2.1 Doğrudan ispat (2s)** — varsayımdan sonuca adım adım.
- **2.2 Çelişkiyle ispat (2s)** — tersini varsayıp çelişki. ★ $\sqrt{2}$ irrasyoneldir.
- **2.3 Karşı örnekle çürütme (1s)** — evrensel iddiayı tek örnekle yıkmak.
- **2.4 Tümevarım ve toplam gösterimi (2s)** — `Σ`; $1+2+\dots+n=\frac{n(n+1)}{2}$.
- **2.5 İspatlı küçük örnekler (2s)** — teknikleri pekiştiren çözümlü ispatlar.

## KISIM II — Sayma / Kombinatorik (110 sayfa)
*Amaç:* TÜBİTAK 1. Aşamanın en yoğun konusu olan saymayı sıfırdan ve derinlemesine kurmak.

### Bölüm 3 — Saymanın Temel İlkeleri (14 sayfa · önkoşul: 1,2 · öncelik: Temel)
- **3.1 Çarpma kuralı (4s)** — bağımsız adımlar; gömlek/pantolon örnekleri.
- **3.2 Toplama kuralı (3s)** — ayrık durumlar.
- **3.3 Ağaç diyagramları ve listeleme (3s)** — sezgi kurma.
- **3.4 İki ilkeyi birlikte kullanma (4s)** — karışık problemler.

### Bölüm 4 — Permütasyon (16 sayfa · önkoşul: 3 · öncelik: Temel)
- **4.1 Faktöriyel (3s)** — $n!$ ve çarpma kuralından gerekçesi.
- **4.2 Sıralı seçim P(n,r) (4s)** — $n$'den $r$ tanesini sırayla.
- **4.3 Tekrarlı permütasyon (4s)** — $\frac{n!}{n_1!n_2!}$. ★ kelime harf dizilimleri.
- **4.4 Dairesel permütasyon (4s)** — $(n-1)!$; dönme ayıklama. ★ yuvarlak masa.

### Bölüm 5 — Kombinasyon (16 sayfa · önkoşul: 4 · öncelik: Temel)
- **5.1 Binom katsayısı (4s)** — $\binom{n}{r}$, $P(n,r)/r!$ ilişkisi; elle örnek.
- **5.2 Simetri ve Pascal bağıntısı (3s)** — örnekten sonra özellik olarak.
- **5.3 Ayraç yöntemi (5s)** — özdeş dağıtım; boş/boş olmayan kutular.
- **5.4 Karışık seçme problemleri (4s)** — komite, el seçme, kısıtlı seçim.

### Bölüm 6 — Binom Açılımı ve Özdeşlikler (14 sayfa · önkoşul: 5 · öncelik: Orta)
- **6.1 Elle açmadan teoreme (4s)** — $(a+b)^2,(a+b)^3$ elle açılır, desen keşfedilir.
- **6.2 Pascal üçgeni (3s)** — katsayıların tablosu.
- **6.3 Özdeşlikler (4s)** — $2^n$, alternatif toplam, hokey sopası.
- **6.4 Kombinatorik ispat (3s)** — "iki yoldan sayma" yaklaşımına giriş.

### Bölüm 7 — Güvercin Yuvası İlkesi (10 sayfa · önkoşul: 1 · öncelik: Temel)
- **7.1 Temel ilke (3s)** — çelişkiyle ispat; somut başlangıç.
- **7.2 Genelleştirilmiş ilke (3s)** — $\lceil n/k\rceil$.
- **7.3 Uygulamalar (4s)** — bölünebilme, geometri. ★ $2n$'den $n+1$ sayı; karede noktalar.

### Bölüm 8 — İçerme-Dışarma (10 sayfa · önkoşul: 5 · öncelik: Orta)
- **8.1 İki ve üç küme (3s)** — Venn ile.
- **8.2 Genel formül (4s)** — "her eleman tam 1 kez".
- **8.3 Düzensiz dizilimler / şapka problemi (3s)** — derangement.

### Bölüm 9 — Izgara Yolları ve Yineleme Bağıntıları (16 sayfa · önkoşul: 5 · öncelik: İleri)
- **9.1 Izgara yolları (5s)** — $(0,0)\to(m,n)$, sağ/yukarı adımlar, $\binom{m+n}{m}$. ★ kafes yolu sayımı.
- **9.2 Yineleme bağıntısı kavramı (3s)** — $a_n$'i önceki terimlerden kurmak.
- **9.3 Fibonacci ve uygulamaları (4s)** — merdiven çıkma; $2\times n$ domino döşeme.
- **9.4 Kapalı form sezgisi (4s)** — karakteristik denklem fikri (hafif).

### Bölüm 10 — Çifte Sayım ve Birebir Eşleme (14 sayfa · önkoşul: 5,6 · öncelik: İleri)
- **10.1 Çifte sayım (double counting) (5s)** — aynı miktarı iki farklı yoldan sayıp eşitleme. ★ el sıkışma lemması.
- **10.2 Birebir eşleme (bijection) (5s)** — kümeler arası 1-1 eşleme kurma.
- **10.3 Kombinatorik ispat örnekleri (4s)** — Pascal'a ikinci ispat, alt küme sayısı.

*KISIM II bütçe: 14+16+16+14+10+10+16+14 = 110*

## KISIM III — Sayılar Teorisi (59 sayfa)
*Amaç:* Bölünebilme, asal sayılar, EBOB/EKOK, modüler aritmetik, taban aritmetiği ve logaritma; sayı kuramının TÜBİTAK çekirdeği.

### Bölüm 11 — Bölünebilme (14 sayfa · önkoşul: 1,2 · öncelik: Temel)
- **11.1 Bölünebilme ve gösterim (3s)** — $a \mid b$.
- **11.2 Bölünebilme kuralları (6s)** — $2,3,4,5,9,11$ ve NEDENLERİ.
- **11.3 Bölme algoritması (5s)** — bölüm ve kalan; $0\le r<b$.

### Bölüm 12 — Asal Sayılar (11 sayfa · önkoşul: 11 · öncelik: Temel)
- **12.1 Asal ve Eratosthenes kalburu (4s)**.
- **12.2 Aralarında asal (3s)** — $\gcd=1$.
- **12.3 Asal çarpanlara ayırma (4s)** — temel teorem; bölen sayısı.

### Bölüm 13 — EBOB ve EKOK (12 sayfa · önkoşul: 12 · öncelik: Temel)
- **13.1 Tanımlar ve özellikler (4s)** — $\gcd$, $\operatorname{lcm}$.
- **13.2 Öklid algoritması (4s)** — NEDEN çalıştığı.
- **13.3 $\gcd\cdot\operatorname{lcm}=ab$ (4s)**.

### Bölüm 14 — Modüler Aritmetik (9 sayfa · önkoşul: 11 · öncelik: Temel)
- **14.1 Kongruans (3s)** — $a\equiv b \pmod m$.
- **14.2 Modüler aritmetik ve üs (3s)** — kurallar.
- **14.3 Son basamak ve kalan problemleri (3s)**.

### Bölüm 15 — Taban Aritmetiği (8 sayfa · önkoşul: 11 · öncelik: İleri)
- **15.1 Taban ve dönüşüm (4s)** — 10↔2, $(101)_2=5$.
- **15.2 Tabanlarda aritmetik + binary'nin CS'deki yeri (4s)**.

### Bölüm 16 — Logaritma (5 sayfa · önkoşul: 15 · öncelik: Orta)
- **16.1 Logaritma nedir? (2s)** — $\log_a x$ tanımı, taban ve argüman; $a^{\log_a x}=x$; basamak sayısı uygulaması. ★ $2^{100}$ kaç basamaklı?
- **16.2 Temel kurallar (1,5s)** — çarpım kuralı (çarpma → toplama), bölüm ve kuvvet kuralı; ispatları ve kısa uygulamalar.
- **16.3 Taban değiştirme (1,5s)** — $\log_a x=\frac{\log_b x}{\log_b a}$; zincirleme sadeleşme; $O(\log n)$ yazarken tabanın önemsizliği.

## KISIM IV — Düşünme Teknikleri (26 sayfa)
*Amaç:* İmkânsızlık ve varlık ispatlarının olimpiyat teknikleri.

### Bölüm 17 — Parite ve Simetri (10 sayfa · önkoşul: 1 · öncelik: Temel)
- **17.1 Parite ve imkânsızlık (4s)** — tek/çift kuralları; alan paritesi.
- **17.2 Renklendirme argümanları (3s)** — tahtayı renklendir. ★ kesik satranç tahtası.
- **17.3 Simetri ile sayma (3s)** — yansıma/ayna. ★ palindrom sayımı.

### Bölüm 18 — İnvaryant ve Monovaryant (8 sayfa · önkoşul: 17 · öncelik: İleri)
- **18.1 İnvaryant (4s)** — değişmeyen nicelik; imkânsızlık. ★ bukalemun problemi.
- **18.2 Monovaryant (4s)** — sürekli azalan nicelik; sonlanma ispatı.

### Bölüm 19 — Uç Değer ve Tersine Çalışma (8 sayfa · önkoşul: 1 · öncelik: Orta)
- **19.1 Uç değer ilkesi (4s)** — en büyük/en küçük eleman. ★ en büyük asal yoktur; minimal karşı örnek.
- **19.2 Tersine çalışma (4s)** — hedeften geriye. ★ yumurta problemi.

## KISIM V — Algoritmik Düşünce (105 sayfa)
*Amaç:* Programlamadan önce sözde kodla algoritma ve karmaşıklık kültürü.

### Bölüm 20 — Algoritma Nedir (10 sayfa · önkoşul: 1 · öncelik: Temel)
- **20.1 Problem, girdi-çıktı, algoritma (3s)** — yemek tarifi benzetmesi.
- **20.2 Sözde kod (4s)** — adım adım talimat dili.
- **20.3 Değişken, koşul, döngü (sözde kodla) (3s)**.

### Bölüm 21 — Karmaşıklık ve Big O (10 sayfa · önkoşul: 20 · öncelik: Temel)
- **21.1 İşlem sayısı (3s)** — hızı ölçmek; n büyüdükçe ne olur.
- **21.2 Big O notasyonu (4s)** — $O(1)$, $O(\log n)$, $O(n)$, $O(n^2)$ sezgisi.
- **21.3 Pratik limitler (3s)** — ~$10^8$ işlem/sn; alan karmaşıklığı.

### Bölüm 22 — Diziler ve Temel Teknikler (12 sayfa · önkoşul: 21 · öncelik: Temel)
- **22.1 Diziler, indis, tarama (3s)**.
- **22.2 Kümülatif toplamlar / prefix sums (5s)** — aralık toplamını $O(1)$. ★ kritik başlangıç tekniği.
- **22.3 İki işaretçi / two pointers (4s)** — sıralı dizide çift tarama.

### Bölüm 23 — Sıralama (14 sayfa · önkoşul: 22 · öncelik: Temel)
- **23.1 Neden sıralarız (2s)**.
- **23.2 Bubble ve Insertion (4s)** — $O(n^2)$ sezgisi.
- **23.3 Merge ve Quick (5s)** — böl-ve-fethet; $O(n\log n)$.
- **23.4 Karmaşıklık karşılaştırması (3s)**.

### Bölüm 24 — İkili Arama (8 sayfa · önkoşul: 23 · öncelik: Temel)
- **24.1 Sıralı dizide arama (4s)** — her adımda yarıya bölme.
- **24.2 Cevap üzerinde ikili arama / bisection (4s)**.

### Bölüm 25 — Temel Veri Yapıları (12 sayfa · önkoşul: 20 · öncelik: Temel)
- **25.1 Stack (4s)** — LIFO.
- **25.2 Queue (4s)** — FIFO.
- **25.3 Set ve Map (4s)** — kavramsal.

### Bölüm 26 — Rekürsiyon ve DP'ye Giriş (14 sayfa · önkoşul: 20 · öncelik: Orta)
- **26.1 Rekürsiyon (4s)** — kendi kendini çağırma; baz durum.
- **26.2 Memoization (4s)** — tekrar hesabı önleme.
- **26.3 DP'ye giriş (6s)** — alt problemler. ★ Fibonacci, merdiven.

### Bölüm 27 — Greedy Yaklaşımı (6 sayfa · önkoşul: 20 · öncelik: Orta)
- **27.1 Greedy kavramı (3s)** — yerel en iyi her zaman doğru mu?
- **27.2 Tipik örnekler (3s)** — aralık seçimi, bozuk para (şartlı), MST bağı.

### Bölüm 28 — Graflar ve Arama (19 sayfa · önkoşul: 25 · öncelik: Orta)
- **28.1 Graflar ve temsiller (3s)** — düğüm/kenar; komşuluk listesi/matrisi.
- **28.2 DFS (3s)**.
- **28.3 BFS (3s)** — en kısa adım.
- **28.4 Topolojik sıralama (3s)** — bağımlılık sırası.
- **28.5 MST / Kruskal-Prim sezgisi (4s)**.
- **28.6 En kısa yol / Dijkstra sezgisi (3s)**.

## KISIM VI — C Programlama (42 sayfa)
*Amaç:* Algoritmaları gerçek bir dille hayata geçirmek; TÜBİTAK'ın C sorularını okumak.

### Bölüm 29 — C'ye Giriş ve Kontrol Akışı (11 sayfa · önkoşul: 20 · öncelik: Temel)
- **29.1 Değişkenler, tipler, printf/scanf (5s)** — ilk program; biçim yer tutucular.
- **29.2 if-else ve switch (6s)** — koşullu akış.

### Bölüm 30 — Döngüler ve Fonksiyonlar (11 sayfa · önkoşul: 29 · öncelik: Temel)
- **30.1 Döngüler (6s)** — for/while/do-while; break/continue; iç içe.
- **30.2 Fonksiyonlar (5s)** — parametre aktarımı, modülerlik, dönüş değeri.

### Bölüm 31 — Diziler, Stringler ve Pointer (13 sayfa · önkoşul: 30 · öncelik: Temel)
- **31.1 Diziler (4s)** — tek/çok boyutlu; ardışık bellek.
- **31.2 Stringler (3s)** — karakter dizisi + null sonlandırıcı.
- **31.3 Pointer ve hafıza (6s)** — adres, `&`, `*`, pointer aritmetiği.

### Bölüm 32 — Bitwise Operatörler ve Struct (7 sayfa · önkoşul: 29 · öncelik: Orta)
- **32.1 Bitwise operatörler (4s)** — `& | ^ ~ << >>`; tek/çift testi, altküme temsili.
- **32.2 Struct (3s)** — ilişkili verileri birleştirme.

## KISIM VII — Alıştırma ve Ekler (~70 sayfa)
*Amaç:* Öğrenilenleri pekiştirmek ve TÜBİTAK formatına bağlamak.

### Bölüm 33 — Alıştırmalar: Sayma (KISIM II) (12 sayfa)
- Zorluk işaretli (kolay/orta/zor) alıştırma seti; çözümler alıştırmaların hemen ardından satır içinde verilir. Ek çözümlü problemler için ayrıca Bölüm 37'ya bakınız.

### Bölüm 34 — Alıştırmalar: Sayılar ve Teknikler (KISIM III–IV) (10 sayfa)
- Bölünebilme, modüler, invaryant, uç değer alıştırmaları.

### Bölüm 35 — Alıştırmalar: Algoritma ve C (KISIM V–VI) (12 sayfa)
- Karmaşıklık okuma, iz sürme, küçük kod parçaları üzerine alıştırmalar.

### Bölüm 36 — Karma Çözümlü Problemler (10 sayfa · önkoşul: tümü)
- Konuları birleştiren, TÜBİTAK ayarında çözümlü sorular.

### Bölüm 37 — Ek Çözümlü Problemler ve İpuçları (12 sayfa)
- Bölüm 33–35'ün alıştırmalarından **bağımsız**, önceki bölümlerin araçlarını pekiştiren ek çözümlü problemler (sayma, sayılar teorisi, algoritma) ve her çözümün sonunda verilen ipuçları.
- **Not:** Bölüm 33–35'ün alıştırmaları kendi bölümlerinde satır içi çözülür; B36 onların çözüm kiti değildir (bkz. `KARARLAR.md` → D21).

### Ekler (4 sayfa)
- **A. Formül listesi** — önemli formüller tek sayfada.
- **B. Terimler sözlüğü** — Türkçe↔İngilizce terim tablosu.

---

## Bölüm → Dosya eşleme (özet)

| Bölüm | Dosya adı (`/output/...`) |
|---|---|
| 1 | `01_matematigin_dili.tex` |
| 2 | `02_ispat_nasil_yapilir.tex` |
| 3 | `03_saymanin_temel_ilkeleri.tex` |
| 4 | `04_permutasyon.tex` |
| 5 | `05_kombinasyon.tex` |
| 6 | `06_binom_acilimi_ve_ozdeslikler.tex` |
| 7 | `07_guvercin_yuvasi_ilkesi.tex` |
| 8 | `08_icerme_disarma.tex` |
| 9 | `09_izgara_yollari_ve_yineleme_iliskileri.tex` |
| 10 | `10_cifte_sayim_ve_birebir_esleme.tex` |
| 11 | `11_bolunebilme.tex` |
| 12 | `12_asal_sayilar.tex` |
| 13 | `13_ebob_ve_ekok.tex` |
| 14 | `14_moduler_aritmetik.tex` |
| 15 | `15_taban_aritmetigi.tex` |
| 16 | `16_logaritma.tex` |
| 17 | `17_parite_ve_simetri.tex` |
| 18 | `18_invaryant_ve_monovaryant.tex` |
| 19 | `19_uc_deger_ve_tersine_calisma.tex` |
| 20 | `20_algoritma_nedir.tex` |
| 21 | `21_karmasiklik_ve_bigo.tex` |
| 22 | `22_diziler_ve_temel_teknikler.tex` |
| 23 | `23_siralama.tex` |
| 24 | `24_ikili_arama.tex` |
| 25 | `25_temel_veri_yapilari.tex` |
| 26 | `26_rekursiyon_ve_dp.tex` |
| 27 | `27_greedy_yaklasimi.tex` |
| 28 | `28_graflar_ve_arama.tex` |
| 29 | `29_c_ye_giris_ve_kontrol_akisi.tex` |
| 30 | `30_donguler_ve_fonksiyonlar.tex` |
| 31 | `31_diziler_stringler_ve_pointer.tex` |
| 32 | `32_bitwise_ve_struct.tex` |
| 33 | `33_alistirmalar_sayma.tex` |
| 34 | `34_alistirmalar_sayilar_teknikler.tex` |
| 35 | `35_alistirmalar_algoritma_c.tex` |
| 36 | `36_karma_cozumlu_problemler.tex` |
| 37 | `37_cozumler_ve_ipuclari.tex` |
| ekler | `38_ekler.tex` |



