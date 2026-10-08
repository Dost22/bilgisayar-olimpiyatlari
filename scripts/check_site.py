#!/usr/bin/env python3
"""check_site.py — Yayın öncesi `site/` denetimi.

Neden var: Netlify/Vercel gibi statik barındırıcılar **derleme yapmaz**; depodaki
`site/` klasörünü olduğu gibi yayımlar. `site/` depoya işlenmemişse yayın
`Deploy directory 'site' does not exist` hatasıyla düşer; içindeki bir dosya ya
da referans eksikse site kırık görünür (bkz. config/KARARLAR.md → D35).

Denetimler:

1. Zorunlu yayın dosyaları var mı? (index.html, PDF (adı `PDF_NAME`), assets/*,
   robots.txt, sitemap.xml, netlify.toml, vercel.json)
2. `index.html` içindeki tüm **yerel** referanslar karşılanıyor mu?
3. Doldurulmamış şablon yer tutucusu (`{{...}}`) kalmış mı?
4. Görseller gerçekten PNG mi? (uzantıya değil **dosya imzasına** bakılır → D34)
5. PDF'in adı `PDF_NAME` mi ve kitabın güncel derlemesi (`book_build.pdf`) ile
   birebir aynı mı? (eski adla kalan kopya da aranır → D36)
6. Depo **kökündeki** `netlify.toml` yayın klasörünü `site` olarak gösteriyor mu?
   (Netlify `netlify.toml`'yi yalnızca depo kökünden okur.)
7. `site/`, `.gitignore` ile dışlanmış mı? (Dışlanmışsa depoda yoktur → yayın düşer.)
8. İletişim bölümünde LinkedIn bağlantısı var mı? (D37)

Kullanım:
    python3 scripts/check_site.py
    python3 scripts/check_site.py --ci   # CI modu: PDF'in ikili (md5) karşılaştırması
                                         # atlanır; yerine site sayacı ile PDF sayfa
                                         # sayısı karşılaştırılır (makineye bağlı değil).
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:  # PDF adı ve LinkedIn adresi TEK KAYNAKTAN gelsin (scripts/build_site.py)
    from build_site import LINKEDIN_URL, PDF_NAME
except Exception:  # build_site içe aktarılamazsa sabit değerlerle devam et
    PDF_NAME = "bilgisayar_olimpiyatlarina_hazirlik.pdf"
    LINKEDIN_URL = "https://www.linkedin.com/in/dost-sefero%C4%9Flu-072954258"

SITE = ROOT / "site"
PDF = ROOT / "book_build.pdf"

REQUIRED = [
    "index.html",
    PDF_NAME,
    "robots.txt",
    "sitemap.xml",
    "netlify.toml",
    "_redirects",
    "vercel.json",
    "assets/style.css",
    "assets/app.js",
    "assets/favicon.svg",
    "assets/cover.png",
    "assets/og.png",
]

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# .gitignore satırı site/ (ya da site/, site/**) gibi tüm siteyi dışlıyor mu?
IGNORES_SITE = re.compile(r"^/?site(?:/?\*{0,2})?/?$|^\*$")


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def site_page_counter(html: str) -> int | None:
    """`index.html`'deki sayfa sayacını (`<b>N</b> sayfa`) okur."""
    m = re.search(r"<b>(\d+)</b>\s*sayfa", html)
    return int(m.group(1)) if m else None


def pdf_page_count(path: Path) -> int | None:
    """PDF'in sayfa sayısını döndürür; PyMuPDF yoksa None."""
    try:
        import fitz  # PyMuPDF — bkz. README (site üretimi bağımlılığı)
        with fitz.open(str(path)) as doc:
            return doc.page_count
    except Exception:
        return None


def local_refs(html: str) -> set[str]:
    """`index.html` içindeki harici olmayan (yerel) src/href hedefleri."""
    refs: set[str] = set()
    for m in re.finditer(r'(?:src|href)="([^"]+)"', html):
        url = m.group(1)
        if re.match(r"^(https?:|mailto:|#|data:)", url):
            continue
        refs.add(url.split("#")[0].split("?")[0])
    return refs


