#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Site üretimi — Bilgisayar Olimpiyatlarına Hazırlık.

Kitabın kendisinden (book_build.pdf) ve kaynak .tex dosyalarından, hiçbir
harici bağımlılık/CDN kullanmayan TEK SAYFALIK statik bir site üretir:

    site/
      index.html          ← sekmeli tek sayfa (Genel Bakış, İçindekiler,
                            Hakkında, Önsöz, Linkler, İletişim)
      bilgisayar_olimpiyatlarina_hazirlik.pdf
                          ← kitabın kendisi (indirilebilir nüsha; adı PDF_NAME)
      assets/style.css    ← tema (açık/koyu)
      assets/app.js       ← sekme yönlendirmesi (hash tabanlı)
      assets/cover.png    ← kapak görseli (PDF 1. sayfa)
      assets/og.png       ← paylaşım kartı (1200x630)
      netlify.toml, vercel.json, robots.txt, README.md

Ayrıca DEPO KÖKÜNE de yayın yapılandırması yazılır (`netlify.toml`,
`vercel.json`). Barındırıcılar bu dosyaları yalnızca depo kökünden okur;
`site/` içindeki kopyalar yalnızca o klasör doğrudan yayına verilirse
(sürükle-bırak / "Base directory = site") geçerlidir (bkz. KARARLAR.md → D35).

Neden script: içindekiler, sayfa sayısı ve sayfa numaraları kitaptan
OTOMATİK türetilir; kitap yeniden derlendiğinde site elle güncellenmez
(tek kaynak ilkesi, bkz. config/KARARLAR.md → D33).

Kullanım:
    python3 scripts/build_site.py
    python3 scripts/build_site.py --no-images   # kapak/OG görselini yeniden üretme
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "book_build.pdf")
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
MUFREDAT = os.path.join(ROOT, "config", "mufredat.md")

BOOK_TITLE = "Bilgisayar Olimpiyatlarına Hazırlık"
BOOK_AUTHOR = "Dost Seferoğlu"
# e-ISBN: kitabın elektronik sürümüne, T.C. Kültür ve Turizm Bakanlığı
# Kütüphaneler ve Yayımlar Genel Müdürlüğü (ISBN Ajansı) tarafından verilmiştir.
# Site künyesi bu TEK KAYNAKTAN beslenir; kitaptaki künye sayfası ise
# frontmatter/kunye.tex içindedir — ikisini birlikte güncelleyin.
BOOK_ISBN = "978-625-00-5243-3"
BOOK_ISBN_ISSUER = "T.C. Kültür ve Turizm Bakanlığı · Kütüphaneler ve Yayımlar Genel Müdürlüğü"
# Telif ve lisans: kitap ücretsiz dağıtılır, telif hakkı yazarda kalır.
# Lisans: CC BY-NC-SA 4.0 (yazar kararı, bkz. KARARLAR.md → D53).
BOOK_COPYRIGHT = "© 2026 Dost Seferoğlu"
BOOK_LICENSE = "Creative Commons CC BY-NC-SA 4.0"
BOOK_LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.tr"
BOOK_FREE = "Bu kitap ücretsiz olarak dağıtılır."
BOOK_TAGLINE = "TÜBİTAK Bilgisayar Olimpiyatı 1. Aşama sınavına hazırlık için kavramsal ve çözümlü bir kaynak."
EMAIL = "dseferoglu26@ku.edu.tr"

# Yayımlanan PDF dosyasının adı — site genelinde TEK KAYNAK. İndirme düğmeleri,
# içindekiler bağlantıları (dosya#page=N) ve önbellek (Cache-Control) kuralları
# hep bu isimden beslenir. Adı değiştirmek için yalnızca burayı düzeltin.
PDF_NAME = "bilgisayar_olimpiyatlarina_hazirlik.pdf"

# Yazarın LinkedIn profili. `href` içinde yüzde kodlamalı biçim kullanılır
# (%C4%9F = "ğ" harfi): tarayıcılar ve sosyal medya kırpıcıları bunu en güvenilir
# şekilde açar. Ekranda gösterilen sürüm ise okunabilirlik için düz yazılır.
LINKEDIN_URL = "https://www.linkedin.com/in/dost-sefero%C4%9Flu-072954258"
LINKEDIN_SHOWN = "linkedin.com/in/dost-seferoğlu-072954258"
SITE_URL = "https://bilgisayar-olimpiyatlari.com"  # özel alan adı (bkz. KARARLAR.md → D50); frontmatter/kunye.tex ile birlikte güncellenir
# Eski Netlify alt adresi — özel alan adına 301 ile yönlendirilir (bkz. KARARLAR.md → D50).
NETLIFY_APP_URL = "https://bilgisayar-olimpiyatlari.netlify.app"


