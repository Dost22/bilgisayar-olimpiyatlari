# AGENTS.md — Kitap Yazımı Talimatları

Bu dosya, projeye katkı yapacak **herhangi bir yapay zekâ ajanına** (Antigravity, Claude, Cursor vb.) yol gösterir. Bir konu yazmadan önce bu dosyayı sonuna kadar oku.

## Proje nedir?

TÜBİTAK 1. Aşama bilgisayar olimpiyatına hazırlananlar için **kavramsal, teorik ve akıcı Türkçe** bir kitap. Çıktı, LaTeX ile derlenen bir PDF'tir. Codeforces tarzı rekabetçi programlama değil; mantık, teori ve sezgi ön plandadır.

## Çalışma modeli: kırılmaz kısıtlar vs. evrimleşen sözleşmeler

Bu repo bir dogma listesi **değildir**. Kurallar iki katmana ayrılır:

**A) Kırılmaz teknik kısıtlar** — sistemin çalışması için olmazsa olmaz (çok azdır):
- `/output` içindeki dosyalar `\input` edilmiş parçalardır; `\documentclass`, `\begin{document}` vb. **içeremez**.
- Derleme `python3 scripts/compile_book.py --compiler tectonic` hatasız bitmelidir.
- `fonts/` klasöründeki TeX Gyre Cursor dosyaları kod bloklarının fontudur: tectonic'in demeti bu fontu **içermez**, şablon fontu repodaki `fonts/`'dan yükler. Bu klasörü silme/taşıma ve tectonic'i repo kökü dışından çalıştırma (bkz. `KARARLAR.md` → D51).
- Dosya adı kuralı, bölümlerin içindekilerde doğru sırayla yer almasını sağlar.

**B) Geliştirilebilir sözleşmeler** — bu dosyadaki ve `config/terminology.md`, `templates/main.tex`, `scripts/` içindeki hemen her şey:
- Bunlar birer **başlangıç varsayımıdır**, kutsal değildir. Her birinin altında bir **gerekçe** yatar (`config/KARARLAR.md` içinde kayıtlıdır).
- Daha iyi bir yol bulursan **YAP**. Şu üç şartla:
  1. `config/KARARLAR.md` dosyasına neyi ve **neden** değiştirdiğini işle.
  2. Değişikliği **kitap geneline yay**: notasyon/terim değiştirdiysen ilgili `.tex` dosyalarını, `terminology.md`'yi ve gerekirse şablonu/script'i de güncelle.
  3. Derlemeyi **yeşil tut** (hatasız bırak).

Örnek: `CTemel` dili, `language=C`'nin Türkçe babel ile çakışması yüzünden eklendi (bkz. `KARARLAR.md` → D3). Daha temiz bir çözüm bulan bunu uygular ve gerekçesini yazar.

Kısaca: **gerekçeyi gör, daha iyisini yap, kaydet, yaygınlaştır.** Buna bu talimat dosyasının kendisi de dahildir.

## Nasıl çalıştırılır?

```bash
# Derleme (kitabı oluşturur, hataları bildirir):
python3 scripts/compile_book.py --compiler tectonic

# Sadece .tex üretip derlemeden kontrol:
python3 scripts/compile_book.py --no-compile

# Derleme kaydını denetle (kritik=0 olmalı: eksik karakter, taşma, tanımsız atıf):
python3 scripts/audit_log.py --brief

# Kitap içeriğini denetle (müfredat ↔ dosya eşleşmesi, atıflar, terimler, ek uyumu):
python3 scripts/audit_book.py --brief

# Tanıtım sitesini kitaptan (book_build.pdf) yeniden üret:
python3 scripts/build_site.py
python3 scripts/build_site.py --no-images   # kapak/OG görselini yeniden üretme

# Yayın klasörünü denetle (Netlify/Vercel yayınından önce — kritik=0 olmalı):
python3 scripts/check_site.py
```

