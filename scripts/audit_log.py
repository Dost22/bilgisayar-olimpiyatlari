#!/usr/bin/env python3
"""audit_log.py — Derleme kaydını (`book_build.log`) denetleyen kapı.

Neden var: `compile_book.py` yalnızca derleyicinin dönüş koduna bakar. LaTeX ise
hataların çoğunu yutup yine de PDF üretir: eksik karakter, tanımsız referans,
bulunamayan dosya, taşan satır... Bunlar "derleme başarılı" görünürken kitaba
sessizce sızabilir. Bu araç kaydı okuyup bu izleri **sayar** ve nesnel bir kapı
kurar; hem CI'da hem yerelde aynı hükmü verir.

Kapılar:

- **KRİTİK (exit 1):** TeX hatası (`! `), `LaTeX Error`, eksik karakter, tanımsız
  kontrol dizisi, kaçak argüman, derlemenin yarıda kesilmesi, bulunamayan dosya,
  tanımsız referans/atıf ve **satır taşması** (`Overfull \\hbox`/`\\vbox` —
  bu kitabın sözleşmesi taşmanın 0 olmasıdır; bkz. `KARARLAR.md` → D5).
- **BİLGİ (exit 0):** `Underfull \\hbox`/`\\vbox`. Yazı tipi metriklerinin doğal
  sonucudur, görünür bir kusur üretmez (mevcut taban çizgisi: 67).

Not: `book_build.log` satır numaraları **birleştirilmiş** `book_build.tex`'e
göredir; taşmayı bölüm dosyasında bulmak için kayıttaki bağlamı okuyun.

Kullanım:
    python3 scripts/audit_log.py
    python3 scripts/audit_log.py --brief        # yalnız özet + kritik bulgular
    python3 scripts/audit_log.py --log baska.log
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "book_build.log"
BASELINE_UNDERFULL = 67  # mevcut taban çizgisi (yalnız bilgi amaçlı gösterilir)

# (ad, kalıp, kritik mi, ne demek?)
RULES = [
    ("TeX hatası", r"^! ", True,
     "Derleyici bir satırı işleyemedi."),
    ("LaTeX Error", r"LaTeX Error", True,
     "Paket/ortam kullanımından doğan hata."),
    ("Eksik karakter", r"Missing character", True,
     "Fontta olmayan bir karakter basıldı; PDF'te kaybolur."),
    ("Tanımsız kontrol dizisi", r"Undefined control sequence", True,
     "Yazımı hatalı bir makro ya da kaçırılmamış özel karakter."),
    ("Tanımsız referans", r"(?:Reference|Citation) [`'][^`']*['`][^\n]*undefined", True,
     "Bir \\ref/\\cite hedefi bulunamadı."),
    ("Kaçak argüman", r"Runaway argument", True,
     "Kapanmayan parantez ya da ortam var."),
    ("Acil durma", r"(?:Emergency stop|Fatal error occurred)", True,
     "Derleme yarıda kesildi."),
    ("Bulunamayan dosya", r"File [`'][^`']*['`] not found", True,
     "\\input/\\includegraphics ya da font yolu yanlış."),
    ("Satır taşması", r"Overfull \\[hv]box", True,
     "Taşan satır; kitabın sözleşmesi bu sayının 0 olmasıdır (D5)."),
    ("Satır seyrekliği", r"Underfull \\[hv]box", False,
     "Bilgi: yazı tipi metriklerinin doğal sonucu, zararsız."),
]

SAMPLE = 3  # kritik bir kalıp için gösterilecek örnek satır sayısı


def main() -> int:
    ap = argparse.ArgumentParser(description="Derleme kaydını denetler.")
    ap.add_argument("--log", default=str(DEFAULT_LOG), help="Denetlenecek kayıt dosyası.")
    ap.add_argument("--brief", action="store_true", help="Yalnız özet ve kritik bulgular.")
    args = ap.parse_args()

    log = Path(args.log)
    if not log.is_file():
        print(f"[HATA] {log} yok; önce derleyin: "
              "python3 scripts/compile_book.py --compiler tectonic", file=sys.stderr)
        return 2

    text = log.read_text(encoding="utf-8", errors="replace")
    print(f"=== audit_log.py — derleme kaydı denetimi ===\nKayıt: {log.name} "
          f"({len(text):,} karakter)")

    kritik = 0
    bilgi = 0
    sample_left = SAMPLE
    for name, pattern, is_critical, note in RULES:
        rx = re.compile(pattern, re.MULTILINE)
        hits = rx.findall(text)
        if not hits:
            if not args.brief:
                print(f"  [{'KRİTİK' if is_critical else 'BİLGİ ':>6}] {name:<24}: 0")
            continue
        if is_critical:
            kritik += len(hits)
        else:
            bilgi += len(hits)
        if is_critical or not args.brief:
            extra = "" if is_critical else f"  (taban çizgisi {BASELINE_UNDERFULL})"
            print(f"  [{'KRİTİK' if is_critical else 'BİLGİ ':>6}] {name:<24}: "
                  f"{len(hits)}{extra}\n          {note}")
            if is_critical:
                for line_no, raw in enumerate(text.splitlines(), 1):
                    if rx.search(raw):
                        print(f"          {log.name}:{line_no}: {raw.strip()[:110]}")
                        sample_left -= 1
                        if sample_left <= 0:
                            break

    durum = "kapı AÇIK (derleme temiz)" if kritik == 0 else "KAPI KAPALI (düzeltme gerekli)"
    print(f"\nÖZET: kritik={kritik}, bilgi={bilgi}  →  {durum}")
    return 1 if kritik else 0


if __name__ == "__main__":
    raise SystemExit(main())