# --------------------------------------------------------------------------
# 1) Kitaptan veri toplama
# --------------------------------------------------------------------------
def read_outline(pdf_path: str):
    """PDF yer imlerinden içindekiler ağacını (başlık, sayfa, seviye) okur."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("Hata: PyMuPDF gerekli. Kurun: python3 -m pip install --user pymupdf")
    doc = fitz.open(pdf_path)
    outline = doc.get_toc(simple=True)
    page_count = doc.page_count
    doc.close()
    return outline, page_count


def read_part_map():
    """config/mufredat.md'den kısım (part) yapısını ve bölüm→kısım eşlemesini çıkarır."""
    part_of_chapter: dict[int, str] = {}
    parts: list[dict] = []
    current = -1
    with open(MUFREDAT, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            m = re.match(r"^##\s+KISIM\s+([IVX]+)\s+—\s+(.+?)\s*(?:\(.*)?$", line)
            if m:
                parts.append({"numeral": m.group(1), "name": m.group(2).strip(), "goal": ""})
                current = len(parts) - 1
                continue
            if current >= 0 and line.startswith("*Amaç:*"):
                parts[current]["goal"] = line[len("*Amaç:*"):].strip()
                continue
            m = re.match(r"^###\s+Bölüm\s+(\d+)\s+—", line)
            if m and current >= 0:
                part_of_chapter[int(m.group(1))] = parts[current]["numeral"]
    return parts, part_of_chapter


def read_oncelik_map() -> dict[int, str]:
    """config/mufredat.md'den bölüm→öncelik eşlemesini okur (Temel|Orta|İleri)."""
    mapping = {}
    with open(MUFREDAT, encoding="utf-8") as fh:
        for raw in fh:
            m = re.match(
                r"^###\s+Bölüm\s+(\d+)\s+—.*?öncelik:\s*(Temel|Orta|İleri)", raw.strip())
            if m:
                mapping[int(m.group(1))] = m.group(2)
    return mapping


def read_cikmis_map():
    """config/cikmis_sorular.md'den bölüm→[(yıl, [soru no, ...]), ...] eşlemesini
    ve yıl→resmî kitapçık URL'si haritasını okur."""
    path = os.path.join(ROOT, "config", "cikmis_sorular.md")
    if not os.path.exists(path):
        return {}, {}
    years: dict[int, str] = {}
    chapters: dict[int, list] = {}
    current = None
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        m = re.match(r"^-\s*(\d{4}):\s*(\S+)$", line)
        if m:
            years[int(m.group(1))] = m.group(2)
            continue
        m = re.match(r"^##\s+Bölüm\s+(\d+)\s", line)
        if m:
            current = int(m.group(1))
            chapters[current] = []
            continue
        m = re.match(r"^(\d{4})\s+(S\d+(?:,\s*S\d+)*)$", line)
        if m and current is not None:
            qs = [int(q[1:]) for q in re.split(r",\s*", m.group(2))]
            chapters[current].append((int(m.group(1)), qs))
    return chapters, years


def chapter_titles_from_source():
    """output/*.tex dosyalarından bölüm başlıklarını sırayla okur (numara = sıra)."""
    import glob
    titles = []
    for path in sorted(glob.glob(os.path.join(ROOT, "output", "*.tex"))):
        text = open(path, encoding="utf-8").read()
        m = re.search(r"\\chapter(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", text)
        titles.append(_tex_plain(m.group(1)) if m else os.path.basename(path))
    return titles


LINKS = [
    {
        "group": "Sınav ve Resmî Kaynaklar",
        "icon": "office",
        "items": [
            {
                "name": "TÜBİTAK Bilim Olimpiyatları",
                "url": "https://bilimolimpiyatlari.tubitak.gov.tr/",
                "desc": "Sınav takvimi, başvuru koşulları ve kamplar hakkındaki resmî bilgi kaynağı.",
            },
            {
                "name": "Geçmiş Sınav Soruları (TÜBİTAK)",
                "url": "https://bilimolimpiyatlari.tubitak.gov.tr/tr/gecmis-sinav-sorulari",
                "desc": "1. ve 2. aşama sınavlarının resmî soru kitapçığı ve yanıt anahtarı arşivi — konuları çıkmış sorularla ölçmek için ana kaynak.",
            },
            {
                "name": "Uluslararası Bilgisayar Olimpiyatı (IOI)",
                "url": "https://ioinformatics.org/",
                "desc": "IOI'nin resmî sitesi: yönetmelik, görev paketleri ve ülke bilgileri.",
            },
            {
                "name": "IOI İstatistikleri",
                "url": "https://stats.ioinformatics.org/",
                "desc": "Yıllara ve ülkelere göre IOI sonuçları, madalya dağılımları ve katılımcı sayıları.",
            },
        ],
    },
    {
        "group": "Alıştırma ve Değerlendirme Platformları",
        "icon": "platform",
        "items": [
            {
                "name": "Codeforces",
                "url": "https://codeforces.com/",
                "desc": "Düzenli yarışmalar, çok geniş problem arşivi ve derecelendirme sistemiyle algoritma pratiğinin en işlek adresi.",
            },
            {
                "name": "AtCoder",
                "url": "https://atcoder.jp/",
                "desc": "Başlangıç seviyesi yarışmaları (ABC) ve özenle hazırlanmış resmî çözümleriyle tanınan Japon platformu.",
            },
            {
                "name": "USACO Guide",
                "url": "https://usaco.guide/",
                "desc": "Konu konu ilerleyen, seviyelendirilmiş problem setleriyle desteklenmiş ücretsiz İngilizce rehber.",
            },
        ],
    },
    {
        "group": "Video Dersler ve Yazılı Kaynaklar",
        "icon": "play",
        "items": [
            {
                "name": "William Fiset — YouTube",
                "url": "https://www.youtube.com/@WilliamFiset-videos",
                "desc": "Graf algoritmaları, veri yapıları ve dinamik programlama üzerine ücretsiz İngilizce video dersler.",
            },
            {
                "name": "Çağatay Çebi",
                "url": "https://www.cagataycebi.com/",
                "desc": "Türkçe algoritma yazıları ve kaynak derlemeleri; olimpiyatçıların sık başvurduğu arşiv.",
            },
        ],
    },
    {
        "group": "Kitaplar",
        "icon": "book",
        "items": [
            {
                "name": "Modern Olympiad Number Theory — Aditya Khurmi",
                "url": "https://math.univ-lyon1.fr/~ducatez/content/Modern_Olympiad_TN.pdf",
                "desc": "Olimpiyat düzeyinde sayılar teorisi kitabı (Ücretsiz PDF, İngilizce). Bu kitabın sayılar teorisi kısımlarını ileri taşımak için.",
            },
        ],
    },
]


# --------------------------------------------------------------------------
# 2) Önsöz / Hakkında: LaTeX'ten okunabilir HTML'e
# --------------------------------------------------------------------------
def _strip_structure(block: str) -> str:
    """Yapısal LaTeX komutlarını ve yorum satırlarını atar."""
    lines = [ln for ln in block.split("\n") if not ln.lstrip().startswith("%")]
    text = "\n".join(lines).strip()
    text = re.sub(r"\\(chapter\*|addcontentsline|markboth|enlargethispage|clearpage)"
                  r"(\{[^{}]*\})*", "", text)
    return text.strip()


def _inline_tex_to_html(text: str) -> str:
    """Satır içi LaTeX komutlarını HTML'e çevirir (kaçış sırası önemlidir)."""
    text = html.escape(text, quote=False)
    text = text.replace("``", "\u201c").replace("''", "\u201d").replace("--", "\u2013")
    # \allowbreak görünmez bir satır kırma iznidir. Kendisinden SONRA gelen
    # boşluğu da yutar; aksi hâlde \texttt{ad@\allowbreak alan.\allowbreak tr}
    # içindeki adres "ad@ alan. tr" biçiminde boşluklu kalır ve hem görünüm
    # hem de mailto bağlantısı bozulur. (Bu yüzden \texttt'ten ÖNCE yapılır.)
    text = re.sub(r"\\allowbreak\s*", "", text)
    text = re.sub(r"\\textit\{([^{}]*)\}", r"<em>\1</em>", text)
    text = re.sub(r"\\textbf\{([^{}]*)\}", r"<strong>\1</strong>", text)
    text = re.sub(r"\\texttt\{([^{}]*)\}", r"<code>\1</code>", text)
    # Bağlantılar: \url{...} ve \href{...}{...} gerçek <a> etiketine dönüşür.
    # Sıra önemli: \texttt yukarıda işlendiği için \href'in metin argümanı
    # artık <code>...</code> olabilir ve içinde süslü parantez kalmaz.
    text = re.sub(r"\\url\{([^{}]*)\}", r'<a href="\1">\1</a>', text)
    text = re.sub(r"\\href\{([^{}]*)\}\{([^{}]*)\}", r'<a href="\1">\2</a>', text)
    text = text.replace("\\,", " ")
    text = re.sub(r"\\[a-zA-Z]+", "", text)          # kalan komutlar
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"<code>([^<]*@[^<]*)</code>", r'<a class="mail" href="mailto:\1">\1</a>', text)
    return re.sub(r"[ \t]+", " ", text).strip()