def main() -> int:
    ap = argparse.ArgumentParser(description="Yayın öncesi site/ denetimi.")
    ap.add_argument(
        "--ci",
        action="store_true",
        help="CI modu: PDF'in ikili (md5) karşılaştırması atlanır; site sayacı ile "
             "kitabın sayfa sayısı karşılaştırılır (site eskimişse kritik verir).",
    )
    args = ap.parse_args()

    issues: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    if not SITE.is_dir():
        print("KRİTİK: site/ klasörü yok → python3 scripts/build_site.py çalıştırın.")
        return 1

    index = SITE / "index.html"
    if not index.exists():
        print("KRİTİK: site/index.html yok → python3 scripts/build_site.py çalıştırın.")
        return 1
    html = index.read_text(encoding="utf-8")

    # 1) zorunlu dosyalar
    for rel in REQUIRED:
        if not (SITE / rel).exists():
            issues.append(f"eksik yayın dosyası: site/{rel}")

    # 2) yerel referanslar
    refs = local_refs(html)
    missing = [r for r in sorted(refs) if not (SITE / r).exists()]
    for ref in missing:
        issues.append(f"index.html referansı karşılanmıyor: {ref}")
    if not missing:
        infos.append(f"{len(refs)} yerel referansın tamamı karşılanıyor")

    # 3) yer tutucu
    for ph in sorted(set(re.findall(r"\{\{[^}]+\}\}", html))):
        issues.append(f"doldurulmamış şablon yer tutucusu: {ph}")

    # 4) PNG imzası (uzantıya değil içeriğe bak)
    for rel in ("assets/cover.png", "assets/og.png"):
        p = SITE / rel
        if p.exists() and p.read_bytes()[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
            issues.append(f"{rel} gerçek PNG değil (imza uyuşmuyor; bkz. KARARLAR.md → D34)")

    # 5) PDF doğru adla ve güncel mi?
    site_pdf = SITE / PDF_NAME
    if PDF.is_file() and site_pdf.is_file():
        if args.ci:
            # CI modu: PDF baytları makineye/derleyici sürümüne göre değişir, bu
            # yüzden md5 karşılaştırılamaz. Yerine "site eskimiş mi?" sorusu
            # makineden bağımsız olarak sayfa sayacıyla yanıtlanır: kitap metni
            # değişip site tazelenmemişse sayaç kitapla uyuşmaz.
            n_pdf = pdf_page_count(PDF)
            n_site = site_page_counter(html)
            if n_pdf is None or n_site is None:
                warnings.append("sayfa sayısı karşılaştırılamadı (PyMuPDF yok ya da "
                                "site sayacı okunamadı)")
            elif n_pdf != n_site:
                issues.append(f"site eskimiş: index.html {n_site} sayfa diyor, kitap "
                              f"{n_pdf} sayfa → python3 scripts/build_site.py çalıştırıp "
                              "site/ klasörünü işleyin")
            else:
                infos.append(f"site sayacı kitapla tutarlı ({n_pdf} sayfa)")
        elif md5(PDF) != md5(site_pdf):
            warnings.append("site/{}, book_build.pdf ile aynı değil → "
                            "python3 scripts/build_site.py çalıştırın".format(PDF_NAME))
        else:
            infos.append("site/{}, kitabın güncel derlemesiyle birebir aynı".format(PDF_NAME))
    legacy_pdf = SITE / "book.pdf"
    if legacy_pdf.exists():
        warnings.append("eski adla kalan PDF: site/book.pdf (D36'da adı değişti) → "
                        "python3 scripts/build_site.py çalıştırın, temizler")

    # 6) depo kökündeki netlify.toml
    root_toml = ROOT / "netlify.toml"
    if not root_toml.exists():
        issues.append("depo kökünde netlify.toml yok (Netlify onu yalnızca kökten okur) → "
                      "python3 scripts/build_site.py")
    elif not re.search(r'publish\s*=\s*"site"', root_toml.read_text(encoding="utf-8")):
        issues.append('kök netlify.toml içinde publish = "site" bulunamadı')

    # 7) .gitignore site/ klasörünü dışlıyor mu?
    gi = ROOT / ".gitignore"
    if gi.exists():
        patterns = [l.strip() for l in gi.read_text(encoding="utf-8").splitlines()]
        bad = [p for p in patterns
               if p and not p.startswith(("#", "!")) and IGNORES_SITE.match(p)]
        if bad:
            issues.append(f".gitignore site/ klasörünü dışlıyor: {bad} "
                          "(site/ depoda bulunmalıdır)")

    # 8) LinkedIn bağlantısı (iletişim bölümü)
    if LINKEDIN_URL not in html:
        warnings.append("index.html'de LinkedIn bağlantısı yok (iletişim bölümü) → "
                        "python3 scripts/build_site.py")
    else:
        infos.append("iletişim bölümünde LinkedIn bağlantısı var")

    size = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    print("=" * 72)
    print(f"YAYIN DENETİMİ: site/  ({size / 1024 / 1024:.1f} MB, "
          f"{sum(1 for f in SITE.rglob('*') if f.is_file())} dosya)")
    print("=" * 72)

    def dump(title: str, items: list[str]) -> None:
        print(f"\n[{title}] {len(items)} bulgu")
        for s in items:
            print("  -", s)

    dump("KRİTİK", issues)
    dump("UYARI", warnings)
    dump("BİLGİ", infos)
    print(f"\nÖZET: kritik={len(issues)}, uyarı={len(warnings)}")
    print("HATIRLATMA: site/ depoya İŞLENMELİDİR — barındırıcı derleme yapmaz, "
          "depodaki site/ klasörünü yayımlar (bkz. KARARLAR.md → D35).")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())