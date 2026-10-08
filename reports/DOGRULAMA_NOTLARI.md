# Denetim Raporu — İnsan Doğrulama Notları

`scripts/review_chapter.py` (Gemini 3.8) tarafından üretilen otomatik bulgular
(110 adet) ve bağımsız doğrulama sonuçları. **Hiçbir düzeltme uygulanmadı.**

## Özet

| Ölçüt | Değer |
|---|---|
| Taranan bölüm | 37/37 |
| Toplam bulgu | 110 (Pass1) + 10 (Pass2) |
| Kritik | 8 |
| Bağımsız olarak doğrulanan kritik | 6 (hepsi GERÇEK) |

Tür dağılımı: `notation_violation` 49, `factual` 23, `bad_reference` 10,
`duplicated_example` 10, `math_error` 8, `logic_gap` 7, `prerequisite_violation` 3.

## Kritik bulgular — bağımsız doğrulama (`scripts/verify_claims.py`)

### DOĞRULANDI — GERÇEK HATA

1. **B03 (`03_saymanin_temel_ilkeleri.tex:375`)** — "oyun en fazla 6 ya da 7
   atışta sonlanır" **yanlış**. Brute-force: en uzun bitiş **6** atış, toplam
   **15** dizilim (7'si `TT`, 8'i 3. `Y` ile). Ayrıca satır 373'teki sayım
   "vb." ile bırakılmış, toplam verilmemiş.

2. **B12 (`12_asal_sayilar.tex:566-592`)** — bölen sayısı **2025** ile
   tam sayı çözüm yok. Doğru değer `d(n) = (4n+1)(5n+1)`; `n=10` için **2091**.
   Kitap `20n²+9n-2024=(n-10)(20n+209)` diyor ama `(n-10)(20n+209)=20n²+9n-2090`.

3. **B13 (`13_ebob_ve_ekok.tex:572`)** — cebir yanlış. `a+c=b` ve `b-c=a`
   çıkarılırsa **`c = b-a`** çıkar (`2c = b-a` değil). Örnek `a=2,b=3,c=1`
   için `c=b-a=1` ✓, `2c=b-a` ✗.

4. **B17 (`17_invaryant_ve_monovaryant.tex:202-203`)** — "başlangıç çarpımı
   `-1` ise tümü `+1` olamaz" iddiası **yanlış**. Karşı örnek:
   `n=2024`, `i ≡ 0 (mod 8)` için `-1` (çarpım `-1`) → **8 adımda tümü `+1`**.

5. **B33 (`33_alistirmalar_sayilar_teknikler.tex:462`)** — "son sayı `0`
   olamaz" iddiası **yanlış** (2023 için). Brute-force: `1..3`, `1..7`,
   `1..11` için `0`'a ulaşılıyor. Nitekim çözümün kendisi de `2025`'e geçiyor.

6. **B36 (`36_cozumler_ve_ipuclari.tex:357,427`)** — "hiçbir nokta ikiden
   fazla ok alamaz" **yanlış**; en yakın komşu grafında üst sınır **5**'tir.
   Doğru iddia tek boyutlu (doğru üzerindeki) noktalar için geçerlidir.

### DOĞRULANAMADI — karar bekliyor (insan yargısı gerekir)

7. **B11 (`11_bolunebilme.tex:671-673`)** — önkoşul ihlali: B11'in önkoşulu
   yalnızca B1-B2 iken, çözüm Fermat'nın Küçük Teoremi'ne dayanıyor. Ancak
   FLT hiçbir yerde *tanıtılmıyor* (B12/B14'te de yok) — yani sorun "erken
   kullanım"dan çok **"hiç tanıtılmamış teoremin kullanılması"**.

8. **B26 (`26_greedy_yaklasimi.tex:271-288`)** — Kesit Özelliği ispatı
   hipotezle tutarsız: teorem "kesin olarak en küçük" diyor ama ispat
   `w(e) ≤ w(e')` yazıp `w(T') = w(T)` sonucuna varıyor; "tüm MST'lerde
   bulunma" sonucuna ulaşmıyor.

## Bağımsız tespitim — Python→C dönüşümünden kalan ETİKETSİZ UYUMSUZLUK

Kod bloklarını sözde koda/C'ye çeviren `scripts/convert_python.py` geçişinde
**blokları tanıtan metin güncellenmemiş**. Bloklar artık sözde kod (veya C)
ama metin hâlâ "Python kodu" diyor:

| Dosya:satır | Metin | Blok aslında |
|---|---|---|
| `17_invaryant_ve_monovaryant.tex:208` | "aşağıdaki Python kodunu" | sözde kod |
| `19_algoritma_nedir.tex:498` | "Python karşılığı" | sözde kod |
| `22_siralama.tex:225` | "Python ile gerçekleme" | sözde kod |
| `22_siralama.tex:382` | "Python ile gösterimi" | sözde kod (kontrol edilmeli) |
| `33_alistirmalar_sayilar_teknikler.tex:185` | "Aşağıdaki Python kodu" | **C kodu** |
| `34_alistirmalar_algoritma_c.tex:393` | "Python dilinde yazımı" | **C kodu** |

Bu, kullanıcının "kod kısmı sonra hep C/C++ olmalı" kararının doğal sonucu;
metinlerin de buna göre düzeltilmesi gerekir.

## Doğrulanmış çapraz tutarsızlıklar (Pass 2 + kendi taramam)

| Tür | Detay |
|---|---|
| Terim ikiliği | **MST**: B26 "Minimum Kapsayan Ağaç", B27 "Minimum Yayılım Ağacı", B37 "MST" |
| Terim ikiliği | **Handshaking Lemma**: B10 "El Sıkışma Lemması", B16 "Tokalaşma Lemması" |
| Terim ikiliği | **graf/çizge**: B27 "graf", B35 "çizge" |
| Kod dili | 18 kalan `fig`/`yayılım` varyantı (B26-B27, B37) |
| Tekrar | IMO 1959 (`21n+4)/(14n+3): **hem B12 hem B13** tam çözümlü |
| Tekrar | Kesik satranç tahtası: **hem B16 hem B17** |
| Tekrar | Hanoi Kuleleri: **hem B09 hem B25** |
| Referans | B36 "Bölüm 32/33/34 Çözümleri" başlıkları altındaki çözülen sorular, B32/33/34'teki alıştırmalarla birebir eşleşmiyor (bilinen yapısal mesele; D12) |

## Önerilen triyaj (uygulanmadan önce onay gerekli)

**Öncelik 1 (matematik — kullanıcı kararı):** B03, B12, B13, B17, B33, B36 kritik
matematik hataları. B03/B12/B13 mekanik düzeltilebilir; B17/B33/B36 soru
ifadesinin değişmesini gerektirir.

**Öncelik 2 (kendi tespitim):** 6 "Python kodu" etiketi → "sözde kod"/"C kodu".

**Öncelik 3 (terminoloji):** MST, Handshaking, graf/çizge tekleştirme.

**Öncelik 4 (tekrar):** IMO 1959 (B12/B13), satranç tahtası (B16/B17),
Hanoi (B09/B25) → birinde tam çözüm, diğerinde metin atfı.

**Öncelik 5 (yapısal):** B11 FLT tanıtımı, B26 kesit ispatı, B36↔B32-34 eşleşmesi.