def frontmatter_paragraphs(rel_path: str) -> list[str]:
    """frontmatter/*.tex dosyasını paragraf listesine (HTML) çevirir."""
    path = os.path.join(ROOT, rel_path)
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    out = []
    for block in raw.split("\n\n"):
        text = _strip_structure(block)
        if not text:
            continue
        text = _inline_tex_to_html(text)
        if text:
            out.append(text)
    return out


def _tex_plain(text: str) -> str:
    """LaTeX kaçışlarını ekranda görünecek düz metne çevirir."""
    text = text.replace("\\'", "").replace("\\%", "%").replace("\\&", "&")
    text = text.replace("\\textbackslash", "\\").replace("~", " ")
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


# Satır içi SVG ikonlar: emoji yerine kullanılır (her platformda/headless'ta
# güvenle basılır, renk temadan miras alınır).
_ICON_PATHS = {
    "office": '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-5h6v5"/>',
    "platform": '<circle cx="12" cy="12" r="3"/>'
                '<path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2.5 2.5 0 0 0-2.5-2.5H4z"/>'
            '<path d="M20 4h-6a3 3 0 0 0-3 3v13a2.5 2.5 0 0 1 2.5-2.5H20z"/>',
}


def svg_icon(name: str) -> str:
    """Tema rengini miras alan küçük bir satır içi SVG döndürür."""
    path = _ICON_PATHS.get(name, _ICON_PATHS["book"])
    return ('<svg class="ico" viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" '
            'fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round">{}</svg>'.format(path))


# --------------------------------------------------------------------------
# 3) İçindekiler, kartlar, linkler, künye: HTML üretimi
# --------------------------------------------------------------------------
def build_chapters(outline, titles, part_of):
    """PDF yer imlerini 7 kısım / 38 bölüm ağacına dönüştürür."""
    chapters: list[dict] = []
    current = None
    last_part = ""
    for level, title, page in outline:
        if title in ("Önsöz", "Hakkında") and level == 1:
            current = None
            continue
        if level == 1:
            n = len(chapters) + 1
            src_title = titles[n - 1] if n - 1 < len(titles) else title
            part = part_of.get(n) or last_part     # ör. "Ekler" bölümü numarasız geçer
            last_part = part or last_part
            current = {"n": n, "title": src_title, "page": page,
                       "part": part, "sections": []}
            chapters.append(current)
        elif current is not None:
            if level == 2:
                current["sections"].append({"title": title, "page": page, "subs": []})
            elif level == 3 and current["sections"]:
                current["sections"][-1]["subs"].append({"title": title, "page": page})
    return chapters


