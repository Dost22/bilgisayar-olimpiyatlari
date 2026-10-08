<!-- Başlık önerisi: "Bölüm 14: yazım düzeltmesi" · "check_site: eksik dosya denetimi" -->

## Ne değişiyor?

<!-- Kısa ve nesnel anlatım. Değişen dosyaları listeleyin. -->

## Neden?

<!-- Gerekçe: hangi hata, hangi sözleşme ihlali, hangi sayfa/issue? -->

## Değişikliğin türü

- [ ] Küçük, nesnel düzeltme (yazım, terim, kod, dizgi)
- [ ] Site ya da araç düzeltmesi
- [ ] Sözleşme değişikliği (kural / terim / müfredat) — `config/KARARLAR.md` kaydı eklendi
- [ ] Diğer (issue: #<!-- numara -->)

## Kontrol listesi

- [ ] Kitap derleniyor: `python3 scripts/compile_book.py --compiler tectonic` (exit 0)
- [ ] `python3 scripts/audit_log.py --brief` → kritik=0 (taşma, eksik karakter yok)
- [ ] `python3 scripts/audit_book.py --brief` → kritik=0
- [ ] `python3 scripts/check_site.py` → kritik=0 (kitap metni değiştiyse `python3 scripts/build_site.py` çalıştırıldı ve `site/` işlendi)
- [ ] Terim ve notasyon `config/terminology.md` ile tutarlı; müfredatla çelişki yok
- [ ] Metin bölüm dosyasındaysa: `\documentclass`/`\usepackage`/`\begin{document}` yok; kod blokları `CTemel`/`CppTemel`
- [ ] `frontmatter/` (Önsöz, Hakkında, künye) dosyalarına dokunulmadı
- [ ] Değişiklik tek konulu; dosya baştan sona yeniden biçimlendirilmedi (gürültüsüz diff)