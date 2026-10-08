#!/usr/bin/env python3
"""check_frontmatter.py — Önsöz/Hakkında'nın sayfa düzenini denetler.

Ne yapar: `book_build.pdf`'in ilk sayfalarını metne çevirip her sayfanın ilk
satırını yazdırır. Böylece bir bölümün bir sonraki sayfaya **taşıp taşmadığı**
(yetim satır / yalnız kalan satır) hemen görülür.

Kullanım:
    python3 scripts/check_frontmatter.py          # ilk 6 sayfa
    python3 scripts/check_frontmatter.py 2 8      # 2..8. sayfalar
    python3 scripts/check_frontmatter.py --lines  # her sayfanın satır sayısı da

Önkoşul: `book_build.pdf` derlenmiş olmalı (ghostscript `gs` gerekir).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "book_build.pdf"


def page_text(pdf: Path, page: int) -> str:
    """Tek sayfanın metnini döndürür (gs ile). Hata olursa uyarır, boş döner."""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "p.txt"
        try:
            r = subprocess.run(
                ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=txtwrite",
                 f"-dFirstPage={page}", f"-dLastPage={page}",
                 f"-sOutputFile={out}", str(pdf)],
                capture_output=True,
            )
        except OSError as e:  # gs çalıştırılamadı
            print(f"  s{page:>3}: [gs hatası: {e}]")
            return ""
        if r.returncode != 0 or not out.exists():
            err = (r.stderr or b"").decode("utf-8", "replace").strip()[:120]
            print(f"  s{page:>3}: [gs başarısız (kod {r.returncode})] {err}")
            return ""
        return out.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    if not shutil.which("gs"):
        print("[HATA] ghostscript (gs) bulunamadı.", file=sys.stderr)
        return 2
    if not PDF.is_file():
        print(f"[HATA] {PDF} yok; önce derleyin.", file=sys.stderr)
        return 2

    ap = argparse.ArgumentParser()
    ap.add_argument("first", nargs="?", type=int, default=2)
    ap.add_argument("last", nargs="?", type=int, default=6)
    ap.add_argument("--lines", action="store_true", help="satır sayısını da göster")
    a = ap.parse_args()

    print(f"=== {PDF.name}: sayfa {a.first}..{a.last} ===")
    for p in range(a.first, a.last + 1):
        txt = page_text(PDF, p)
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        # sayfa numarası satırını at
        body = [l for l in lines if not re.fullmatch(r"\d+", l)]
        head = body[0][:70] if body else "(boş)"
        tail = body[-1][:60] if body else ""
        n = len(body)
        flag = ""
        if n <= 3:
            flag = "  <-- ⚠ NEREDEYSE BOŞ (yetim satır olabilir)"
        extra = f" [{n} satır]" if a.lines else ""
        print(f"  s{p:>3}: {head}{extra}")
        if flag:
            print(f"        son satır: {tail!r}{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())