- Derleyici olarak **tectonic** kullanılır (`brew install tectonic`). pdfLaTeX de desteklenir.
- `/site` klasörü **otomatik üretilir** (kaynak: `templates/site/` + `scripts/build_site.py`); **elle düzenlenmez**. Kitap yeniden derlendikten sonra `build_site.py` çalıştırılır, içindekiler/sayfa numaraları kendiliğinden tazelenir (tek kaynak ilkesi; bkz. `KARARLAR.md` → D33).
- **Yayın statiktir:** barındırıcı (Netlify/Vercel) **derleme yapmaz**, depoda bulduğu `site/` klasörünü olduğu gibi yayımlar. Bu yüzden `site/` **depoya işlenmelidir** ve `.gitignore`'a `site/` satırı **eklenmez** (eklenirse yayın `Deploy directory 'site' does not exist` hatasıyla düşer). Depo kökündeki `netlify.toml`/`vercel.json` da `build_site.py` tarafından üretilir ve yayın klasörünü orada ilan eder — barındırıcılar ayar dosyasını yalnızca depo **kökünden** okur (bkz. `KARARLAR.md` → D35).
- `/output` içindeki tüm `.tex` dosyaları, dosya adına göre sırayla kitaba eklenir.
- `/config/mufredat.md` içindeki müfredat; bölümleri, alt konuları, önkoşulları ve sayfa bütçesini tanımlar. Her bölüm bir `.tex` dosyasıdır.

## Depo, Git ve katkı akışı (GitHub)

Bu depo **herkese açıktır**: okuyucular hata bildirir, öneri açar ve küçük
düzeltmeler için pull request gönderir. Akış üç kanaldan işler — **issue**
(bildirim/öneri), **pull request** (nesnel, küçük düzeltme) ve yalnızca yazarın
kararından sonra **ajanların yazdığı** büyük içerik. Katkı kuralları
`CONTRIBUTING.md`, bildirim formları `.github/ISSUE_TEMPLATE/` içindedir; bunlar
bu dosyayla birlikte güncel tutulur.

**Kırılmaz kısıtlar (Git ve CI):**

- `.env` **asla** sürüm kontrolüne girmez (API anahtarı taşır); `.gitignore` korur.
  `_eski_output/` (betik yedekleri) ve kökteki elle tazelenen PDF de işlenmez.
- Her gönderimde CI şu kapıları kapatır: derleme `exit 0`, `audit_log.py` kritik=0,
  `audit_book.py` kritik=0, `check_site.py --ci` kritik=0. **Yeşil olmayan değişiklik
  işlenmez**; kırmızıysa önce düzelt, sonra işle.
- `check_site.py` CI'da `--ci` modunda koşar: PDF'in ikili (md5) karşılaştırması
  makineye/derleyici sürümüne bağlı olduğu için atlanır; yerine site sayacı ile
  kitabın sayfa sayısı karşılaştırılır (site eskimişse kritik verir).
- Derleme, kitabın üretildiği **tectonic sürümüne sabitlenmiştir**
  (`.github/workflows/kitap.yml` ile `config/KARARLAR.md` → D69 birlikte güncellenir).
- `site/` **depoda bulunur**; kitap metni değiştiyse yeniden üretilip işlenir (D35).
- Karar günlüğü kuralı dış katkılar için de geçerlidir: bir sözleşme değiştiyse
  `config/KARARLAR.md`'ye kayıt eklenir; böylece dışarıdan gelen değişiklik de
  gerekçesiyle yaşar.
- Bir issue'yu düzeltirken: sayfa numarasından bölümü bul (`config/mufredat.md`
  → "Bölüm → Dosya" tablosu), metni `output/{NN}_*.tex` içinde düzelt (`site/` elle
  düzenlenmez), sonra denetimleri koştur; commit/PR metninde issue numarasına atıf yap.
- **Lisans bölünmesi (D70):** `scripts/`, `templates/`, `.github/` → **MIT**; kitap
  metni, üretilen içerik ve `site/` → **CC BY-NC-SA 4.0**. Yeni dosyaya lisans başlığı
  kopyalamayın; depo düzeyindeki ilan (`README.md` + `LICENSE`/`LICENSE-MIT`) geçerlidir.
  Üçüncü taraf metinlerin (ör. `fonts/LICENSE.txt`) kendi lisansı korunur.

