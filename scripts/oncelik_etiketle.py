#!/usr/bin/env python3
"""oncelik_etiketle.py — Bölümlere "1. Aşama önceliği" etiketlerini işler.

TEK KAYNAK: config/mufredat.md içindeki bölüm başlıklarında `· öncelik: X`
alanı (X ∈ Temel|Orta|İleri). Bu betik iki şeyi üretir:

  1. `--mufredat`: mufredat.md başlıklarına eksikse `· öncelik: X` alanını
     ekler (eşleme, bu dosyanın altındaki ONCELIK sözlüğünden okunur;
     değişiklik önce sözlükte, sonra bu bayrakla yapılır).
  2. (varsayılan): output/NN_*.tex dosyalarındaki bölüm başlığını FİHRİST
     biçimine çevirir/günceller (idempotent):

         \chapter[Başlık · \textit{X}]{Başlık}
         \chaptermark{Başlık}          % üstbilgi, etiketsiz temiz başlığı taşır

     Yani öncelik etiketi İçindekiler'de başlığın yanında görünür; bölüm
     başlığının altına ayrıca satır BASILMAZ (bkz. KARARLAR.md → D44).

Kullanım:
    python3 scripts/oncelik_etiketle.py --mufredat
    python3 scripts/oncelik_etiketle.py            # .tex'leri etiketle
    python3 scripts/oncelik_etiketle.py --dry-run
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUFREDAT = os.path.join(ROOT, "config", "mufredat.md")
OUTPUT = os.path.join(ROOT, "output")

# Bölüm numarası → öncelik düzeyi. Yalnızca Bölüm 1–32 işaretlenir;
# 33–38 alıştırma/başvuru bölümleri olduğu için işaretsizdir (kullanıcı kararı).
ONCELIK = {
    1: "Temel", 2: "Temel", 3: "Temel", 4: "Temel", 5: "Temel", 6: "Orta",
    7: "Temel", 8: "Orta", 9: "İleri", 10: "İleri", 11: "Temel", 12: "Temel",
    13: "Temel", 14: "Temel", 15: "İleri", 16: "Orta", 17: "Temel", 18: "İleri",
    19: "Orta", 20: "Temel", 21: "Temel", 22: "Temel", 23: "Temel", 24: "Temel",
    25: "Temel", 26: "Orta", 27: "Orta", 28: "Orta", 29: "Temel", 30: "Temel",
    31: "Temel", 32: "Orta",
}


def update_mufredat(dry: bool) -> list[str]:
    """mufredat.md bölüm başlıklarına öncelik alanını ekler/günceller."""
    notes = []
    lines = open(MUFREDAT, encoding="utf-8").read().split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^(### Bölüm )(\d+)( — .*\()(.*?)(\))$", line)
        if not m:
            continue
        num = int(m.group(2))
        if num not in ONCELIK:
            continue
        level = ONCELIK[num]
        inner = m.group(4)
        new_inner = re.sub(r" · öncelik: (Temel|Orta|İleri)", "", inner)
        new_inner += " · öncelik: {}".format(level)
        new_line = m.group(1) + m.group(2) + m.group(3) + new_inner + m.group(5)
        if new_line != line:
            notes.append("  mufredat: Bölüm {} → {}".format(num, level))
            if not dry:
                lines[i] = new_line
    if not dry:
        open(MUFREDAT, "w", encoding="utf-8").write("\n".join(lines))
    return notes


def tex_file(num: int) -> str | None:
    hits = sorted(glob.glob(os.path.join(OUTPUT, "{:02d}_*.tex".format(num))))
    return hits[0] if hits else None


def _convert(text: str, level: str) -> str | None:
    """Bölüm başlığını fihrist biçimine çevirir; dönüşemezse None döner."""
    # 0) Onarım: betiğin eski sürümü ham string yüzünden dosyalara
    #    "\\chapter[...]{...}\\n\\chaptermark{...}" biçiminde bozuk metin
    #    yazmış olabilir; bu durumu tanıyıp doğru biçime çevir.
    m = re.search(r"(?:\\\\)chapter\[([^\]]*?)\]\{([^\n]*?)\}(?:\\n)"
                  r"(?:\\\\)chaptermark\{([^\n]*?)\}", text)
    if m:
        title = m.group(2)
        repl = ("\\chapter[{t} · \\textit{{{l}}}]{{{t}}}\n"
                "\\chaptermark{{{t}}}".format(t=title, l=level))
        return text[:m.start()] + repl + text[m.end():]
    # 1) Eski biçim: \chapter{T}\n\oncelik{X} → fihrist biçimine çevir.
    m = re.search(r"(\\chapter\{([^\n]*?)\})\n\s*\\oncelik\{[^}]*\}", text)
    if m:
        title = m.group(2)
        repl = ("\\chapter[{t} · \\textit{{{l}}}]{{{t}}}\n"
                "\\chaptermark{{{t}}}".format(t=title, l=level))
        return text[:m.start()] + repl + text[m.end():]
    # 2) Mevcut fihrist biçimi: yalnızca etiketi güncelle.
    m = re.search(r"(\\chapter\[[^\]]*? · )\\textit\{(?:Temel|Orta|İleri)\}(\]\{[^\n]*?\})", text)
    if m:
        repl = m.group(1) + "\\textit{{{}}}".format(level) + m.group(2)
        return text[:m.start()] + repl + text[m.end():]
    # 3) Etiket yok: ilk \chapter{T} satırını fihrist biçimine çevir.
    m = re.search(r"(\\chapter\{([^\n]*?)\})\n", text)
    if m:
        title = m.group(2)
        repl = ("\\chapter[{t} · \\textit{{{l}}}]{{{t}}}\n"
                "\\chaptermark{{{t}}}\n".format(t=title, l=level))
        return text[:m.start()] + repl + text[m.end():]
    return None


def update_tex(dry: bool) -> list[str]:
    """output/*.tex dosyalarına fihrist etiketini ekler/günceller.

    Biçim: \chapter[Başlık · \textit{X}]{Başlık} + hemen altına
    \chaptermark{Başlık} (üstbilgi, etiketsiz temiz başlığı taşır).
    """
    notes = []
    for num, level in sorted(ONCELIK.items()):
        path = tex_file(num)
        if path is None:
            notes.append("  [UYARI] Bölüm {} için dosya bulunamadı".format(num))
            continue
        text = open(path, encoding="utf-8").read()
        new_text = _convert(text, level)
        if new_text is None:
            notes.append("  [UYARI] {} içinde \\chapter bulunamadı".format(os.path.basename(path)))
            continue
        if new_text != text:
            notes.append("  {} → fihrist etiketi: {}".format(os.path.basename(path), level))
            if not dry:
                open(path, "w", encoding="utf-8").write(new_text)
        else:
            notes.append("  {} → zaten güncel: {}".format(os.path.basename(path), level))
    return notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mufredat", action="store_true", help="öncelik alanını mufredat.md'ye işle")
    ap.add_argument("--dry-run", action="store_true", help="değişiklik yapmadan yalnızca göster")
    a = ap.parse_args()

    if a.mufredat:
        notes = update_mufredat(a.dry_run)
    else:
        notes = update_tex(a.dry_run)
    print("\n".join(notes) if notes else "  (değişiklik yok)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
