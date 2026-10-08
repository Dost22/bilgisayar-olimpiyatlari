#!/usr/bin/env python3
"""audit_lists.py — LaTeX dosyalarında "çıplak liste" (Markdown tarzı) satırları sınıflar.

Sınıflar:
  [ITEMIZE İÇİ]  satır zaten bir itemize/enumerate içinde → `- ` yerine `\\item` olmalı
  [ÇIPLAK]       normal metinde `- ` ile başlıyor → `itemize` ortamına çevrilmeli
  [KALIN(**)]    `**...**` → `\\textbf{...}` olmalı

Yalnızca rapor üretir (düzeltme yapmaz).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERBATIM = re.compile(r"\\begin\{(lstlisting|verbatim|minted)\}.*?\\end\{\1\}", re.S)
MATH_ENV = re.compile(r"\\begin\{(array|tabular|tikzpicture|align|equation|cases|matrix|"
                      r"pmatrix|bmatrix|vmatrix|smallmatrix)\*?\}.*?\\end\{\1\*?\}", re.S)
INLINE_MATH = re.compile(r"\$[^$\n]*\$")
DISPLAY_MATH = re.compile(r"\\\[.*?\\\]", re.S)
LIST_BEGIN = re.compile(r"\\begin\{(itemize|enumerate)\}")
LIST_END = re.compile(r"\\end\{(itemize|enumerate)\}")
BULLET = re.compile(r"^(\s*)[-*]\s+(\S.*)$")
BOLD = re.compile(r"\*\*([^*\n]{1,120})\*\*")


def blank(m: re.Match[str]) -> str:
    return "".join("\n" if c == "\n" else " " for c in m.group(0))


def main() -> int:
    grand = {"itemize": 0, "ciplak": 0, "kalin": 0, "dosya": 0}
    for f in sorted(Path(ROOT / "output").glob("*.tex")):
        raw = f.read_text(encoding="utf-8")
        masked = raw
        for pat in (VERBATIM, MATH_ENV, DISPLAY_MATH, INLINE_MATH):
            masked = pat.sub(blank, masked)

        depth = 0
        in_item = 0
        ciplak = 0
        raw_lines = raw.splitlines()
        masked_lines = masked.splitlines()
        if len(raw_lines) != len(masked_lines):  # hizalama bozuksa güvenli tarafta kal
            print(f"[DİKKAT] satır hizası bozuk: {f.name}")
            continue

        for i, ml in enumerate(masked_lines):
            for _ in LIST_BEGIN.finditer(ml):
                depth += 1
            # Yalnızca maskesiz (dokunulmamış) satırlarda madde işareti ara:
            # aksi hâlde matematikteki "-" işareti yanlış pozitif üretir.
            rb = BULLET.match(ml)
            if rb and raw_lines[i].lstrip()[:1] not in ("-", "*"):
                rb = None  # yanlış pozitif: "-" maskelenmiş matematikten geliyor
            if rb:
                if depth > 0:
                    in_item += 1
                    tag = "ITEMIZE İÇİ"
                else:
                    ciplak += 1
                    tag = "ÇIPLAK    "
                print(f"   {f.name}:{i+1} [{tag}] {raw_lines[i].strip()[:72]}")
            for _ in LIST_END.finditer(ml):
                depth = max(0, depth - 1)

        n_bold = len(BOLD.findall(masked))
        if ciplak or in_item or n_bold:
            print(f"== {f.name}: çıplak={ciplak}, itemize-içi={in_item}, kalın(**)={n_bold}")
            grand["dosya"] += 1
        grand["ciplak"] += ciplak
        grand["itemize"] += in_item
        grand["kalin"] += n_bold

    print(f"\nTOPLAM: çıplak={grand['ciplak']}, itemize-içi={grand['itemize']}, "
          f"kalın={grand['kalin']}, dosya={grand['dosya']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())