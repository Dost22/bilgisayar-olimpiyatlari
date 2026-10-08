#!/usr/bin/env python3
"""check_number_suffixes.py — Sayıya bağlanan Türkçe ekleri (N'de / N'da ...) denetler.

Kural: Ekin biçimi, sayının TÜRKÇE OKUNUŞUNUN son sesine göre belirlenir
("on yedi'de", "otuz dört'te", "kırk beş'ten"). Bu araç, metindeki her
`N'<ek>` kalıbını bulup doğru eki bağımsız olarak hesaplar ve uyuşmayanları
raporlar (isteğe bağlı olarak düzeltir).

Kullanım:
    python3 scripts/check_number_suffixes.py            # rapor
    python3 scripts/check_number_suffixes.py --fix      # düzelt
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT / "output", ROOT / "frontmatter"]

VOWELS = "aeıioöuü"
BACK = "aıou"
UNVOICED = "çtkfhsş"
ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]

SUFFIXES = ["dan", "den", "tan", "ten", "daki", "deki", "taki", "teki",
            "da", "de", "ta", "te", "ya", "ye", "a", "e"]
PAT = re.compile(r"(\d+)'(" + "|".join(sorted(SUFFIXES, key=len, reverse=True)) + r")\b")


def reading(n: int) -> str:
    if n == 0:
        return "sıfır"
    if n < 10:
        return ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return TENS[t] + (" " + ONES[o] if o else "")
    if n < 1000:
        h, rest = divmod(n, 100)
        return ONES[h] + " yüz" + ((" " + reading(rest)) if rest else "")
    if n < 10000:
        th, rest = divmod(n, 1000)
        return ONES[th] + " bin" + ((" " + reading(rest)) if rest else "")
    return " ".join(ONES[int(d)] + (" bin" if i == 1 else "") for i, d in enumerate(str(n)) if d != "0")


def kind_of(s: str) -> str:
    if s.endswith("ki"):
        return "loc+ki"
    if s in ("da", "de", "ta", "te"):
        return "loc"
    if s in ("dan", "den", "tan", "ten"):
        return "abl"
    return "dat"


def correct(n: int, kind: str) -> str:
    w = reading(n)
    last = w[-1]
    unvoiced = last in UNVOICED
    lv = next((c for c in reversed(w) if c in VOWELS), "a")
    kalin = lv in BACK
    if kind == "loc":
        return ("ta" if kalin else "te") if unvoiced else ("da" if kalin else "de")
    if kind == "loc+ki":
        return correct(n, "loc") + "ki"
    if kind == "abl":
        return ("tan" if kalin else "ten") if unvoiced else ("dan" if kalin else "den")
    if unvoiced:
        return "a" if kalin else "e"
    if last in VOWELS:
        return "ya" if kalin else "ye"
    return "a" if kalin else "e"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()

    total = bad = 0
    for d in DIRS:
        for f in sorted(d.glob("*.tex")):
            t = f.read_text(encoding="utf-8")
            fixes = []
            n_bad = 0
            for m in PAT.finditer(t):
                total += 1
                n, got = int(m.group(1)), m.group(2)
                want = correct(n, kind_of(got))
                if want != got:
                    ln = t[: m.start()].count("\n") + 1
                    print(f"{f.name}:{ln}: {n}'{got} → {n}'{want}")
                    fixes.append((m.start(2), m.end(2), want))
                    n_bad += 1
            if n_bad:
                bad += n_bad
                if args.fix:
                    out, pos = [], 0
                    for s, e, w in fixes:
                        out.append(t[pos:s]); out.append(w); pos = e
                    out.append(t[pos:])
                    f.write_text("".join(out), encoding="utf-8")
    print(f"\nincelenen {total} kalıp, uyuşmazlık {bad}"
          + (" (düzeltildi)" if args.fix else " (rapor)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())