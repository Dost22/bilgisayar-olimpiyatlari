#!/usr/bin/env python3
"""check_secrets.py — Depoya sır (API anahtarı, token) sızmasını engelleyen kapı.

Neden var: bu depo **herkese açıktır**. Bir üretim betiğinde anahtarın koda
gömülmesi bir kez gerçekten oldu: `scripts/convert_python.py` içinde canlı bir
Google API anahtarı duruyordu ve GitHub'ın **push protection**'ı ilk gönderimi
(`GH013: Repository rule violations found ... GCP API Key Bound to a Service
Account`) reddetti (bkz. `KARARLAR.md` → D72). Kapı, aynı hatanın ikinci kez
olmasını makineyle engeller: hem yaygın sağlayıcı imzalarını hem de `.env`
dosyasındaki gerçek anahtarın koda kopyalanmasını arar.

Denetimler:

1. Bilinen sağlayıcı imzaları (Google `AIza…`/`AQ.…`, OpenAI `sk-…`, Anthropic
   `sk-ant-…`, GitHub `ghp_…`/`github_pat_…`, AWS `AKIA…`, Slack, Stripe, özel
   anahtar blokları, webhook'lar …)
2. `.env` içindeki her değerin (≥16 karakter) depodaki dosyalarda **birebir**
   geçip geçmediği (asıl koruma: gerçek anahtar koda yapıştırılırsa yakalanır)
3. Jenerik riskli atama kalıbı: `ANAHTAR_ADI = "uzun-deger"`

İzin listesi (bilerek): `config/KARARLAR.md` — karar günlüğü olayı sır **adıyla**
anlatır (ör. "GCP API Key Bound to a Service Account"); bu bir sızma değildir.

Kullanım:
    python3 scripts/check_secrets.py
    python3 scripts/check_secrets.py --brief
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Sır taramasından muaf tutulan dosyalar (gerekçe: olay anlatımı).
ALLOWLIST = {"config/KARARLAR.md"}
# Taranmayan dizinler: üretilen site, derleme çıktısı, ikili/yedek içerik.
SKIP_DIRS = {".git", "site", "_eski_output", "__pycache__"}
SKIP_SUFFIXES = {".pdf", ".png", ".jpg", ".otf", ".ttf", ".zip", ".gz"}

# (ad, kalıp) — gerçek sağlayıcı imzaları
SIGNATURES = [
    ("Google API anahtarı", r"AIza[0-9A-Za-z_\-]{35}"),
    ("Google OAuth/erişim jetonu", r"\bAQ\.[A-Za-z0-9_\-]{20,}"),
    ("OpenAI anahtarı", r"\bsk-[A-Za-z0-9]{32,}"),
    ("Anthropic anahtarı", r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
    ("GitHub anahtarı", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b"),
    ("GitHub ince taneli jeton", r"\bgithub_pat_[A-Za-z0-9_]{22,}"),
    ("AWS erişim anahtarı", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Slack jetonu", r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    ("Stripe canlı anahtarı", r"\bsk_live_[A-Za-z0-9]{20,}"),
    ("Özel anahtar bloğu", r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    ("Slack/Discord webhook",
     r"(?:hooks\.slack\.com/services|discord(?:app)?\.com/api/webhooks)/\S{20,}"),
    ("Telegram bot jetonu", r"\b\d{8,10}:AA[A-Za-z0-9_\-]{30,}"),
]

# Jenerik atama kalıbı: ANAHTAR = "en az 25 karakterlik dize"
GENERIC_ASSIGN = re.compile(
    r"\b([A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD))\s*=\s*[\"']([^\"'\s]{25,})[\"']"
)

# Değeri bu uzunluğun altındaki .env satırları yok sayılır (yanlış pozitifi azaltır).
ENV_MIN_LEN = 16


def repo_files() -> list[Path]:
    """**Yayımlanacak** (git'te izlenen) dosyalar; git yoksa dizin taraması.

    Ölçüt bilinçli olarak "izlenen dosyalar"dır: kapının işi, depoya gidecek
    içerikte sır olmadığını garanti etmektir. (`.gitignore` ile dışlanmış yerel
    dosyalar yayımlanmaz; yine de onlara anahtar koymamanız önerilir.)
    """
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True
        )
        if out.returncode == 0 and out.stdout.strip():
            return [
                ROOT / rel
                for rel in out.stdout.splitlines()
                if rel.strip() and (ROOT / rel).is_file()
            ]
    except OSError:
        pass

    out_paths: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if p.suffix in SKIP_SUFFIXES or rel.as_posix() in ALLOWLIST:
            continue
        out_paths.append(p)
    return sorted(out_paths)


def env_values() -> list[tuple[str, str]]:
    """.env içindeki (ad, değer) çiftleri — değeri ≥16 karakter olanlar."""
    env_file = ROOT / ".env"
    if not env_file.is_file():
        return []
    vals: list[tuple[str, str]] = []
    for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if len(value) >= ENV_MIN_LEN:
            vals.append((name.strip(), value))
    return vals


def main() -> int:
    ap = argparse.ArgumentParser(description="Depoda sır taraması yapar.")
    ap.add_argument("--brief", action="store_true")
    args = ap.parse_args()

    files = repo_files()
    envs = env_values()
    findings: list[str] = []

    print("=== check_secrets.py — sır taraması ===")
    print(f"Taranan dosya: {len(files)} · .env anahtarı: {len(envs)}")

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")

        for name, pattern in SIGNATURES:
            for m in re.finditer(pattern, text):
                line_no = text[: m.start()].count("\n") + 1
                findings.append(f"{rel}:{line_no}: {name} imzası bulundu")

        for m in GENERIC_ASSIGN.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            findings.append(
                f'{rel}:{line_no}: gömülü sır olabilecek atama: {m.group(1)} = "..."'
            )

        for name, value in envs:
            if value in text:
                line_no = text[: text.find(value)].count("\n") + 1
                findings.append(
                    f"{rel}:{line_no}: .env içindeki {name} değeri koda kopyalanmış"
                )

    if findings:
        print(f"\n[KRİTİK] {len(findings)} bulgu — depo HERKESE AÇIK, bu değerler paylaşılmamalı:")
        for f in findings:
            print("  -", f)
        print(
            "\nDüzeltme: değeri `.env` dosyasına taşıyın ve kodda ortam değişkeninden okuyun "
            "(desen: `load_env_key()`). Anahtar bir kez paylaşıldıysa **iptal edip yenileyin**; "
            "GitHub'ın 'allow secret' bağlantısını KULLANMAYIN (sırrın depoya girmesine izin "
            "verir; bkz. KARARLAR.md → D72)."
        )
    else:
        print(
            f"[OK] sır bulunamadı (taranan {len(files)} dosya"
            f"{', .env değerleriyle karşılaştırıldı' if envs else ''}) → kapı açık"
        )

    if args.brief:
        print(f"ÖZET: kritik={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())