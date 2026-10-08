#!/usr/bin/env python3
"""audit_markdown.py — LaTeX dosyalarında Markdown kalıntısı arar.

Markdown kalıntıları PDF'te görünür kusur üretir (ör. `**kalın**` yıldızlarıyla
basılır, `- madde` düz tire olur). Bu araç, `lstlisting`/`verbatim` blokları
DIŞINDA kalan Markdown kalıntılarını bulur:

  * `**kalın**` / `__kalın__`
  * satır başında `- ` veya `* ` (madde işareti)
  * satır başında `1. ` / `2. ` (numaralı liste)
  * satır başında `#` (başlık)

Kullanım:
    python3 scripts/audit_markdown.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# verbatim benzeri ortamlar: içerik ham basılır, Markdown aranmaz
VERBATIM = re.compile(r"\\begin\{(lstlisting|verbatim|minted)\}.*?\\end\{\1\}", re.S)
# matematik ortamları: içindeki "-" eksi işaretidir, madde işareti değil
MATH_ENV = re.compile(
    r"\\begin\{(array|tabular|tabular\*|tikzpicture|align|align\*|equation|equation\*|"
    r"cases|matrix|pmatrix|bmatrix|vmatrix|smallmatrix|displaymath)\}.*?"
    r"\\end\{\1\}",
    re.S,
)
# satır içi matematik: $...$ ve \( ... \)
INLINE_MATH = re.compile(r"\$[^$\n]*\$|\\\(.*?\\\)")
DISPLAY_MATH = re.compile(r"\\\[.*?\\\]", re.S)

BOLD = re.compile(r"\*\*[^*\n]{1,80}\*\*")
BULLET = re.compile(r"^\s*[-*]\s+\S", re.M)
NUMBERED = re.compile(r"^\s*\d+\.\s+\S", re.M)
HEADING = re.compile(r"^\s*#{1,6}\s+\S", re.M)
LINK = re.compile(r"\]\([^)\s]+\)")
BACKTICK = re.compile(r"(?<!`)`(?!`)[^`\n]+(?<!`)`(?!`)")
HRULE = re.compile(r"^\s*([-*_])\1{2,}\s*$", re.M)


def mask(text: str) -> str:
    """Hedef kalıpları, satır sayısını koruyarak boşlukla değiştirir."""
    def blank(m: re.Match[str]) -> str:
        return "".join("\n" if c == "\n" else " " for c in m.group(0))

    for pat in (VERBATIM, MATH_ENV, DISPLAY_MATH, INLINE_MATH):
        text = pat.sub(blank, text)
    return text


def main() -> int:
    total = 0
    for f in sorted(Path(ROOT / "output").glob("*.tex")):
        raw = f.read_text(encoding="utf-8")
        masked = mask(raw)
        raw_lines = raw.splitlines()
        masked_lines = masked.splitlines()
        if len(raw_lines) != len(masked_lines):
            print(f"[DİKKAT] hiza bozuk: {f.name}")
            continue

        findings = []
        for label, pat in (("KALIN(**)", BOLD), ("MADDE(-)", BULLET),
                           ("NUMARALI(1.)", NUMBERED), ("BASLIK(#)", HEADING),
                           ("BAGLANTI", LINK), ("GERITIRNAK", BACKTICK), ("CİZGİ(---)", HRULE)):
            for m in pat.finditer(masked):
                ln = masked[: m.start()].count("\n") + 1
                rl = raw_lines[ln - 1].strip()
                # yanlış pozitif filtresi: işaret gerçekten satırın başında mı?
                if label in ("MADDE(-)", "NUMARALI(1.)", "BASLIK(#)"):
                    first = rl[:1]
                    want = {"MADDE(-)": ("-", "*"), "NUMARALI(1.)": tuple("1234567890"),
                            "BASLIK(#)": ("#",)}[label]
                    if first not in want:
                        continue
                findings.append((ln, label, rl[:80]))

        if findings:
            print(f"--- {f.name}: {len(findings)} kalıntı ---")
            for ln, label, snip in sorted(set(findings)):
                print(f"   satır {ln:>4} [{label}] {snip}")
            total += len(findings)

    print(f"\nTOPLAM Markdown kalıntısı: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())