def finish_pages(chapters, total_pages):
    """Her bölümün son sayfasını bir sonrakinin sayfasından türetir."""
    for i, ch in enumerate(chapters):
        nxt = chapters[i + 1]["page"] if i + 1 < len(chapters) else total_pages + 1
        ch["last_page"] = max(ch["page"], nxt - 1)


def build_toc_html(chapters, parts):
    blocks = []
    oncelik = read_oncelik_map()
    cikmis_map, cikmis_years = read_cikmis_map()
    chip_cls = {"Temel": "temel", "Orta": "orta", "İleri": "ileri"}
    for part in parts:
        chs = [c for c in chapters if c["part"] == part["numeral"]]
        if not chs:
            continue
        rows = []
        for ch in chs:
            sec_items = []
            for sec in ch["sections"]:
                subs = "".join(
                    '<li>{} <span class="pg">s. {}</span></li>'.format(esc(s["title"]), s["page"])
                    for s in sec["subs"]
                )
                subs_html = '<ul class="toc-subs">{}</ul>'.format(subs) if subs else ""
                sec_items.append(
                    '<li><a href="{f}#page={p}" target="_blank" rel="noopener"><b>{t}</b></a>'
                    ' <span class="pg">s. {p}</span>{s}</li>'.format(
                        f=PDF_NAME, p=sec["page"], t=esc(sec["title"]), s=subs_html)
                )
            if not sec_items:
                sec_items.append('<li class="pg">—</li>')
            chip = ""
            level = oncelik.get(ch["n"])
            if level:
                chip = '<span class="chip chip-{c}" title="1. Aşama önceliği">{l}</span>'.format(
                    c=chip_cls[level], l=esc(level))
            cikmis = ""
            pairs = cikmis_map.get(ch["n"])
            if pairs:
                links = []
                for year, qs in pairs:
                    label = "{} S{}".format(year, ", S".join(str(q) for q in qs))
                    url = cikmis_years.get(year)
                    if url:
                        links.append('<a href="{u}" target="_blank" rel="noopener" '
                                     'title="TÜBİTAK resmî kitapçığı ({y})">{l}</a>'.format(
                                         u=esc(url), y=year, l=esc(label)))
                    else:
                        links.append(esc(label))
                cikmis = ' · Çıkmış sorular: ' + " · ".join(links)
            rows.append(
                '<details class="toc-ch">'
                '<summary><span class="toc-num">{n}.</span>'
                '<span class="toc-name">{t}</span>{chip}'
                '<span class="toc-page">s. {a}–{b}</span></summary>'
                '<div class="toc-sections">'
                '<p class="hint"><a href="{f}#page={a}" target="_blank" rel="noopener">'
                'Bu bölümü PDF&#8217;te aç</a> · {k} alt konu{cikmis}</p>'
                '<ol>{items}</ol></div></details>'.format(
                    f=PDF_NAME, n=ch["n"], t=esc(ch["title"]), a=ch["page"],
                    b=ch["last_page"], k=len(ch["sections"]),
                    chip=chip, cikmis=cikmis, items="".join(sec_items))
            )
        part_pages = sum(c["last_page"] - c["page"] + 1 for c in chs)
        blocks.append(
            '<details class="toc-part">'
            '<summary><span class="part-numeral">{num}. KISIM</span> {name}'
            '<span class="part-meta">Bölüm {a}–{b} · {p} sayfa</span></summary>'
            '<div class="part-body"><p class="part-goal">{goal}</p>{rows}</div>'
            '</details>'.format(
                num=esc(part["numeral"]), name=esc(part["name"]),
                a=chs[0]["n"], b=chs[-1]["n"], p=part_pages,
                goal=esc(part["goal"]) or "—", rows="".join(rows))
        )
    return "\n        ".join(blocks)


def build_cikmis_html(chapters):
    """'Çıkmış Sorular' paneli: bölüm bölüm ilişkili geçmiş soruların listesi."""
    cikmis_map, cikmis_years = read_cikmis_map()
    oncelik = read_oncelik_map()
    chip_cls = {"Temel": "temel", "Orta": "orta", "İleri": "ileri"}
    if not cikmis_map:
        return '<p class="hint">Eşleme henüz eklenmedi.</p>'
    rows = []
    for ch in chapters:
        pairs = cikmis_map.get(ch["n"])
        if not pairs:
            continue
        links = []
        for year, qs in pairs:
            label = "{} S{}".format(year, ", S".join(str(q) for q in qs))
            url = cikmis_years.get(year)
            if url:
                links.append('<a class="qlink" href="{u}" target="_blank" rel="noopener" '
                             'title="TÜBİTAK resmî kitapçığı ({y})">{l}</a>'.format(
                                 u=esc(url), y=year, l=esc(label)))
            else:
                links.append(esc(label))
        chip = ""
        level = oncelik.get(ch["n"])
        if level:
            chip = '<span class="chip chip-{c}">{l}</span>'.format(
                c=chip_cls[level], l=esc(level))
        rows.append(
            '<div class="cikmis-row">'
            '<span class="toc-num">{n}.</span>'
            '<span class="cikmis-name">{t}</span>{chip}'
            '<span class="cikmis-links">{links}</span></div>'.format(
                n=ch["n"], t=esc(ch["title"]), chip=chip, links=" · ".join(links)))
    return "\n      ".join(rows)


