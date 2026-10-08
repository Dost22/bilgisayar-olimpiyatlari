# Round-2 Denetim Raporu — Bağımsız Doğrulama

`scripts/review_chapter.py` (Gemini 3.8) ile **düzeltmelerden sonraki güncel hâl**
üzerinde ikinci tam tur denetim. Rapor tarihi: 19 Eylül 2026.

## Özet — iyileşme

| Ölçüt | Round 1 | Round 2 |
|---|---|---|
| Toplam bulgu | 110 (+10 çapraz) | **82** (+5 çapraz) |
| **Kritik** | 8 | **1** |
| Major | 48 | 31 |
| Minor | 53 | 49 |

Tür dağılımı (R2): `notation_violation` 31, `factual` 21, `bad_reference` 11,
`logic_gap` 8, `math_error` 5, `duplicated_example` 5, `prerequisite_violation` 1.

Round 1'in 8 kritiğinin tamamı kapatıldı; yerine tek yeni kritik çıktı (B17).

---

## A) GERÇEK MATEMATİK HATALARI — bağımsız doğrulandı

### A0. `16_parite_ve_simetri.tex:295-328` — KRİTİK: YANLIŞ İDDİA (at turu)

**Bulgu.** Örnek, "$5 \times 5$ tahtada at $(1,1)$'den başlayıp her kareyi bir kez
ziyaret ederek $(5,5)$'te durabilir mi?" diye sorup **"hayır"** sonucuna varıyor
(satır 327: "ayrıntılı bir graf analizi ... Hamilton yolunun bulunmadığını gösterir").

**Neden yanlış.** Böyle bir yol **vardır**. Bağımsız doğrulama
(`/tmp/knight.py`, tam arama + Warnsdorff sıralaması):

```
(1,1) → (2,3) → (1,5) → (3,4) → (4,2) → (5,4) → (3,5) → (1,4) → (2,2) → (4,1)
→ (5,3) → (4,5) → (2,4) → (1,2) → (3,1) → (5,2) → (4,4) → (2,5) → (3,3) → (2,1)
→ (1,3) → (3,2) → (5,1) → (4,3) → (5,5)
```

25 karenin tamamı ziyaret ediliyor ve tüm hamleler geçerli (programatik olarak
doğrulandı). Kitabın kendi metni de satır 323'te "açık bir at turu $5 \times 5$'te
mevcuttur" diyerek çelişkiye düşüyor.

**Doğru klasik ifade.** $5 \times 5$ tahtada **kapalı** tur yoktur; çünkü kapalı bir
turda ziyaret edilen siyah ve beyaz kare sayıları eşit olmak zorundadır, oysa tahtada
$13$ siyah ve $12$ beyaz kare vardır. (Doğrulama: $(1,1) \to (1,1)$ kapalı tur
aramasi → **YOK**.)

**Önerilen düzeltme:** örnek ve ispat, kapalı tur biçimine çevrilsin (hazırlanan
`P18-16-at` görevi).

### A1. `17_invaryant_ve_monovaryant.tex:363-382` — KRİTİK: yanlış monovaryant

**Bulgu.** Çember süreci (negatif sayı işaret değiştirir, komşularına mutlak
değeri eklenir) için çözümde şu potansiyel öneriliyor:

$$\Phi = \sum_{1 \le i < j \le n} |x_i - x_j| \quad \text{veya} \quad \sum_{i=1}^n \Bigl(\sum_{j=1}^{n-1} j\,x_{i+j}\Bigr)^2$$

ve gerekçe olarak "ters sıralanmış çiftlerin azalması" ile "durum uzayının sonlu
sayıda permütasyonla ilişkili olması" gösteriliyor.

**Neden yanlış.** (i) Önerilen fonksiyonlar monovaryant **değildir**; (ii) $x_i$'ler
reel sayı olduğundan "sonlu permütasyon" argümanı geçersizdir; (iii) toplam
invaryantı zaten gösterilmiş, ama sonlanma için bu yetmez.

