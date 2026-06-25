#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser(description="Package Figure 1 workflow assets")
    p.add_argument("--source-pdf", required=True)
    p.add_argument("--source-png", required=True)
    p.add_argument("--out-dir", default="3_results/figures")
    args = p.parse_args()

    source_pdf = Path(args.source_pdf).resolve()
    source_png = Path(args.source_png).resolve()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not source_pdf.exists() or not source_png.exists():
        raise SystemExit("Source PDF/PNG must exist.")

    pdf_out = out_dir / "Figure_1_final.pdf"
    png_out = out_dir / "Figure_1_final.png"
    svg_out = out_dir / "Figure_1_final.svg"

    shutil.copy2(source_pdf, pdf_out)
    shutil.copy2(source_png, png_out)
    subprocess.run([
        "pdftocairo", "-svg", str(pdf_out), str(svg_out)
    ], check=True)

    print("Packaged Figure 1")
    print(f"PDF sha256: {sha256(pdf_out)}")
    print(f"PNG sha256: {sha256(png_out)}")
    print(f"SVG sha256: {sha256(svg_out)}")


if __name__ == "__main__":
    main()