def build_part_cards(chapters, parts):
    cards = []
    for part in parts:
        chs = [c for c in chapters if c["part"] == part["numeral"]]
        if not chs:
            continue
        cards.append(
            '<div class="card">'
            '<span class="num-badge">{num}. KISIM · BÖLÜM {a}–{b}</span>'
            '<h3>{name}</h3><p>{goal}</p></div>'.format(
                num=esc(part["numeral"]), a=chs[0]["n"], b=chs[-1]["n"],
                name=esc(part["name"]), goal=esc(part["goal"]) or "")
        )
    return "\n        ".join(cards)


def build_links_html():
    groups = []
    for group in LINKS:
        cards = []
        for item in group["items"]:
            shown = item["url"].replace("https://", "").replace("http://", "").rstrip("/")
            cards.append(
                '<a class="link-card" href="{url}" target="_blank" rel="noopener">'
                '<span class="lc-head"><span class="lc-name">{name}</span>'
                '<span class="lc-url">{shown}</span></span>'
                '<div class="lc-desc">{desc}</div></a>'.format(
                    url=esc(item["url"]), name=esc(item["name"]),
                    shown=esc(shown), desc=esc(item["desc"]))
            )
        groups.append(
            '<div class="link-group"><h3>{icon}<span>{name}</span></h3>'
            '<div class="link-list">{cards}</div></div>'.format(
                icon=svg_icon(group["icon"]), name=esc(group["group"]),
                cards="\n".join(cards))
        )
    return "\n      ".join(groups)


def build_kunye_html(chapters, parts, pages, build_date):
    sections = sum(len(c["sections"]) for c in chapters)
    rows = [
        ("Kitap adı", BOOK_TITLE),
        ("Yazar", BOOK_AUTHOR),
        ("e-ISBN", BOOK_ISBN),
        ("ISBN veren kurum", BOOK_ISBN_ISSUER),
        ("Hedef", "TÜBİTAK Bilim Olimpiyatları · Bilgisayar dalı 1. Aşama sınavı"),
        ("Kapsam", "Sayma ve kombinatorik, sayılar teorisi, düşünme teknikleri, "
                   "algoritmik düşünce, C programlama, çözümlü problemler, formül ve terim ekleri"),
        ("Yapı", "{p} kısım · {c} bölüm · {s} alt konu".format(
            p=len(parts), c=len(chapters), s=sections)),
        ("Uzunluk", "{} sayfa (B5), tek PDF dosyası".format(pages)),
        ("Anlatım dili", "Türkçe"),
        ("Önkoşul", "Yok — kitap sıfırdan başlar"),
        ("Hazırlanışı", "Yapay zekâ araçlarından yararlanılarak derlendi ve düzenlendi; "
                        "müfredat, kapsam ve kalite denetimi yazara aittir (bkz. Hakkında)"),
        ("Sürüm", "Bu sayfa {} tarihindeki derlemeden üretildi".format(build_date)),
        ("Telif", BOOK_COPYRIGHT),
        ("Lisans", BOOK_LICENSE + " — " + BOOK_LICENSE_URL),
        ("Ücret", "Ücretsizdir"),
    ]
    return "\n        ".join(
        "<tr><th>{}</th><td>{}</td></tr>".format(esc(k), esc(v)) for k, v in rows
    )


# --------------------------------------------------------------------------
# 4) Görseller (kapak + paylaşım kartı)
# --------------------------------------------------------------------------
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def _pick_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


# PNG dosya imzası (ilk 8 bayt). Üretilen görsellerin gerçekten PNG olduğunu
# doğrulamak için kullanılır; bkz. _is_png ve make_images.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _is_png(path: str) -> bool:
    """Dosyanın uzantısına değil, gerçek içeriğine bakarak PNG olup olmadığını söyler.

    PyMuPDF bir PDF *sayfasını* `.png` uzantılı yola kaydettiğinde dosya PDF
    olarak kalır (içerik `%PDF-1.7` ile başlar). Bu sessiz hata, tarayıcıda
    ve görsel yükleyen araçlarda "cannot identify image file" hatasına yol
    açar; bu yüzden üretimden sonra imza denetlenir.
    """
    try:
        with open(path, "rb") as fh:
            return fh.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE
    except OSError:
        return False


