# Round-2 Uygulama Durumu

Tarih: 19 Eylül 2026 · Kitap: **561 sayfa**, 37 bölüm, derleme **exit 0** (0 hata,
0 eksik karakter), overfull 12 (hepsi ≤6.3pt, kozmetik).

## ✅ UYGULANDI (kitaba işlendi)

### 1. Mekanik düzeltmeler — `scripts/fix_literal.py` (deterministik, API'siz)

| Düzeltme | Adet | Dosya |
|---|---|---|
| C kod bloklarında kayıp `#` geri kondu (`include <...>` → `#include <...>`, `define` → `#define`) | **53** | 15 |
| `işleç` → `operatör` (Türkçe ekleri koruyarak; `işlecinin`→`operatörünün`) | **8** | 5 |

Doğrulama: kalan `işleç` kökü **0**; 53 satırın tamamı `lstlisting` içinde; derleme
yeşil. Yedek: `_eski_output/literal_backup_20260919_*`.

### 2. `scripts/fix_literal2.py` — mekanik (deterministik, API'siz)

**34 (`old`,`new`) çifti + 2 satır aralığı düzeltmesi**, 13 dosyada. Çiftler
`fix_literal2_pairs.py` (+ `..._b26.py`) içindedir; her çiftin `old` metni dosyada
tam 1 kez geçmezse hiçbir dosya yazılmaz.

