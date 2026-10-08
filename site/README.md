# Site klasörü — Bilgisayar Olimpiyatlarına Hazırlık

Bu klasör **otomatik üretilir**; elle düzenlemeyin. Kaynak şablonlar
`templates/site/` altında, üretici ise `scripts/build_site.py` dosyasındadır:

```bash
python3 scripts/build_site.py          # kitabı PDF'ten okuyup siteyi yeniden üretir
```

Kitap yeniden derlendikten sonra bu komutu çalıştırmak yeterlidir; içindekiler,
sayfa numaraları ve sayfa sayısı kendiliğinden güncellenir.

## İçerik

| Dosya | Açıklama |
|---|---|
| `index.html` | Tek sayfalık site: Genel Bakış, İçindekiler, Hakkında, Önsöz, Linkler, İletişim |
| `bilgisayar_olimpiyatlarina_hazirlik.pdf` | Kitabın indirilebilir nüshası (adı `build_site.py` → `PDF_NAME`) |
| `assets/style.css` | Tema (açık/koyu desteği) |
| `assets/app.js` | Sekme yönlendirmesi |
| `assets/cover.png` | Kapak görseli |
| `assets/og.png` | Paylaşım kartı (WhatsApp/X için) |
| `netlify.toml`, `vercel.json` | Yayın ayarları (yalnızca bu klasör doğrudan yayına verilirse okunur) |
| `robots.txt`, `sitemap.xml` | Arama motoru dosyaları |

Depo **köküne** ayrıca `netlify.toml` ve `vercel.json` yazılır: barındırıcılar bu
dosyaları yalnızca depo kökünden okur (`KARARLAR.md` → D35).

## Nasıl yayımlanır?

> **En kritik nokta:** Bu klasör (`site/`) **depoya işlenmiş olmalıdır.** Netlify
> derleme yapmaz; depoda bulduğu `site/` klasörünü olduğu gibi yayımlar. Klasör
> depoda yoksa yayın `Deploy directory 'site' does not exist` hatasıyla düşer.
> Bu yüzden `.gitignore` içine `site/` satırı **eklenmez**. Yayından önce
> `python3 scripts/check_site.py` ile denetleyin.

### 1) Netlify — en kolay yol (sürükle-bırak)

1. <https://app.netlify.com/drop> adresini açın.
2. Bu `site` klasörünü sayfaya sürükleyin.
3. Site birkaç saniyede yayına girer; verilen adresi paylaşabilirsiniz.

Komut satırından eşdeğeri (depo kökündeyken):

```bash
npx netlify-cli deploy --prod --dir=site
```

Adresi sonradan **Site configuration → Change site name** ile anlamlı bir
hâle getirebilirsiniz; sitenin asıl (kanonik) adresi ise özel alan adı
`bilgisayar-olimpiyatlari.com`'dur (kurulum ve DNS adımları için bkz.
`config/KARARLAR.md` → D50).

### 2) Netlify — Git deposundan

1. Depoyu GitHub'a gönderin; **`site/` klasörü de depoda bulunsun**:

   ```bash
   git add site && git commit -m "Site yayını" && git push
   ```

2. Netlify'da **Add new site → Import an existing project** ile depoyu seçin.
3. **Build command** alanını **boş** bırakın (derleme adımı yoktur).
4. **Publish directory** alanına `site` yazın; **Base directory** alanını ise
   **boş** bırakın. (Depo kökündeki `netlify.toml` yayın klasörünü zaten
   bildirir ve arayüz ayarını geçersiz kılar; base directory `site` yazılırsa
   Netlify ayar dosyasını kök yerine `site/` içinden okur ve `site/site` yolunu
   arar.)

### 3) Vercel

Depo kökündeyken:

```bash
npx vercel --prod
```

(Depo kökündeki `vercel.json`, `outputDirectory: "site"` ayarını içerir.)

Ya da Vercel panosundan depoyu içe aktarıp **Output Directory** alanına `site`
yazın. `cd site && npx vercel --prod` biçiminde yayımlayacaksanız `site/`
içindeki `vercel.json` devrededir; orada `outputDirectory` bilinçli olarak
yazılmamıştır (proje kökü zaten `site/` olur).

### 4) Kendi alan adınız

- Netlify: **Domain management → Add a domain**
- Vercel: **Settings → Domains**

Alan adını bağladıktan sonra üç yerde güncelleme yapın:
`scripts/build_site.py` içindeki `SITE_URL`, ardından siteyi yeniden üretin.

## Notlar

- Sitede harici font, CDN ya da izleme betiği yoktur; tamamı kendi dosyalarından
  çalışır. Bu yüzden intranet/çevrimdışı ortamda da sorunsuz açılır.
- İletişim, e-posta bağlantısı (`mailto:`) ile çalışır; sunucu tarafı gerekmez.
  Form istenirse Netlify Forms (`data-netlify="true"`) eklenebilir, ancak o zaman
  site yalnızca Netlify'da çalışır.
- PDF yalnızca indirme olarak sunulur; ayrıca her bölümün başlığı doğrudan ilgili
  PDF sayfasına (`bilgisayar_olimpiyatlarina_hazirlik.pdf#page=N`) bağlanır.