def make_images(pdf_path: str, stats_line: str) -> list[str]:
    """PDF'in 1. sayfasından kapak ve 1200x630 paylaşım kartı üretir."""
    import fitz

    notes = []
    doc = fitz.open(pdf_path)
    first = doc[0]
    cover_path = os.path.join(ASSETS, "cover.png")
    pix = first.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    pix.save(cover_path)
    notes.append("cover.png {}x{}".format(pix.width, pix.height))

    og_path = os.path.join(ASSETS, "og.png")
    width, height = 1200, 630
    og = fitz.open()
    page = og.new_page(width=width, height=height)
    page.draw_rect(fitz.Rect(0, 0, width, height), color=None, fill=(0.055, 0.42, 0.357))
    page.draw_rect(fitz.Rect(0, 0, width, 10), color=None, fill=(0.04, 0.30, 0.26))

    font_path = _pick_font()
    font = fitz.Font(fontfile=font_path) if font_path else None

    # Kapak görselini sağ tarafa oranını koruyarak yerleştir.
    cover_box = fitz.Rect(823, 90, 1140, 540)
    page.insert_image(cover_box, filename=cover_path)

    if font:
        kwargs = {"fontname": "F0", "fontfile": font_path, "color": (1, 1, 1)}

        def wrap(text, size, max_w):
            lines, line = [], ""
            for word in text.split():
                trial = (line + " " + word).strip()
                if font.text_length(trial, fontsize=size) > max_w and line:
                    lines.append(line)
                    line = word
                else:
                    line = trial
            if line:
                lines.append(line)
            return lines

        y = 150
        for line in wrap(BOOK_TITLE, 54, 690):
            page.insert_text((76, y), line, fontsize=54, **kwargs)
            y += 66
        y += 12
        page.insert_text((76, y), BOOK_AUTHOR, fontsize=27, **kwargs)
        y += 46
        page.insert_text((76, y), "TÜBİTAK Bilgisayar Olimpiyatı · 1. Aşama", fontsize=19, **kwargs)
        y += 34
        page.insert_text((76, y), stats_line, fontsize=19, **kwargs)
    else:
        notes.append("uyarı: sistem fontu bulunamadı, paylaşım kartına metin yazılmadı")

    # DİKKAT: `og` bir PDF belgesidir. Doğrudan `og.save(og_path)` çağrısı
    # dosyayı uzantıya bakmadan PDF olarak yazar: adı "og.png" olur ama içeriği
    # `%PDF-1.7` kalır. Tarayıcı, sosyal medya kartı ve görsel yükleyen araçlar
    # bu dosyayı açamaz. Bu yüzden sayfayı 1200x630 piksele raster edip (72 dpi
    # varsayılanı: 1 punto = 1 piksel) PNG olarak kaydediyoruz.
    og_pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
    og_pix.save(og_path)
    og.close()
    doc.close()

    for path in (cover_path, og_path):
        if not _is_png(path):
            raise RuntimeError(
                "{} PNG olarak yazılamadı (dosya içeriği PNG değil); "
                "görsel yükleyiciler bu dosyayı açamaz.".format(os.path.basename(path))
            )

    notes.append("og.png {}x{}".format(og_pix.width, og_pix.height))
    return notes


# --------------------------------------------------------------------------
# 5) Dosyaları yaz
# --------------------------------------------------------------------------
ROOT_NETLIFY_TOML = """# Netlify yapılandırması — Bilgisayar Olimpiyatlarına Hazırlık
# (scripts/build_site.py tarafından üretilir; elle düzenlemeyin.)
#
# Netlify `netlify.toml` dosyasını YALNIZCA depo kökünden (base directory) okur
# ve buradaki ayarlar arayüzdeki (UI) ayarları EZER. Bu yüzden yayın klasörü
# arayüze bağımlı kalmadan burada açıkça bildirilir.
#
# Site tamamen STATİKTİR: derleme adımı yoktur (command yazılmamıştır). Yayımlanan
# içerik `site/` klasörüdür ve DEPODA BULUNMAK ZORUNDADIR. Netlify kitabı
# derlemez; site yerelde `python3 scripts/build_site.py` ile üretilip depoya
# işlenir. `site/` depoda yoksa yayın
# "Deploy directory 'site' does not exist" hatasıyla düşer
# (bkz. config/KARARLAR.md → D33, D35).

[build]
  publish = "site"

# Yayın içeriği site/ klasörünün kendisidir. Depo kökünde netlify.toml olduğu
# sürece arayüzdeki "Base directory" alanı BOŞ kalmalıdır; `site` yazılırsa bu
# dosya okunmaz ve Netlify site/site yolunu arar.
#
# `__PDF__` yayımlanan PDF'in dosya adıdır (build_site.py → PDF_NAME yazarken
# yerine koyar); adı elle yazmayın ki tek kaynaktan yönetilsin.
#
# PDF, her kitap sürümünde içerik olarak DEĞİŞİR; uzun önbellek, yeni sürüm
# yayımlandığında okuyucuların eski dosyayı görmesine yol açar (bkz.
# KARARLAR.md → D52). Bu yüzden kısa süre + must-revalidate: tarayıcı/CDN
# her istekte ETag ile doğrular, güncelleme en geç 5 dakika içinde yayılır.

[[headers]]
  for = "/__PDF__"
  [headers.values]
    Cache-Control = "public, max-age=300, must-revalidate"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

# Eski *.netlify.app adresi özel alan adına yönlendirilir (bkz. KARARLAR.md → D50).
# Netlify, netlify.app alt adresini primary domaine OTOMATİK yönlendirmez
# (otomatik yönlendirme yalnızca apex ↔ www arasındadır); bu açık 301 kuralı
# eski adresin tüm bağlantılarını korur. `__APP_URL__`/`__SITE_URL__` yer
# tutucuları build_site.py tarafından doldurulur.

[[redirects]]
  from = "__APP_URL__/*"
  to = "__SITE_URL__/:splat"
  status = 301
  force = true
"""