## Bir bölüm (chapter) nasıl yazılır (adım adım)

1. `/config/mufredat.md` içindeki ilgili BÖLÜMÜ bul; içindeki alt konuları (`section`), önkoşulları ve sayfa bütçesini oku.
2. Dosyayı şu adla oluştur: `/output/{NN}_{slug}.tex` (NN = 2 haneli bölüm numarası). Hazır dosya adları, müfredatın "Bölüm → Dosya" tablosundadır.
3. Dosya `\chapter{Bölüm Adı}` satırıyla başlar; müfredattaki her alt konu, sırasıyla bir `\section{...}` olur. Gerekirse `\subsection` kullan.
4. Bölümün **bütün alt konularını tek dosyada**, sayfa bütçesine uyan derinlikte yaz.
5. Yazımı bitirince `python3 scripts/compile_book.py --compiler tectonic` çalıştır ve **hatasız** bittiğini doğrula. Hata varsa düzelt.

## LaTeX kuralları (kırılmaz kısıtlar + gerekçeli sözleşmeler)

- Bu dosyalar `\input` ile `/templates/main.tex` içine eklenir. Bu yüzden:
  - `\documentclass`, `\usepackage`, `\begin{document}`, `\end{document}` **YAZMA**.
  - Sadece `\chapter{...}` ile başlayan içerik yaz.
