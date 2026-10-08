# Bilgisayar Olimpiyatlarına Hazırlık

TÜBİTAK **Bilgisayar Olimpiyatı 1. Aşama** sınavına hazırlananlar için yazılmış,
kavramsal ve akıcı Türkçe bir kitabın **kaynak deposu**. Kitap LaTeX ile dizilir,
`tectonic` ile derlenir ve tek bir PDF olarak yayımlanır; tanıtım sitesi de bu
depodan üretilir. Bu depo yalnızca dosyaları barındırmaz: kitabın **müfredatını**,
**terim sözleşmesini**, **kalite barajını** ve alınan kararların **gerekçelerini**
de içerir — böylece hem insanlar hem yapay zekâ ajanları aynı kurallarla çalışır.

| | |
|---|---|
| **Kitap (PDF), içindekiler, çıkmış soru eşlemesi** | <https://bilgisayar-olimpiyatlari.com> |
| **Yazar** | Dost Seferoğlu |
| **e-ISBN** | 978-625-00-5243-3 · T.C. Kültür ve Turizm Bakanlığı (ISBN Ajansı) |
| **Kapsam** | 7 kısım · 38 bölüm · ~120 alt konu · ~570 sayfa |
| **Lisans** | Kitap metni [CC BY-NC-SA 4.0](LICENSE) · araçlar [MIT](LICENSE-MIT) — kitap ücretsiz dağıtılır, satılamaz |

## Hata buldunuz mu? Bir konu mu öneriyorsunuz?

Kitabın en değerli girdisi okurun geri bildirimidir: sayfa numarasıyla gelen her
bildirim bir sonraki sürümde iz bırakır.

- 🐞 [**Hata / yazım hatası bildir**](../../issues/new?template=hata-bildirimi.yml) — sayfa numarası ve
  metnin aynen alıntısı, düzeltmeyi saniyeler içinde mümkün kılar.
- 💡 [**Konu, bölüm ya da örnek öner**](../../issues/new?template=icerik-onerisi.yml) — müfredatta
  eksik gördüğünüz yerleri yazın.
- 🛠️ [**Site ya da araç hatası bildir**](../../issues/new?template=site-ve-araclar.yml) — PDF
  bağlantıları, sayfa numaraları, derleme betikleri.
- ✍️ Küçük ve nesnel düzeltmeler için doğrudan **pull request** açabilirsiniz;
  kurallar [CONTRIBUTING.md](CONTRIBUTING.md) içindedir.

> Bildirimler Türkçe yazılırsa daha hızlı işlenir; İngilizce de kabul edilir.

## Bu kitap nasıl yazıldı?

Metin, yapay zekâ araçlarıyla — yazarın belirlediği müfredat ve kalite çıtasıyla —
üretilir; yazar metni düzenler, denetler ve onaylar. Bu yüzden depoda iki tür belge
vardır: **kitabın kendisi** ve **kitabı üreten kurallar**. Ajanlara yol gösteren
sözleşme [`AGENTS.md`](AGENTS.md), alınan kararların gerekçeli günlüğü
[`config/KARARLAR.md`](config/KARARLAR.md), içerik denetimleri `scripts/` altındadır.
Kitabın "yazarın sesi"ni taşıyan metinleri (Önsöz, Hakkında, künye) yalnızca yazara
aittir.

## Depo düzeni

| Yol | Ne var? |
|---|---|
| `output/{NN}_{slug}.tex` | Kitabın gövdesi: **38 bölüm dosyası** (bölüm sırası dosya adındadır) |
| `frontmatter/` | Önsöz, Hakkında, künye (e-ISBN) |
| `templates/main.tex` | Kitabın LaTeX şablonu (paketler, tanım/teorem ortamları, `CTemel`/`CppTemel` kod dilleri, TikZ sözleşmesi) |
| `config/mufredat.md` | **Tek kaynak:** kısımlar, bölümler, alt konular, önkoşullar, sayfa bütçesi, öncelik etiketi |
| `config/terminology.md` | **Tek kaynak:** terim ve notasyon sözleşmesi |
| `config/KARARLAR.md` | Karar günlüğü (D1…): ne, neden, hangi dosyalar etkilendi |
| `scripts/` | Derleme, denetim ve site üretim araçları (`compile_book.py` ile başlayın) |
| `fonts/` | Kod bloklarının fontu (TeX Gyre Cursor, GUST Font License — derleme için **gereklidir**) |
| `site/` | Yayımlanan statik site — **otomatik üretilir**, elle düzenlenmez, depoda bulunmalıdır |
| `reports/` | Denetim kayıtları ve doğrulama notları |