# `site/` klasörünün İÇİNE yazılan kopya: yalnızca bu klasör doğrudan yayına
# verilirse (sürükle-bırak ya da "Base directory = site") okunur.
SITE_NETLIFY_TOML = """# Bu dosya site/ klasörünün İÇİNDEDİR: yalnızca bu klasör doğrudan yayına
# verildiğinde (sürükle-bırak ya da Netlify'da "Base directory = site") okunur.
# Depo kökünden yapılan yayında geçerli olan dosya: ../netlify.toml
#
# `publish` bilinçli olarak YAZILMAMIŞTIR: Netlify, publish belirtilmezse base
# directory'yi (yani bu klasörü) yayımlar. Böylece "Base directory = site"
# ayarında var olmayan `site/site` yolu aranmaz.

[[headers]]
  for = "/__PDF__"
  [headers.values]
    Cache-Control = "public, max-age=300, must-revalidate"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

# Eski *.netlify.app adresi özel alan adına yönlendirilir (bkz. KARARLAR.md → D50).
# Aynı kural site/_redirects dosyasında da durur; sürükle-bırak yayınında her iki
# yerden hangisi işlenirse işlensin yönlendirme sağlanır.

[[redirects]]
  from = "__APP_URL__/*"
  to = "__SITE_URL__/:splat"
  status = 301
  force = true
"""

ROOT_VERCEL_JSON = """{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": null,
  "buildCommand": null,
  "outputDirectory": "site",
  "cleanUrls": true,
  "headers": [
    {
      "source": "/__PDF__",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=300, must-revalidate" }]
    },
    {
      "source": "/assets/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    }
  ]
}
"""

# site/ içindeki kopya: `cd site && npx vercel --prod` ile yayımlanırken proje
# kökü bu klasör olur; bu yüzden `outputDirectory` YAZILMAZ (varsayılan: proje
# kökü). Yazılırsa var olmayan `site/site` klasörü aranır.
SITE_VERCEL_JSON = """{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": null,
  "buildCommand": null,
  "cleanUrls": true,
  "headers": [
    {
      "source": "/__PDF__",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=300, must-revalidate" }]
    },
    {
      "source": "/assets/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    }
  ]
}
"""


def write_site(ctx: dict) -> str:
    os.makedirs(ASSETS, exist_ok=True)
    tpl_path = os.path.join(ROOT, "templates", "site", "index.html")
    with open(tpl_path, encoding="utf-8") as fh:
        page = fh.read()
    for key, value in ctx.items():
        page = page.replace("{{" + key + "}}", value)
    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", page)))
    if leftover:
        print("  ! doldurulmamış yer tutucu: " + ", ".join(leftover))
    out = os.path.join(SITE, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)

    for name in ("style.css", "app.js", "favicon.svg", "yazar.jpg"):
        shutil.copyfile(os.path.join(ROOT, "templates", "site", name),
                        os.path.join(ASSETS, name))

    readme_src = os.path.join(ROOT, "templates", "site", "README.md")
    if os.path.exists(readme_src):
        with open(readme_src, encoding="utf-8") as fh:
            readme = fh.read().replace("__SITE_URL__", SITE_URL)
        with open(os.path.join(SITE, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(readme)

    shutil.copyfile(PDF, os.path.join(SITE, PDF_NAME))

    # PDF adı D36'da değişti; eski adla kalan dosya depoda/yayında kalmasın.
    legacy_pdf = os.path.join(SITE, "book.pdf")
    if os.path.exists(legacy_pdf) and os.path.basename(legacy_pdf) != PDF_NAME:
        os.remove(legacy_pdf)

    # Yayın yapılandırması İKİ yere yazılır ve içerikleri bilinçli olarak farklıdır:
    #   - depo kökü  : Netlify/Vercel yapılandırmayı YALNIZCA kökten okur
    #                  (publish = "site", outputDirectory = "site")
    #   - site/ içi  : yalnızca bu klasör doğrudan yayına verilirse okunur;
    #                  orada yayın kökü klasörün kendisidir, bu yüzden yol
    #                  belirtilmez (aksi hâlde var olmayan site/site aranır).
    # `__PDF__` yer tutucusu, PDF'in gerçek adıyla (tek kaynak: PDF_NAME) doldurulur.
    deploy_files = [
        (os.path.join(ROOT, "netlify.toml"), ROOT_NETLIFY_TOML),
        (os.path.join(ROOT, "vercel.json"), ROOT_VERCEL_JSON),
        (os.path.join(SITE, "netlify.toml"), SITE_NETLIFY_TOML),
        (os.path.join(SITE, "vercel.json"), SITE_VERCEL_JSON),
    ]
    for path, content in deploy_files:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content.replace("__PDF__", PDF_NAME)
                          .replace("__APP_URL__", NETLIFY_APP_URL)
                          .replace("__SITE_URL__", SITE_URL))
    # Eski *.netlify.app adresi → özel alan adı (301). Sürükle-bırak yayınında da
    # garantili işlenmesi için ayrıca `_redirects` yazılır (bkz. KARARLAR.md → D50).
    redirects = "{}/*  {}/:splat  301!".format(NETLIFY_APP_URL, SITE_URL)
    with open(os.path.join(SITE, "_redirects"), "w", encoding="utf-8") as fh:
        fh.write("# Eski *.netlify.app adresi özel alan adına yönlendirilir (bkz. KARARLAR.md → D50)\n"
                 + redirects + "\n")
    print("      yayın yapılandırması: {} (depo kökü + site/)".format(
        ", ".join(sorted({os.path.basename(p) for p, _ in deploy_files}))))

    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml\n".format(SITE_URL))
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 '  <url><loc>{}/</loc></url>\n</urlset>\n'.format(SITE_URL))
    return out


# --------------------------------------------------------------------------
# 6) Ana akış
# --------------------------------------------------------------------------
TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