- Matematik: satır içi `$...$`, blok `\[ ... \]` veya `equation`/`align` (amsmath yüklü).
- Hazır ortamlar (numara otomatik, [chapter]'a bağlı):
  - `\begin{definition}...\end{definition}` → Tanım
  - `\begin{theorem}...\end{theorem}` → Teorem
  - `\begin{lemma}...\end{lemma}` → Önerme
  - `\begin{corollary}...\end{corollary}` → Sonuç
  - `\begin{example}...\end{example}` → Örnek
- Kod blokları:
  - Python: `\begin{lstlisting}[language=Python] ... \end{lstlisting}`
  - **C: `\begin{lstlisting}[language=CTemel] ... \end{lstlisting}`** — Yerleşik `language=C` ve `C++` Türkçe babel ile ÇAKIŞIR (bkz. `KARARLAR.md` → D3); şu anki çözüm `CTemel`.
  - **C++: `\begin{lstlisting}[language=CppTemel] ... \end{lstlisting}`** — aynı gerekçeyle C++ için özel tanım (bkz. `KARARLAR.md` → D64). C++ yalnızca kodun C ile gereksiz yere uzayacağı yerlerde kısalık için kullanılır; C öğreten bölümler (29–32) C kalır.
- Kod içinde Türkçe karakter serbest (UTF-8 / fontspec ile sorunsuz basılır).
- Düz metinde `%` karakteri kullanacaksan `\%` yaz; kod bloklarında `%` serbesttir.
- Satır içi kod: `\texttt{int}`, `\texttt{if}` gibi.
- Türkçe karakterleri doğrudan yaz (`ç, ö, ü, ş, ğ, ı, İ`). `babel[turkish]` yüklü.

## KALİTE BARAJI (en önemli kısım)

Her alt konu **en az 2–4 sayfa**, tam, derin ve öğretici olmalıdır. Kısaltılmış örnek içerik YAZMA. Bir konu şu sırayla ve bu derinlikte olmalı:

1. **Giriş / sezgi** (1–2 paragraf): Bu konu neden önemli, neyi çözer, hangi fikre dayanır.
2. **Tanımlar** (`definition`): Her terim kesin ve gerektiğinde küçük bir örnekle tanımlanmalı.
3. **Teorem / önerme / sonuç** + **ispat ya da ispat taslağı**: Sonucun NEDEN doğru olduğunu açıkla; sadece formül verme.
4. **3–5 işlenmiş örnek** (`example`): Kolaydan zora; her birinin çözümü adım adım tam yazılmış olmalı.
5. **Gerekliyse kısa kod** (`lstlisting`): C (CTemel).
6. (İsteğe bağlı) **Uyarı / not**: Sık yapılan hatalar, alternatif bakış açıları.

## TÜRKÇE KALİTESİ — çok kritik

- **Ana dili Türkçe olan usta bir yazar** gibi yaz. Makine çevirisi hissi, kopuk cümle, devrik anlatım KESİNLİKLE olmayacak.
- Bağlaç ve geçişler doğal: *dolayısıyla, öte yandan, yani, buna göre, demek ki, o hâlde*.
- Fiil çekimleri ve ekler kusursuz (`-erek/-arak`, `-den/-dan`, `-de/-da` uyumu).
- Matematik terimlerinin yerleşik Türkçe karşılıklarını kullan: *değişmez (invariant), yarı-değişmez (monovariant), güvercin yuvası ilkesi, ikili arama, taban aritmetiği* gibi.
- Cümleler uzun ve açıklayıcı olabilir, ancak hiçbir cümle belirsiz veya muğlak olmasın.

## Üslup (sistem promptu karşılığı)

> Sen TÜBİTAK 1. aşama bilgisayar olimpiyatlarına hazırlananlar için teorik, akıcı bir kitap yazan asistansın. Çıktıların kusursuz LaTeX formatında olmalı. Sadece teorik anlatım, konseptler ve C++/Python ile yazılmış kısa açıklayıcı kod blokları üret. Test case veya grader mantığına girme.

## Yapılacaklar listesi (örnek)

Her BÖLÜM için:

1. `config/mufredat.md` içindeki o bölümün **alt konularını**, önkoşulunu ve sayfa bütçesini çıkar.
2. Ajan, bölümün tamamını (tüm `\section`'larıyla) `/output/{NN}_{slug}.tex` dosyasına yazar.
3. `python3 scripts/compile_book.py --compiler tectonic` ile derle ve hatasız olduğunu doğrula.
4. `python3 scripts/audit_book.py --brief` ve `python3 scripts/audit_log.py --brief` ile denetimleri koştur (kritik=0).

> Not: Kitabın metni yazarın belirlediği müfredat ve kalite çıtasıyla üretilir; **üretim
> (generation) betikleri bu depoda bulunmaz** (bkz. `KARARLAR.md` → D71). Depoda yalnızca
> kitabın kendisi, kuralları ve derleme/denetim araçları yaşar.

---

## TERMİNOLOJİ VE NOTASYON TUTARLILIĞI (kritik)

Kitabın tamamında aynı kavram aynı adla, aynı notasyonla kullanılmalıdır.

- Mevcut sözleşme `/config/terminology.md` içindedir (yaşayan belge). Oku ve uy; ama daha iyisini bulursan değiştir, `KARARLAR.md`'ye işle ve kitap geneline yay.
- Yeni bir terim/gösterim getiriyorsan, onu `/config/terminology.md` dosyasına da **ekle** (çelişki yaratma).
- Her terimi ilk kullandığın yerde tanımla.
- Henüz tanıtılmamış bir kavrama ileri referans verme; mecbur kalırsan “Bölüm X'te göreceğiz” diye açıkça belirt.
- Kullanılacak **bölüm sırası**, `config/mufredat.md`'deki sıradır (7 kısım: I. Sıfırdan Temeller → II. Sayma → III. Sayılar Teorisi → IV. Düşünme Teknikleri → V. Algoritmik Düşünce → VI. C Programlama → VII. Alıştırma ve Ekler). Önceki bölümler, sonraki bölümlerin araçlarını kullanamaz (ör. Bölüm 11, Bölüm 14'te tanımlanan modüler aritmetiği kullanamaz).

## YAZARIN SESİ: ONAY ALINMADAN YAZILMAZ (bkz. `KARARLAR.md` → D28, D29)

`frontmatter/` içindeki **Önsöz** ve **Hakkında** ile kaptaki metinler, kitap gövdesinden farklıdır: bunlar bilgi değil, **yazarın beyanıdır** (kim olduğu, ne yaptığı, kime teşekkür ettiği).

> **Künye istisnası:** `frontmatter/kunye.tex` (kapak arkasındaki e-ISBN künyesi) yazarın sesini taşımaz; **bibliyografik veridir** ve yalnızca yazarın verdiği resmî bilgilerle (ad, e-ISBN, yayın türü/yılı) güncellenir. Buraya lisans/telif beyanı gibi **yorum** cümleleri onay alınmadan yazılmaz. Künye ve sitedeki mevcut telif/lisans beyanı (© 2026 Dost Seferoğlu · CC BY-NC-SA 4.0) **yazarın D53'te verdiği kararla onaylanmış sabit metindir**; yalnızca yazarın yeni bir kararıyla değiştirilir. ISBN **iki yerde** yaşar ve birlikte güncellenir: `frontmatter/kunye.tex` (kitap) ile `scripts/build_site.py` → `BOOK_ISBN`/`BOOK_ISBN_ISSUER` (site). Künye sayfası eklendiğinde/çıkarıldığında **tüm sayfa numaraları kayar** — derleme sonrası `python3 scripts/check_frontmatter.py 2 6 --lines` ile Önsöz/Hakkında'nın hâlâ tek sayfa olduğunu doğrulayın ve siteyi yeniden üretin.

- Bir ajan bu metinleri **doğrudan yazmaz ve değiştirmez**.
- Gerekiyorsa: kısa bir **taslak** hazırlayıp kullanıcıya sunar, **açık onay** aldıktan sonra uygular, ardından `KARARLAR.md`'ye işler.
- Yazarın emeğini tanımlarken **abartma ve yanlış atıf yapma**: bu kitap yazdırılarak (yapay zekâ araçlarıyla) oluşturulmuştur; yazarın katkısı tecrübe, **müfredatı belirlemek**, **kalite çıtasını korumak** ve **kitabı düzenlemek**tir. Metin, bu gerçeği olduğu gibi yansıtmalıdır.
- Bu dosyalarda ekleme yapılırsa **sayfa doluluğu** kısıtı vardır: Önsöz 2. sayfayı, Hakkında 3. sayfayı son satırına kadar doldurur; ekleme yapılırsa karşılığında kırpılmalı ya da en fazla 1 satır `\enlargethispage` kullanılmalıdır. Denetim: `python3 scripts/check_frontmatter.py 1 5 --lines`.

## ÖRNEKLERİ KENDİN UYDURMA — KLASİKLERİ UYARLA

Milyonlarca yüksek kaliteli kaynak var; tekerleği yeniden icat etme.

- İyi bilinen, zamansız **klasik** örnekleri ve standart problemleri kullan (örn. bukalemun problemi, güvercin yuvası örnekleri, köşeleri kesik satranç tahtası, yumurta problemi).
- Her örneği kendi sözcüklerinle **tam çöz ve açıkla**; yalnızca cevap verme.
- Bir kaynağı kelimesi kelimesine uzun uzun kopyalama. Kısa klasik problemler ve standart gerçekler serbestçe uyarlanabilir; ancak anlatım senin ve akıcı Türkçe olmalı.
- Örnekleri kolaydan zora sırala; zorluk çıtasını müfredattaki `difficulty_cap` değerine göre ayarla.

### Kaynak belirtme (yalnızca doğrudan alıntılarda)

Bunun amacı başkasının sorusunu kendimizinmiş gibi sunmamaktır; kapsamlı bir kaynakça kurmak değildir. Bu yüzden etiket **yalnızca** bir problemi doğrudan, tanınmış bir kaynaktan (olimpiyat/yarışma sorusu ya da aynen alınan klasik bulmaca) aldığında konur:

```latex
\begin{example}[Kısa Ad (Kaynak, yıl)]
```

- Olimpiyat soruları: `\begin{example}[Uluslararası Matematik Olimpiyatı 1959, Problem 1]`
- Doğrudan alınan klasik bulmacalar: `\begin{example}[Kesilmiş Satranç Tahtası (Max Black, 1946)]`

Kurallar:

- **Etiket gerekli DEĞİLDİR:** kişi adına bağlı teorem ve gerçekler (Euler, Pascal, Fermat, Lucas vb.), standart yöntemler ve herkesin bildiği klasik problemler için kaynak yazma. Bunlarla uğraşma; kitapta bunlar ortak bilgi sayılır.
- **Kaynak uydurma.** Emin olmadığın bir kaynağı yazma; emin değilsen etiketsiz bırak.
- Kaynak adı Türkçe yazılır (`Uluslararası Matematik Olimpiyatı`, `Kvant Dergisi`); özel ad ve yıllar korunur.
- Aynı problem kitapta iki kez geçiyorsa etiket her iki yerde de aynı yazılır.

## EĞİTİM KİTABI YAZIM İLKELERİ

**Öncelikli üç kural (bunlar olmadan yazma):**

- **Somut → soyut.** Elle hesaplanmış küçük örneklerle başla; okuyucunun örüntüyü kendisinin görmesini sağla, sonra genel tanımı/teoremi getir. Asla soyut bir özdeşlikle (ör. Pascal) açılış yapma.
- **Önkoşulu bilen okuyucu varsay (konuyu değil).** Okuyucu, bu bölümün ÖNKOŞUL bölümlerini (bkz. `mufredat.md`) bilir; onların ötesini bilmez. Bu bölümün konusunu sıfırdan, somuttan soyuta, her sembolü açıklayarak ve her adımı kelimelerle gerekçeleyerek anlat. Önceki bölümlere metinle atıf yap ("Bölüm 5'te gördüğümüz gibi") — bu kitabı bütünleştirir; sonraki bölümlerin kavramlarını kullanma.
- **Örnek önce, kural sonra.** Yeni bir formül/özdeşlik vermeden önce, onun ne işe yaradığını somut ve sayısal bir örnekle göster.

Aşağıdaki maddeler de bu üçüne ek olarak uygulanır:

1. **Motivasyon önce gelir.** Her bölüm “bu araç hangi problemi çözüyor, neden var?” diyerek açılmalı.
2. **Sezgi → kesinlik.** Önce fikri sezdir, sonra tanım/teorem ile kesinleştir.
3. **“Nasıl akıl ederiz?”i göster.** Örnek çözümünde yalnız çözümü değil, çözüme götüren düşünceyi de anlat (“burada toplamın paritesini izlemek akla geliyor”).
4. **Yaygın hataları işaretle.** “En sık yapılan hata …” uyarıları ekle.
5. **Tek fikir, tek bölüm.** Bir `\section` bir fikri taşısın; konuyu gereksiz yere şişirme, gerekirse alt bölüm aç.
6. **Tutarlı derinlik.** Konuyu `difficulty_cap` ayarını aşmadan ama sulandırmadan işle.
7. **Çözümlü örnek esastır.** İstersen kısa “alıştırma” ekleyebilirsin, ama asıl taşıyıcı çözümlü örneklerdir. Online judge / test case / grader formatı **yasak** (bu bir teori kitabıdır).
8. **Gerekirse görsel — ortak sözleşmeyle.** Geometrik ya da dizisel konularda açıklayıcı bir TikZ şekli faydalıysa ekle (zorunlu değil), ama **yalnızca** `templates/main.tex`'teki ortak görsel sözleşmesiyle (bkz. `KARARLAR.md` → D54): vurgu rengi `kitapvurgu`, kalıplar `dugum`/`kutu`/`kenar`/`kitap-ok`/`etiket`. Kurallar: **yönlü kenarları adlandırılmış düğümlerle ve düğümlerden SONRA** çiz (ok ucu düğüm sınırında görünsün; ham koordinat + düğümden önce çizilirse ok ucu dolgunun altında kalır); yönsüz kenarları ham koordinatla düğümlerden önce çiz; etiketleri bölgenin görsel merkezine koy, çizgilerden en az ~3pt açık bırak; `of` anahtarını yalnızca adlandırılmış düğümlerle kullan; `figure` + `\caption` ile etiketle ve metinden sözel atıf ver. Her şekil hem tectonic hem pdfLaTeX ile derlenmeli.
9. **Çapraz referans güvenli olsun.** Bölümler arası atıfta metin kullan (“Bölüm 1'de gördüğümüz gibi”); kırılgan `\ref` etiketleri yerine metin atfı tercih et.