## Derleme

Gereksinimler:

```bash
brew install tectonic        # TeX derleyicisi (tek komut; paketleri kendi indirir)
pip install PyMuPDF          # yalnızca site üretimi için
brew install ghostscript     # yalnızca sayfa düzeni denetimi için (check_frontmatter.py)
```

Kitabı derleyin ve denetleyin (komutlar **depo kökünden** çalıştırılır):

```bash
python3 scripts/compile_book.py --compiler tectonic   # → book_build.pdf
python3 scripts/audit_log.py --brief                  # derleme kaydı kapısı
python3 scripts/audit_book.py --brief                 # içerik denetimi (müfredat, atıflar, terimler)
python3 scripts/build_site.py                         # kitaptan siteyi yeniden üretir
python3 scripts/check_site.py                         # yayın öncesi site denetimi
python3 scripts/check_frontmatter.py 2 6 --lines       # Önsöz/Hakkında sayfa düzeni
```

## Değişiklik akışı

Yeni bir bölüm ya da alt konu yazacak ajan, sırasıyla şu üç kaynağı okur:
[`config/mufredat.md`](config/mufredat.md) (o bölümün alt konuları, önkoşulu ve
sayfa bütçesi), [`AGENTS.md`](AGENTS.md) (yazım kuralları ve kalite barajı) ve
[`config/terminology.md`](config/terminology.md) (terim/notasyon sözleşmesi).
Metin doğrudan `output/{NN}_{slug}.tex` dosyasına yazılır; ardından derleme ve
üç denetim koşar.

## Lisans ve üçüncü taraf bileşenler

Depo **çift lisanslıdır**: kitabın metni korunur, araçlar serbest bırakılır.

| Kapsam | Lisans | Dosya |
|---|---|---|
| **Kitap metni ve yayımlanan içerik** — `output/`, `frontmatter/`, `config/`, `reports/`, `site/`, kök Markdown dosyaları | **CC BY-NC-SA 4.0** | [`LICENSE`](LICENSE) |
| **Araçlar ve şablonlar** — `scripts/`, `templates/`, `.github/` | **MIT** | [`LICENSE-MIT`](LICENSE-MIT) |

Kitabın metni **CC BY-NC-SA 4.0** altındadır:

- **BY** — kaynak belirtilmelidir (*Bilgisayar Olimpiyatlarına Hazırlık*, Dost Seferoğlu),
- **NC** — ticari kullanım yasaktır; kitap satılamaz,
- **SA** — türev çalışmalar (çeviri, ders notu, uyarlama) aynı lisansla paylaşılmalıdır.

Araçlar ise **MIT** altındadır: derleme/site/denetim betiklerini ve şablonları
kendi projenizde özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz
(yalnızca telif satırını koruyun). Ayrımın gerekçesi `config/KARARLAR.md` → D70'te
kayıtlıdır.

Ayrıca:

- `fonts/` altındaki TeX Gyre Cursor fontları **GUST Font License** altındadır
  (`fonts/LICENSE.txt`); bu deponun lisanslarından bağımsızdır.
- Çıkmış sınav soruları yalnızca **bağlantı** olarak gösterilir; soru metinlerinin
  hakları TÜBİTAK'a aittir.
- Yazar fotoğrafı (`templates/site/yazar.jpg`) yalnızca tanıtım sitesinde kullanılır.