LEAD_TEXT = ("Kombinatorik, sayılar teorisi, düşünme teknikleri, algoritmik düşünce ve C programlama. "
             "TÜBİTAK Bilgisayar Olimpiyatı 1. Aşama sınavına hazırlanan bir öğrenciye, hiçbir önbilgi "
             "varsaymadan sıfırdan anlatan ve çözümlü örneklerle örülmüş kapsamlı bir kaynak.")

DESCRIPTION_TEXT = ("TÜBİTAK Bilgisayar Olimpiyatı 1. Aşama sınavına hazırlık için yazılmış ücretsiz Türkçe "
                    "kitap: sayma, sayılar teorisi, algoritmik düşünce ve C programlama. Çözümlü örneklerle, "
                    "tek PDF dosyası.")


def human_size(path: str) -> str:
    return "{:.1f} MB".format(os.path.getsize(path) / (1024 * 1024)).replace(".", ",")


def main() -> None:
    parser = argparse.ArgumentParser(description="Kitaptan statik site üretir.")
    parser.add_argument("--no-images", action="store_true",
                        help="kapak ve paylaşım kartı görsellerini yeniden üretme")
    args = parser.parse_args()

    if not os.path.exists(PDF):
        sys.exit("Hata: {} bulunamadı.\nÖnce kitabı derleyin:  "
                 "python3 scripts/compile_book.py --compiler tectonic".format(PDF))

    print("[1/4] Kitap okunuyor: {}".format(os.path.relpath(PDF, ROOT)))
    outline, pages = read_outline(PDF)
    titles = chapter_titles_from_source()
    parts, part_of = read_part_map()
    chapters = build_chapters(outline, titles, part_of)
    finish_pages(chapters, pages)

    if len(chapters) != len(titles):
        print("  ! uyarı: yer imlerindeki bölüm sayısı ({}) ile kaynak dosya sayısı ({}) uyuşmuyor"
              .format(len(chapters), len(titles)))
    eksik = [c["n"] for c in chapters if not c["part"]]
    if eksik:
        print("  ! uyarı: şu bölümler bir kısma bağlanamadı: {}".format(eksik))
    if len(parts) != 7:
        print("  ! uyarı: mufredat.md'de beklenen 7 kısım yerine {} kısım bulundu".format(len(parts)))

    sub_count = sum(len(s["subs"]) for c in chapters for s in c["sections"])
    topic_count = sum(len(c["sections"]) for c in chapters)
    print("      {} bölüm · {} kısım · {} alt konu · {} alt başlık · {} sayfa".format(
        len(chapters), len(parts), topic_count, sub_count, pages))

    today = _dt.date.today()
    build_date = "{} {} {}".format(today.day, TR_MONTHS[today.month - 1], today.year)
    stats_line = "{} sayfa · {} bölüm · {} kısım · Ücretsiz".format(
        pages, len(chapters), len(parts))

    ctx = {
        "TITLE": esc(BOOK_TITLE),
        "AUTHOR": esc(BOOK_AUTHOR),
        "LEAD": esc(LEAD_TEXT),
        "DESCRIPTION": esc(DESCRIPTION_TEXT),
        "SITE_URL": esc(SITE_URL),
        "PAGES": str(pages),
        "CHAPTER_COUNT": str(len(chapters)),
        "PART_COUNT": str(len(parts)),
        "TOPIC_COUNT": str(topic_count),
        "PDF_SIZE": human_size(PDF),
        "BUILD_DATE": build_date,
        "MAIL": esc(EMAIL),
        "COPYRIGHT": esc(BOOK_COPYRIGHT),
        "LICENSE_SHORT": esc("CC BY-NC-SA 4.0"),
        "FREE": esc(BOOK_FREE),
        "MAIL_SUBJECT": "Bilgisayar%20Olimpiyatlar%C4%B1na%20Haz%C4%B1rl%C4%B1k%20%E2%80%94%20geri%20bildirim",
        "PDF_FILE": esc(PDF_NAME),
        "LINKEDIN_URL": esc(LINKEDIN_URL),
        "LINKEDIN_SHOWN": esc(LINKEDIN_SHOWN),
        "TOC": build_toc_html(chapters, parts),
        "PART_CARDS": build_part_cards(chapters, parts),
        "LINKS": build_links_html(),
        "CIKMIS": build_cikmis_html(chapters),
        "KUNYE": build_kunye_html(chapters, parts, pages, build_date),
        "ABOUT": "\n      ".join("<p>{}</p>".format(p) for p in frontmatter_paragraphs("frontmatter/hakkinda.tex")),
        "PREFACE": "\n      ".join("<p>{}</p>".format(p) for p in frontmatter_paragraphs("frontmatter/onsuz.tex")),
    }

    print("[2/4] Sayfa üretiliyor: site/index.html")
    out = write_site(ctx)

    if args.no_images and os.path.exists(os.path.join(ASSETS, "cover.png")):
        print("[3/4] Görseller korundu (--no-images)")
    else:
        print("[3/4] Görseller üretiliyor (kapak + paylaşım kartı)")
        try:
            for note in make_images(PDF, stats_line):
                print("      " + note)
        except Exception as exc:  # görsel üretimi siteyi bloklamasın
            print("      ! görsel üretilemedi: {}".format(exc))

    print("[4/4] Tamamlandı → {}".format(os.path.relpath(out, ROOT)))
    print("\nYerel deneme için:  cd site && python3 -m http.server 8000")
    print("Ardından:           open http://localhost:8000\n")


if __name__ == "__main__":
    main()