**Bağımsız doğrulama** (`/tmp/verify_r2.py`, `/tmp/find_mono.py`):

| Aday fonksiyon | Arttığı hamle / toplam |
|---|---|
| $\sum\|x_i-x_j\|$ | 602 / 2705 |
| $\sum(x_i-x_j)^2$ | 583 / 2772 |
| $\sum(x_i-x_{i+1})^2$ | 837 / 2213 |
| $\sum x_i^2$ | 3869 / ~15000 |
| $\sum \max(0,-x_i)$ | 2820 / ~15000 |
| negatif sayı adedi | 3447 / ~15000 |
| $\max x_i$ | 2577 / ~15000 |

Yani kitapta önerilenler dâhil **hiçbir doğal aday monovaryant değil.**

**DOĞRU ÇÖZÜM (bulundu ve doğrulandı).** Problem, klasik **IMO 1986 Soru 3**
beşgen versiyonudur; doğru potansiyel **pentagram köşegenleri** üzerindedir:

$$\Phi = \tfrac{1}{2}\sum_{i=1}^{5}(x_i - x_{i+2})^2$$

- $\Phi \ge 0$ ve tamsayı değerlidir (kareler toplamı, yarısı).
- Her hamlede **$\Delta\Phi = -\,t\cdot S$**; burada $t = |x_i| > 0$ (seçilen negatif
  sayının mutlak değeri) ve $S = \sum x_i > 0$ (invaryant toplam). Dolayısıyla
  $\Delta\Phi < 0$ **kesin**.
- Sonuç: $\Phi$ negatif olmayan bir tamsayı olup her adımda kesin azalır; süreç en
  fazla $\Phi_0$ adımda durur.

**Doğrulama sonucu:** $\Delta\Phi = -tS$ eşitliği **19.246 hamlede sıfır uyuşmazlık**
ile sağlandı ve "adım sayısı ≤ $\Phi_0$" empirik olarak doğrulandı
(`/tmp/verify_phi.py`). Monovaryantlık yalnızca **n = 5** için geçerlidir (k = 2 ≡ 3);
diğer $n,k$ çiftlerinde geçmez (`/tmp/phi_general.py`).

**Önerilen düzeltme:** Örnek, klasik beşgen/tamsayı biçimine çevrilsin ve çözüm
yukarıdaki $\Phi$ ile yeniden yazılsın. (Reel sayı versiyonu korunacaksa sonlanma
iddiası bu yöntemle ispatlanamaz.)

### A2. `35_karma_cozumlu_problemler.tex:652` — MAJOR: toplamın üst sınırı

**Bulgu.** İçerme-dışarma formülü

$$N(\text{hiçbiri}) = \sum_{k=0}^{2n-1} (-1)^k\, r_k\, (n-k)!$$

üst sınırı $2n-1$ ile yazılmış. Ancak $k > n$ için $(n-k)!$ **tanımsızdır** ve
$n \times n$ tahtaya aynı satır/sütunda olmayan en fazla $n$ yasaklı kare
yerleştirilebilir.

**Bağımsız doğrulama** (`/tmp/verify_r2.py`) — brute-force sayım:

| n | brute-force | üst sınır $n$ | üst sınır $2n-1$ |
|---|---|---|---|
| 2 | 0 | **0 ✓** | tanımsız |
| 3 | 1 | **1 ✓** | tanımsız |
| 4 | 3 | **3 ✓** | tanımsız |
| 5 | 16 | **16 ✓** | tanımsız |
| 6 | 96 | **96 ✓** | tanımsız |
| 7 | 675 | **675 ✓** | tanımsız |

**Önerilen düzeltme:** üst sınır $2n-1 \to n$. (Formülün geri kalanı doğru.)

---

## B) GERÇEK TEKNİK HATA — sistematik

### B1. C kod bloklarında `#` işareti düşmüş

