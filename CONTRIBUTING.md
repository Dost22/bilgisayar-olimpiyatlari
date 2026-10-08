# Katkı Rehberi

Bu kitabı okuduğunuz için teşekkürler. Kitap, okurun geri bildirimiyle büyür:
bulunan her hata, anlaşılmayan her paragraf bir sonraki sürümde iz bırakır. Bu
dosya, katkının hangi kanaldan ve hangi kurallarla ilerlediğini anlatır.

## Önce şunu bilin: bu kitap nasıl yazılıyor?

Kitabın metni elle yazılmaz; **yazarın belirlediği müfredat ve kalite çıtasıyla
yapay zekâ ajanları** tarafından yazılır, yazar düzenler ve onaylar. Bunun iki
sonucu vardır:

- Kitabın **sesi**, **derinliği** ve **terimleri** tek elden korunur; bu yüzden
  hazır uzun metinler (bölüm, alt konu, paragraf) doğrudan kitaba girmez.
- Buna karşılık **bildirimler** en değerli katkıdır: iyi bir bildirim, ajanın
  yazacağı düzeltmenin gerekçesidir. Sayfa numarasıyla gelen bir hata bildirimi
  çoğu zaman bir düzeltme yamasından daha faydalıdır.

## Hangi kanal, hangi katkı?

| Katkınız | Nereye? | Kim uygular? |
|---|---|---|
| Yazım, hesap, atıf, dizgi hatası | [Hata bildirimi](../../issues/new?template=hata-bildirimi.yml) | yazar + ajan |
| Yeni konu, bölüm ya da örnek önerisi | [İçerik önerisi](../../issues/new?template=icerik-onerisi.yml) | yazar karar verir, ajan yazar |
| Site ya da araç hatası | [Site / araç hatası](../../issues/new?template=site-ve-araclar.yml) veya doğrudan PR | katkıcı veya yazar |
| Küçük, nesnel düzeltme | **Pull request** | katkıcı |

Kitabın güncel sürümü <https://bilgisayar-olimpiyatlari.com> adresindedir;
bildirimden önce oraya bakmak, düzeltilmiş bir hatayı yeniden bildirmenizi önler.

## Pull request ile katkı

Doğrudan kabul edilen katkılar **nesnel** olanlardır. Ölçüt, "bence daha iyi olur"
değil, "yanlış" ya da "sözleşmeyle çelişiyor" diyebilmektir:

- **Yazım ve dil:** yazım hatası, ek uyumu, bozuk cümle, tutarsız büyük/küçük harf.
- **Matematik:** hesap hatası, eksik ya da yanlış ispat adımı, yanlış cevap.
- **Atıf:** yanlış bölüm numarası, var olmayan alt konuya gönderme, kayan sayfa numarası.
- **Dizgi:** LaTeX hatası, bozuk tablo ya da şekil, kod bloğunun dil etiketi.
- **Araçlar:** `scripts/` altındaki betiklerde ve `templates/` içinde hata.

Her PR için geçerli kurallar:

1. **Tek konu.** Bir PR bir işi yapar; biçimlendirme gürültüsü üretmez.
2. **Kırılmaz kısıtlar.** `output/*.tex` dosyaları `\documentclass`, `\usepackage`
   ya da `\begin{document}` içermez. Kod blokları C için `CTemel`, C++ için
   `CppTemel` dilini kullanır (yerleşik `C`/`C++` Türkçe babel ile çakışır).
3. **Yazarın sesi dokunulmaz.** `frontmatter/onsuz.tex`, `frontmatter/hakkinda.tex`
   ve `frontmatter/kunye.tex` yalnızca yazara aittir; PR ile değiştirilmez.
4. **Tek kaynak ilkeleri.** Müfredat `config/mufredat.md`, terim ve notasyon
   `config/terminology.md` dosyalarından gelir; bu iki dosyayla çelişen değişiklik
   yapılmaz. Bir sözleşmeyi değiştirmeniz gerekiyorsa önce o dosyayı güncelleyin,
   sonra kitabı ona uydurun.
