#!/usr/bin/env python3
"""audit_book.py — Paylaşımdan ÖNCE kitabı denetleyen kontrol aracı.

Hızlı, nesnel kontroller yapar:

1. `output/*.tex` ile `config/mufredat.md` "Bölüm → Dosya" tablosunun eşleşmesi
2. Bölüm numaralarının 1..N kesintisiz olması ve dosya adı numarasıyla uyumu
3. `\chapter{...}` başlığının müfredattaki başlıkla tutarlılığı
4. Müfredattaki alt konu sayısı ile dosyadaki `\section` sayısının karşılaştırılması
5. Tüm "Bölüm N" atıflarının geçerli aralıkta olması
6. Sayıya bağlı Türkçe ek uyumu (ör. "Bölüm 17'da" hatası)
7. Yer tutucu/uyarı izleri: TODO, FIXME, TBD, XXX, lorem, ???
8. Yasaklı terim kalıntıları (işleç, yayılım ağacı, özyineleme ...)
9. Tekrar eden örnek başlıkları (aynı klasik örnek birden çok yerde)
10. İleri referanslar (bir bölümün KENDİSİNDEN SONRAKİ bölüme atfı)

Kullanım:
    python3 scripts/audit_book.py            # tam denetim
    python3 scripts/audit_book.py --brief    # yalnız özet + kritik bulgular
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
MUFREDAT = ROOT / "config" / "mufredat.md"

VOWELS = "aeıioöuü"
BACK_VOWELS = "aıou"
UNVOICED = "çtkfhsş"
ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

FORBIDDEN_TERMS = [
    "işleç önceliği", "minimum yayılım ağacı", "özyineleme", "iki işaretçi",
    "kümülatif toplam", "bit maskesi", "bit düzeyinde", "karma tablosu",
    "öncelikli kuyruk", "ikili öbek",
    # D63: stars and bars'ın yerleşik Türkçe adı "ayraç yöntemi"dir;
    # aşağıdaki eski ad biçimleri kullanılmaz.
    "Yıldızlar ve Bölücüler", "Yıldızlar ve bölücüler", "yıldız-bölücü",
    "çubuk-yıldız", "Çubuk-Ayraç",
]
PLACEHOLDERS = ["TODO", "FIXME", "TBD", "XXX", "lorem", "LOREM", "???"]


def reading(n: int) -> str:
    if n < 10:
        return ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + (" " + ONES[ones] if ones else "")
    return str(n)


def correct_suffix(n: int, kind: str) -> str:
    word = reading(n)
    last = word[-1]
    unvoiced = last in UNVOICED
    last_vowel = next((v for v in reversed(word) if v in VOWELS), "a")
    kalin = last_vowel in BACK_VOWELS
    if kind == "loc":
        return ("ta" if kalin else "te") if unvoiced else ("da" if kalin else "de")
    if kind == "loc+ki":
        return correct_suffix(n, "loc") + "ki"
    if kind == "abl":
        return ("tan" if kalin else "ten") if unvoiced else ("dan" if kalin else "den")
    if unvoiced:
        return "a" if kalin else "e"
    if last in VOWELS:
        return "ya" if kalin else "ye"
    return "a" if kalin else "e"


def suffix_kind(s: str) -> str:
    if s.endswith("ki"):
        return "loc+ki"
    if s in ("da", "de", "ta", "te"):
        return "loc"
    if s in ("dan", "den", "tan", "ten"):
        return "abl"
    return "dat"


def parse_mufredat():
    """(numara -> (başlık, alt konu sayısı)) ve dosya tablosunu döndürür."""
    text = MUFREDAT.read_text(encoding="utf-8")
    chapters: dict[int, tuple[str, int]] = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"^### Bölüm (\d+) — (.+?) \(", line)
        if m:
            cur = int(m.group(1))
            chapters[cur] = (m.group(2).strip(), 0)
            continue
        if cur and re.match(r"^- \*\*\d+\.\d+", line):
            title, k = chapters[cur]
            chapters[cur] = (title, k + 1)
    table: dict[str, int] = {}
    for line in text.splitlines():
        m = re.match(r"^\| (\d+) \| `([^`]+)` \|$", line)
        if m:
            table[m.group(2)] = int(m.group(1))
        m = re.match(r"^\| ekler \| `([^`]+)` \|$", line)
        if m:
            table[m.group(1)] = -1
    return chapters, table


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", action="store_true")
    args = ap.parse_args()

    chapters, table = parse_mufredat()
    files = sorted(OUT.glob("*.tex"))
    issues: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    # 1/2/3/4
    seen_nums = []
    for f in files:
        m = re.match(r"^(\d+)_", f.name)
        if not m:
            issues.append(f"Dosya adı numara ile başlamıyor: {f.name}")
            continue
        num = int(m.group(1))
        seen_nums.append(num)
        if f.name not in table:
            issues.append(f"Müfredatın dosya tablosunda yok: {f.name}")
        elif table[f.name] not in (num, -1):
            issues.append(f"Tablo numarası uyuşmuyor: {f.name} (tablo={table[f.name]})")
        body = f.read_text(encoding="utf-8")
        ch = re.search(r"\\chapter\*?(?:\[[^\]]*\])?\{([^}]*)\}", body)
        if not ch:
            issues.append(f"\\chapter bulunamadı: {f.name}")
        elif num in chapters:
            want = chapters[num][0]
            got = ch.group(1).strip()
            if want.lower() != got.lower() and want.lower() not in got.lower():
                warnings.append(f"Başlık farkı: {f.name} → dosyada '{got}', müfredatta '{want}'")
        if num in chapters:
            want_sections = chapters[num][1]
            got_sections = len(re.findall(r"^\\section\{", body, re.M))
            if want_sections and got_sections != want_sections:
                warnings.append(
                    f"Alt konu sayısı: {f.name} → {got_sections} \\section (müfredatta {want_sections})"
                )

    if seen_nums != list(range(1, len(files) + 1)):
        issues.append(f"Numaralandırma kesintisiz değil: {seen_nums}")

    # 5/6/7/8/9
    refs_by_file: dict[str, list[tuple[int, int]]] = defaultdict(list)
    suffix_errors: list[str] = []
    dup_examples: dict[str, list[str]] = defaultdict(list)
    for f in files:
        body = f.read_text(encoding="utf-8")
        for i, line in enumerate(body.splitlines(), 1):
            for m in re.finditer(
                r"Bölüm(?:~|\s)(\d+)'(ya|ye|a|e|dan|den|tan|ten|daki|deki|taki|teki|da|de|ta|te)",
                line,
            ):
                n, got = int(m.group(1)), m.group(2)
                want = correct_suffix(n, suffix_kind(got))
                if want != got:
                    suffix_errors.append(f"{f.name}:{i}: Bölüm {n}'{got} → '{want}'")

        for m in re.finditer(r"Bölüm(?:~|\s)(\d+)", body):
            n = int(m.group(1))
            refs_by_file[f.name].append((n, body[: m.start()].count("\n") + 1))
            if n not in chapters:
                issues.append(f"{f.name}: geçersiz atıf → Bölüm {n}")

        for term in FORBIDDEN_TERMS:
            if term in body:
                warnings.append(f"Yasaklı terim kalıntısı: '{term}' ({f.name})")
        for ph in PLACEHOLDERS:
            if ph in body:
                issues.append(f"Yer tutucu izi: '{ph}' ({f.name})")
        for m in re.finditer(r"\\begin\{example\}(?:\[([^\]]*)\])?", body):
            if m.group(1):
                dup_examples[m.group(1).strip()].append(f.name)

    # 10: ileri referanslar
    for fname, refs in refs_by_file.items():
        src_num = int(re.match(r"^(\d+)_", fname).group(1))
        for n, ln in refs:
            if n > src_num:
                warnings.append(f"İleri referans: {fname}:{ln} → Bölüm {n}")

    for k, v in dup_examples.items():
        if len(set(v)) > 1:
            infos.append(f"Tekrar eden örnek başlığı '{k}': {sorted(set(v))}")

    print("=" * 72)
    print(f"DENETİM: {len(files)} dosya, {len(chapters)} bölüm")
    print("=" * 72)

    def dump(title: str, items: list[str], limit: int | None = None):
        print(f"\n[{title}] {len(items)} bulgu")
        for s in (items if limit is None else items[:limit]):
            print("  -", s)

    dump("KRİTİK", issues)
    dump("UYARI", warnings, limit=30 if args.brief else None)
    if not args.brief:
        dump("BİLGİ", infos)
    print(
        f"\nÖZET: kritik={len(issues)}, uyarı={len(warnings)}, "
        f"ek biçim hatası={len(suffix_errors)}"
    )
    for s in suffix_errors:
        print("  -", s)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())