**Bulgu.** 14 dosyada toplam ~51 satırda önişlemci yönergeleri
`include <stdio.h>` / `define MAXN 1005` biçiminde, yani **baştaki `#` yok**.
Diğer 9 dosyada `#include` doğru yazılmış → **tutarsız ve derlenemez C**.

Kök neden: geçmişteki bir "düz metinde `#` kaçışı" geçişi, `lstlisting` içindeki
`#` karakterlerini de silmiş. `templates/main.tex` içindeki `CTemel` dilinde
`include, define` anahtar sözcük olarak tanımlı olduğundan dizgi hatası
vermiyor, bu yüzden derleme yeşil kalırken hata görünmez kalmış.

**Etkilenen dosyalar (satır sayısı):** `09`(2), `11`(1), `12`(4), `19`(1), `23`(1),
`24`(2), `25`(7), `27`(5), `30`(7), `31`(3), `33`(1), `34`(9), `35`(6), `36`(4).

**Önerilen düzeltme:** yalnızca `lstlisting` blokları içinde, satır başındaki
`include <...>` → `#include <...>` ve `define NAME ...` → `#define NAME ...`.

### B2. Bézout Özdeşliği / Genişletilmiş Öklid — hiç anlatılmıyor, ama atıf veriliyor

**Bulgu.** Kavram kitapta **hiçbir yerde tanıtılmıyor**, buna karşın:

- `36_cozumler_ve_ipuclari.tex:235`: "Sayılar aralarında asal ise **Bölüm~13'te
  işlediğimiz Genişletilmiş Öklid Algoritması** ile geriye doğru giderek ..."
  → B13'te böyle bir içerik **yok** (doğrulandı: `grep` B13'te
  "Genişletilmiş"/"Bézout"/"ax + by" için sonuç vermiyor).
- `36_...:246`: çözümde "Geriye Doğru Yerine Koyma (Bézout Özdeşliği)" adımı
  kullanılıyor.
- `37_ekler.tex:93`: "Bézout Özdeşliği ve Genişletilmiş Öklid **(Bölüm 13 ve 16)**"
  → B16 "Parite ve Simetri" olup konuyla ilgisizdir; B13'te de içerik yok.

Bu, kullanıcının kuralının ("kitap, anlatmadığı hiçbir kavrama referans vermez")
doğrudan ihlalidir — FLT vakasıyla (D17) aynı sınıftan.

**Önerilen düzeltme:** Bézout Özdeşliği ve Genişletilmiş Öklid, doğal yeri olan
**Bölüm 13'e (EBOB ve EKOK)** öğretilsin (teorem + geriye doğru yerine koyma
yöntemi + $42x + 55y = 1$ tipi bir örnek); ardından `37:93`'teki atıf
"(Bölüm 13)" olarak düzeltilsin. Böylece `36:235`'teki atıf da doğru hâle gelir.

---

## C) YANLIŞ BÖLÜM ATIFLARI

| Dosya:satır | Mevcut | Doğrusu |
|---|---|---|
| `11_bolunebilme.tex:427` | "Bölüm 1'de ele aldığımız İyi Sıralama İlkesi" | Bölüm 18 |
| `24_temel_veri_yapilari.tex:55` | "Bölüm 19'da gördüğümüz fonksiyon çağrıları" | Bölüm 29 |
| `37_ekler.tex:118` | "Bézout ve Genişletilmiş Öklid (Bölüm 13 ve 16)" | Bölüm 13 — **ama önce B13'e içerik eklenmeli (bkz. B2)** |

---

## D) TEKRARLANAN KLASİK ÖRNEKLER