5. **Kalite barajı.** Yeni ya da yeniden yazılan metin, `AGENTS.md` içindeki yazım
   kurallarına (somuttan soyuta, çözümlü örnek, terim tutarlılığı) uyar.
6. **Karar günlüğü.** Bir kural, terim ya da yapıyı değiştirdiyseniz
   `config/KARARLAR.md` dosyasına yeni bir kayıt ekleyin: ne değişti, neden,
   hangi dosyalar etkilendi, eski davranış neydi. Bu depoda kararlar gerekçesiyle yaşar.

## Kabul edilmeyen katkılar

- Test case, grader, online judge çıktısı ya da çözüm denetimi (bu bir **teori**
  kitabıdır; alıştırmalar kâğıt üzerinde çözülür).
- Kaynağı belirsiz alıntılar, uydurma kaynak etiketleri, uzun birebir kopyalar.
- Kitabın sesini taklit eden, kalite barajını atlayan metin eklemeleri.
- Kapsam dışı ileri konular (2. Aşama odaklı veri yapıları ya da kitapta yer alması
  kararlaştırılmamış kavramlar).
- Tüm dosyayı yeniden akıtan, satır sonlarını değiştiren "biçimlendirme" PR'ları.

## Yerel kurulum ve doğrulama

Gereksinimler:

```bash
brew install tectonic ghostscript   # derleyici + sayfa düzeni denetimi
pip install PyMuPDF                 # site üretimi ve site denetimi
```

PR göndermeden önce, **depo kökünden**:

```bash
python3 scripts/compile_book.py --compiler tectonic   # derleme → book_build.pdf (exit 0 olmalı)
python3 scripts/audit_log.py --brief                  # derleme kaydı: kritik=0 olmalı
python3 scripts/audit_book.py --brief                 # içerik: kritik=0 olmalı
python3 scripts/build_site.py                         # kitap metni değiştiyse mutlaka!
python3 scripts/check_site.py                         # site: kritik=0 olmalı
```

Bu denetimlerin tamamı her pull request'te GitHub Actions ile otomatik koşar
(`.github/workflows/kitap.yml`). Derleme, kitabın üretildiği **tectonic sürümüne**
sabitlenmiştir; sürümü yükseltmek isterseniz iş akışındaki sürümü ve
`config/KARARLAR.md` kaydını birlikte güncelleyin. `check_site.py` CI'da `--ci`
modunda çalışır (PDF baytları derleyici sürümüne göre değiştiği için ikili
karşılaştırma yerine sayfa sayısı karşılaştırılır).

## Üslup ve iletişim

- Bildirim ve PR metinlerini **Türkçe** yazmanız tercih edilir; İngilizce de kabul edilir.
- Eleştiri kitaba yönelik olsun, kişiye değil. "Bu cümle anlaşılmıyor, çünkü..."
  biçimindeki bildirimler en hızlı sonuç verenlerdir.
- Bir değişikliğin kapsamı tartışmalıysa PR açmak yerine önce issue açıp sorun:
  yazarın kararı beklenmeden yapılan kapsamlı değişiklikler geri çevrilebilir.

## Lisans

Bu depo **çift lisanslıdır** (bkz. `config/KARARLAR.md` → D70):

- Kitap metni, üretilen içerik ve site → **CC BY-NC-SA 4.0** ([`LICENSE`](LICENSE)).
- Araçlar ve şablonlar (`scripts/`, `templates/`, `.github/`) → **MIT**
  ([`LICENSE-MIT`](LICENSE-MIT)).

Katkı sağladığınızda, katkınızın dokunduğu alanın lisansıyla (içerik → CC BY-NC-SA 4.0,
araç → MIT) paylaşılmasını kabul etmiş olursunuz: **gelen katkı, giden lisansla aynı
koşullara tabidir.** `frontmatter/` altındaki "yazarın sesi" metinleri ve yazar
fotoğrafı yalnızca yazara aittir; lisans kapsamı dışında ayrıca izin gerektirir.