| Konu | İçerik |
|---|---|
| **prefix sums** | B21 (11 yer: bölüm/alt bölüm başlıkları, tanımlar, caption, özet) + B35 (3) + B36 (2): "kümülatif toplam" → "prefix sums" |
| **two pointers** | B21 (3) + B34 (1): "İki İşaretçi (Two Pointers)" → "Two Pointers" |
| **rekürsiyon** | B34: "Özyineleme yığını" → "Rekürsiyon yığını"; B13 C yorumu → `Rekursif yontem` |
| **greedy** | B22 (1), B26 (1), B27 (2): "Açgözlü/açgözlülük" → "Greedy" |
| **Yanlış atıflar** | B11: "Bölüm 1'deki İyi Sıralama İlkesi" → "Bölüm 18'deki İyi Sıralılık İlkesi"; B24: "Bölüm 19'daki fonksiyon çağrıları" → "Bölüm 29'da göreceğimiz" |
| **B26 Kesit Özelliği ispatı** | "kesin en küçük" hipotezi kullanılarak **çelişkiyle** bitirildi ($w(T') < w(T)$  çelişki). Eski ispat yalnız $w(T')=w(T)$ deyip teoremin iddiasına ulaşmıyordu |
| **B35 formül üst sınırı** | $\sum_{k=0}^{2n-1} \to \sum_{k=0}^{n}$ (brute-force ile $n=2..7$ doğrulandı) |
| **Bézout / Genişletilmiş Öklid** | **İçerik EKLENMEDİ** (kullanıcı kararı: kapsam dışı). Yalnız tanıtılmamış kavram atıfları temizlendi: B36 (2 yer), B37 (Ekler maddesi silindi), B13 (kapanış ibaresi çıkarıldı) |
| **B11 palindrom indeksleri** | Basamak indeksleri $k-m$ ve $k-1+m$ olarak düzeltildi (eskiden $m-1$ / $2k-m$ ile tutarsızdı) |
| **B16 at turu (YANLIŞ iddia)** | Örnek **kapalı tur** biçimine çevrildi; ispat parite sayımıyla ($13$ siyah / $12$ beyaz). Eski metin "$(1,1)\to(5,5)$ turu yoktur" diyordu; oysa **vardır** |
| **B17 monovaryant** | Yanlış potansiyeller ve geçersiz "sonlu permütasyon" argümanı kaldırıldı. Yerine **1986 IMO S3 (beşgen) tamsayı versiyonu** + **pentagram potansiyeli** $\Phi=\frac12\sum(x_i-x_{i+2})^2$, $\Delta\Phi=-tS$ (19.246 hamlede sıfır uyuşmazlık) |
| **B17 örnek/çözüm uyuşmazlığı** | "Taş eksiltme" örneği, çözümüyle uyumlu **doldurma (bootstrap) problemi** biçimine çevrildi; çevre ($P$) yarı-değişmeziyle $m \ge 8$ alt sınırı kanıtlandı |

### 3. Sözleşme güncellemeleri

- `config/terminology.md`
  - `stack`, `queue`, `set`, `map` **yasak listesinden çıkarıldı** (Türkçe
    karşılıkları yerleşik); başlıklarda `Stack (Yığın)` gibi çift gösterim serbest.
  - Yeni "Yazım tercihleri" bölümü: **`operatör` kullanılır, `işleç` KULLANILMAZ.**
  - `Fermat's Little Theorem` satırı eklendi (Bölüm 14'te ispatlanır).

## ⏸ KARAR BEKLEYENLER

| Konu | Durum |
|---|---|
| **Tekrar eden klasik örnekler** | IMO 1959 (B12+B13), kesik satranç (B16+B17), Hanoi (B09+B25), $n \mid 2^n-1$ (B11 örneği + B33 alıştırması). **Editoryal karar bekliyor**: hangisinde tam çözüm kalsın, hangisi kısa atfa dönüşsün? |
| **B36'daki $42x + 55y = 1$ egzersizi** | Bir **lineer Diyofant denklemi**dir; Diyofant'ı kapsam dışı bıraktığımıza göre bu egzersiz de kaldırılmalı mı? (Şu an yalnız "Bézout / Genişletilmiş Öklid" adları temizlendi; egzersizin kendisi duruyor.) |
| **Bézout içeriği** | Kullanıcı kararı: **eklenmeyecek** (kapsam dışı). |

## 🔧 Tekrar çalıştırma

```bash
python3 scripts/fix_literal.py --check                            # 1. dalga denetimi
python3 scripts/fix_literal2.py --check                           # 2. dalga denetimi
python3 scripts/fix_literal2.py                                   # 2. dalga uygula + derle
python3 scripts/fix_literal2.py --module fix_literal2_pairs_b26   # yalnız B26 ispatı
python3 scripts/fix_findings.py P16 --dry-run                     # Gemini görevleri (kredi gerekir)
```

Yedekler: `_eski_output/literal_backup_*`, `_eski_output/literal2_backup_*`,
`_eski_output/r2fix_backup/`.### 4. R3 — Tekrar temizliği + Diyofant egzersizinin atılması

`scripts/fix_literal2_pairs_r3.py` ve `..._r4.py` ile uygulandı:

| Değişiklik | Ayrıntı |
|---|---|
| **B36: Lineer Tam Sayı Denklemleri alt bölümü ATILDI** | 61 satır (228-288) silindi. **Gerekçe:** $42x+55y=1$ bir lineer Diyofant denklemidir; Diyofant konusu kitaptan çıkarılmıştır (D13) ve bu alt bölüm B32/33/34'teki hiçbir alıştırmaya karşılık gelmiyordu (orphan çözüm). |
| **IMO 1959 tekrarı giderildi** | B12'de problem ifadesi + **B13'e ileri atıf** kaldı (tam çözüm B13'te, Öklid'in doğal yeri). B12'nin çözümü (lineer kombinasyon yöntemi) kaldırıldı. |
| **Kesilmiş satranç tahtası tekrarı giderildi** | B16'da tam çözüm (parite) kaldı; B17'deki uzun çözüm **kısa, değişmez-odaklı** sürüme indirildi (B16'ya atıfla). |
| **Hanoi tekrarı giderildi** | B09'da modelleme kaldı; B25'in çözümüne "$H_n = 2H_{n-1}+1$ bağıntısını Bölüm 9'da elde etmiştik" atfı eklendi. |
| **$n \mid 2^n-1$ tekrarı giderildi** | B33'te alıştırma kaldı; B11'deki çözümlü örnek, **$n^3-n$'in $6$'ya bölünmesi** ile değiştirildi (B11'in kendi aracını kullanır). Böylece B11'deki Fermat ileri referansı da ortadan kalktı. |

Sonuç: **561 → 558 sayfa**, derleme `exit 0`, 0 hata, 0 eksik karakter.

---

## YAPISAL KONU — ÇÖZÜLDÜ (D22)

**B36 ile B32/33/34 arasındaki ilişki netleşti ve etiketler dürüstleştirildi.**

İnceleme sonucu:
- **B32, B33, B34 üçü de kendi alıştırmalarını SATIR İÇİ tam çözüyor** (12 + 12 + 15 = 39 çözüm; hepsi `\begin{proof}[Çözüm]`).
- **B36 ise onların sorularını çözmüyor**; **bağımsız** bir ek problem seti çözüyor (7 basamaklı sayılar, örten fonksiyonlar, $x_1+\dots+x_4=18$, $2^{2026}+3^{2026} \bmod 7$, $1..20$ tahtası ...).

Seçilen çözüm (kullanıcı kararı: seçenek 1) — **yeniden adlandırma**:

| Eski | Yeni |
|---|---|
| `\chapter{Çözümler ve İpuçları}` | `\chapter{Ek Çözümlü Problemler ve İpuçları}` |
| `\section{Bölüm 32 Çözümleri: İleri Sayma ve Kombinatorik}` | `\section{Ek Problemler: İleri Sayma ve Kombinatorik}` |
| `\section{Bölüm 33 Çözümleri: Sayılar Teorisi ve Problem Çözme Teknikleri}` | `\section{Ek Problemler: Sayılar Teorisi ve Problem Çözme Teknikleri}` |
| `\section{Bölüm 34 Çözümleri: Algoritmalar ve C Programlama}` | `\section{Ek Problemler: Algoritmalar ve C Programlama}` |

Ayrıca B36'nın giriş paragrafı düzeltildi (o bölümlerin çözüm kiti olduğu iddiası yanlıştı) ve
`config/mufredat.md`'deki B36/B32 tanımları güncellendi. İçerik değişmedi; yalnız etiketler
içerikle uyumlu hâle getirildi. **Kitapta başka yerde "Bölüm 36" atfı yok**, dolayısıyla
düzeltme gereken atıf çıkmadı.

**Reddedilen alternatif:** B32–34'ün satır içi çözümlerini kaldırmak. B36 o soruları
çözmediği için 39 alıştırma çözümsüz kalırdı.

## 🔧 Tekrar çalıştırma

```bash
python3 scripts/fix_literal.py --check                              # 1. dalga
python3 scripts/fix_literal2.py --check                             # 2. dalga
python3 scripts/fix_literal2.py --module fix_literal2_pairs_r3      # R3 (tekrar + Diyofant)
python3 scripts/fix_literal2.py --module fix_literal2_pairs_r4      # R4 (B17 satranç)
python3 scripts/fix_literal2.py --module fix_literal2_pairs_r5      # R5 (B36 etiketleri)
python3 scripts/fix_findings.py P16 --dry-run                       # Gemini görevleri (kredi gerekir)
```

Yedekler: `_eski_output/literal_backup_*`, `_eski_output/literal2_backup_*`,
`_eski_output/r2fix_backup/`.
