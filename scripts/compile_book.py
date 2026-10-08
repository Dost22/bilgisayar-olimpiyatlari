#!/usr/bin/env python3
"""compile_book.py

/output klasöründeki tüm .tex dosyalarını sıralayıp
/templates/main.tex şablonuna yerleştirerek kitabı derler.

Yaptıkları:
1. /output içindeki .tex dosyalarını doğal (nümerik) olarak sıralar.
2. /templates/main.tex'i okur; \\begin{document} içinde \\tableofcontents
   sonrasına her dosya için \\input{output/dosya_adi} satırı ekler.
3. Kök dizinde book_build.tex dosyasını oluşturur.
4. pdflatex'i book_build.tex için iki kez çalıştırır (TOC indeksleri için).
5. Ortaya çıkan book_build.pdf kök dizinde kalır.

Kullanım:
    python3 scripts/compile_book.py
    python3 scripts/compile_book.py --no-compile         # sadece .tex üret
    python3 scripts/compile_book.py --compiler latexmk   # farklı derleyici
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "templates" / "main.tex"
OUTPUT_DIR = ROOT / "output"
BUILD_TEX = ROOT / "book_build.tex"


def natural_sort_key(path: Path):
    """Dosya adını, içindeki sayıları nümerik sıralayacak bir anahtara çevirir."""
    name = path.name
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def collect_output_files() -> list[Path]:
    """/output içindeki .tex dosyalarını doğal sırada döndürür."""
    if not OUTPUT_DIR.is_dir():
        return []
    files = [p for p in OUTPUT_DIR.glob("*.tex") if p.is_file()]
    return sorted(files, key=natural_sort_key)


# TEK KAYNAK: config/mufredat.md — aynı çözümleme scripts/build_site.py →
# read_part_map() içinde de vardır; ikisi birlikte güncellenmelidir (D67).
KISIM_HEADER_RE = re.compile(r"^##\s+KISIM\s+([IVX]+)\s+—\s+(.+?)\s*(?:\(.*)?$")
BOLUM_HEADER_RE = re.compile(r"^###\s+Bölüm\s+(\d+)\s+—")


def read_part_map() -> dict[int, str]:
    """config/mufredat.md'den bölüm numarası → 'KISIM X — Ad' eşlemesini çıkarır."""
    mufredat_path = ROOT / "config" / "mufredat.md"
    part_of: dict[int, str] = {}
    current_part = ""
    for raw in mufredat_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = KISIM_HEADER_RE.match(line)
        if m:
            current_part = f"KISIM {m.group(1)} — {m.group(2).strip()}"
            continue
        m = BOLUM_HEADER_RE.match(line)
        if m and current_part:
            part_of[int(m.group(1))] = current_part
    return part_of


def insert_inputs(template_text: str, files: list[Path]) -> str:
    """Şablondaki \\tableofcontents satırının hemen sonrasına \\input satırları ekler.

    Her kısmın ilk bölümünden önce, fihristte kısım gruplarını gösteren
    ``\\kisimfihrist{KISIM X — Ad}`` satırı yerleştirilir (gövdeye bir şey
    basılmaz; bkz. KARARLAR.md → D67). Kısım adları tek kaynak olan
    config/mufredat.md'den okunur.
    """
    begin_doc_idx = template_text.find(r"\begin{document}")
    toc_idx = template_text.find(r"\tableofcontents")

    if begin_doc_idx == -1:
        raise ValueError("Şablonda \\begin{document} bulunamadı.")
    if toc_idx == -1:
        raise ValueError("Şablonda \\tableofcontents bulunamadı.")
    if toc_idx < begin_doc_idx:
        raise ValueError("\\tableofcontents, \\begin{document} öncesinde olamaz.")

    # \tableofcontents satırının bitiş yeri (satır sonu).
    line_end = template_text.find("\n", toc_idx)
    if line_end == -1:
        line_end = len(template_text)

    part_of = read_part_map()
    input_lines: list[str] = []
    last_part: str | None = None
    for f in files:
        m = re.match(r"^(\d+)_", f.name)
        chapter_no = int(m.group(1)) if m else 0
        part = part_of.get(chapter_no)
        if part and part != last_part:
            input_lines.append(f"\\kisimfihrist{{{part}}}")
            last_part = part
        input_lines.append(f"\\input{{{OUTPUT_DIR.name}/{f.name}}}")

    insert_point = line_end + 1
    block = ""
    if input_lines:
        block = (
            "\n% --- Bölüm dosyaları (compile_book.py tarafından üretildi) ---\n"
            + "\n".join(input_lines)
            + "\n"
        )
    return template_text[:insert_point] + block + template_text[insert_point:]