| Örnek | Nerede tekrarlı | Öneri |
|---|---|---|
| IMO 1959 S1, $(21n+4)/(14n+3)$ | B12 §223 **ve** B13 §277, ikisinde de sıfırdan çözülü | B13'te (Öklid) kalsın; B12'de ya kaldır ya da B13'e atıf |
| Kesik satranç tahtası (domino) | B16 §202 **ve** B17 §105 | B17'deki örnek farklı bir invaryant problemiyle değiştirilsin |
| Hanoi Kuleleri | B09 §255 **ve** B25 §107 | B25'te B09'daki $T(n)=2T(n-1)+1$ bağıntısına atıf verilsin |
| $n \mid 2^n-1$ | B11 §535 örneği **ve** B33 §148 alıştırması | B11'den çıkarılsın (B33'te alıştırma olarak kalsın) |

---

## E) MANTIK BOŞLUKLARI

1. **`11:331`** — Palindrom basamak indekslemesi tutarsız: sayı
   $N = \overline{a_k \dots a_1 a_1 \dots a_k}$ diye tanımlanıp çözümde $a_m$'nin
   sağ yarıdaki indisi $m-1$ kabul edilmiş; tanım ile kullanım çelişiyor.
2. **`16:282`** — At (knight) örneği: "atın rengi değiştirir" kuralı tek başına
   çelişki vermiyor deniyor, sonra "ayrıntılı bir graf analizi gösterir" denerek
   ispat tamamlanmıyor. (Round 1'den beri açık.)
3. **`17:384-...`** — Örnek soru **taş eksiltme** (her saniye bir taş kaldırma)
   ama çözümün büyük kısmı soruda geçmeyen **virüs yayılımı** problemini
   çözüyor; soru ile çözüm uyuşmuyor.
4. **`26:271-291`** — Kesit Özelliği ispatı "tüm MST'lerde bulunma" sonucuna
   ulaşmıyor (hipotez "kesin en küçük", ispatta $w(e) \le w(e')$). Round 1'den beri açık.

---

## F) TERİM SÖZLEŞMESİ (notation_violation) — DİKKAT: yanlış pozitif içeriyor

Denetim, `terminology.md` Tablo A'yı harfiyen uygulayarak 31 ihlal bildirdi.
Bunların önemli bir kısmı **karar gerektirir**, çünkü kitap zaten
"İngilizce (Türkçe)" kalıbını kullanıyor:

| Bulgu | Örnek | Değerlendirme |
|---|---|---|
| "kümülatif toplam" | `21:118` başlık `\section{Kümülatif Toplamlar (Prefix Sums)}`; `35`, `36` | Başlıklar İngilizce-öncelikli yapılabilir; metin içi kullanımlar da düzeltilmeli |
| "iki işaretçi" | `21:233`, `34:401` başlıkları | Aynı |
| "yığın / kuyruk / eşlem" | `24:18` başlıkları `\section{Stack (Yığın)}` | **Karar gerekli**: "yığın/kuyruk" Türkçe literatürde yerleşik; Tablo A onları yasaklıyor |
| "açgözlü" | `26:61` `[Açgözlü Seçim Özelliği / Greedy Choice Property]` | Başlıktan çıkarılmalı |
| "özyineleme" | `34:216` "Özyineleme yığınından" | **Gerçek ihlal** (standardize terim: rekürsiyon) |
| sözde kodda `MOD` | `14:115` | ❌ **YANLIŞ POZİTİF** — blok artık sözde kod, `MOD` doğrudur |

---

## Önerilen triyaj

| Öncelik | İçerik | Nitelik |
|---|---|---|
| **R1** | A1 (B17 monovaryant) — doğru ispatla yeniden yaz | doğrulanmış matematik hatası |
| **R2** | A2 (B35 üst sınır $n$) | doğrulanmış matematik hatası |
| **R3** | B1 (`#include` — 14 dosya, ~51 satır) | doğrulanmış teknik hata |
| **R4** | C (3 yanlış atıf) | mekanik |
| **R5** | D (4 tekrar eden klasik) | editoryal |
| **R6** | E (4 mantık boşluğu; `16:282` ve `26:271` dahil) | yeniden yazım |
| **R7** | F (terminoloji; karar gerektirenler ayrıştırılarak) | karar + düzeltme |