def build_tex(files: list[Path]) -> None:
    """Şablonu okuyup girdi satırlarıyla birleştirir ve book_build.tex yazar."""
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    result = insert_inputs(template_text, files)
    BUILD_TEX.write_text(result, encoding="utf-8")


def run_latex(compiler: str) -> list[int]:
    """book_build.tex'i derler; dönüş kodlarını liste olarak döndürür.

    pdflatex gibi derleyicilerde içindekiler indekslerinin oturması için iki
    geçiş yapılır. Tectonic ise gerekli tüm geçişleri tek çağrıda kendisi yapar.
    """
    if compiler == "tectonic":
        # --keep-logs: tectonic log dosyasını VARSAYILAN olarak saklamaz; derleme
        # kaydını denetleyebilmek (scripts/audit_log.py) için açıkça istenir.
        cmd = [compiler, "--keep-logs", BUILD_TEX.name]
        print(f"[Derleniyor] {' '.join(cmd)} (tectonic çoklu geçişi otomatik yapar)")
        result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[UYARI] hata kodu {result.returncode}", file=sys.stderr)
            tail = "\n".join(result.stdout.splitlines()[-30:])
            if tail:
                print(tail, file=sys.stderr)
        return [result.returncode]

    cmd = [compiler, "-interaction=nonstopmode", BUILD_TEX.name]
    codes: list[int] = []
    for pass_no in (1, 2):
        print(f"[Derleniyor] Geçiş {pass_no}/2: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        codes.append(result.returncode)
        if result.returncode != 0:
            print(
                f"[UYARI] Geçiş {pass_no} hata kodu {result.returncode} ile bitti.",
                file=sys.stderr,
            )
            tail = "\n".join(result.stdout.splitlines()[-30:])
            if tail:
                print(tail, file=sys.stderr)
    return codes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Kitabı derleyip PDF üretir.")
    parser.add_argument(
        "--compiler",
        default="pdflatex",
        help="LaTeX derleyicisi (varsayılan: pdflatex; en kolay alternatif: tectonic).",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Yalnızca book_build.tex üret, PDF derlemesi yapma.",
    )
    args = parser.parse_args(argv)

    files = collect_output_files()
    if not files:
        print("/output klasöründe .tex dosyası bulunamadı.")
        return 1

    print("/output içinde bulunan dosyalar (sıralı):")
    for f in files:
        print(f"  - {f.name}")

    build_tex(files)
    print(f"[OK] {BUILD_TEX.name} oluşturuldu ({len(files)} girdi).")

    if args.no_compile:
        print("Derleme atlandı (--no-compile).")
        return 0

    if shutil.which(args.compiler) is None:
        print(
            f"[HATA] '{args.compiler}' sistemde bulunamadı. "
            "Lütfen bir TeX dağıtımı kurun (örn. MacTeX: https://www.tug.org/mactex/).",
            file=sys.stderr,
        )
        return 2

    codes = run_latex(args.compiler)

    pdf = ROOT / "book_build.pdf"
    if pdf.is_file():
        print(f"[OK] {pdf.name} üretildi ({pdf.stat().st_size} bayt).")
        return 0 if all(code == 0 for code in codes) else 1

    print("[HATA] book_build.pdf üretilemedi.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
