#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path

import fitz

HEADER_FONT_SIZE = 15.2
RIGHT_LABEL_FONT_SIZE = 11.7
STORAGE_FONT_SIZE = 10.8
FILE_TYPE_FONT_SIZE = 18.4
METADATA_FONT_SIZE = 14.2

RIGHT_SIDE_LABEL_REPLACEMENTS = [
    ((1050, 4, 1130, 49), (1055, 3, 1125, 49), "DATA\nWRITTEN", HEADER_FONT_SIZE),
    ((1140, 4, 1186, 49), (1135, 3, 1191, 49), "FILE\nTYPE", HEADER_FONT_SIZE),
    ((1190, 4, 1292, 49), (1188, 3, 1294, 49), "END REASON\nMETADATA", HEADER_FONT_SIZE),
    ((1045, 64, 1130, 97), (1040, 64, 1135, 100), "All raw signals\nfrom experiment", RIGHT_LABEL_FONT_SIZE),
    ((1066, 104, 1115, 137), (1061, 103, 1120, 139), "Optional\nStorage", STORAGE_FONT_SIZE),
    ((1124, 116, 1212, 151), (1120, 114, 1216, 152), "bulk-fast5", FILE_TYPE_FONT_SIZE),
    ((1226, 81, 1255, 105), (1222, 80, 1259, 106), "YES", METADATA_FONT_SIZE),
    ((1052, 200, 1132, 232), (1048, 199, 1136, 235), "Single Molecule\nRaw Signals", RIGHT_LABEL_FONT_SIZE),
    ((1065, 241, 1120, 273), (1060, 240, 1122, 275), "Automatic\nStorage", STORAGE_FONT_SIZE),
    ((1121, 253, 1218, 311), (1118, 251, 1221, 313), "pod5,\nmulti-fast5", FILE_TYPE_FONT_SIZE),
    ((1226, 224, 1255, 249), (1222, 223, 1259, 250), "YES", METADATA_FONT_SIZE),
    ((1042, 315, 1144, 348), (1038, 314, 1148, 350), "Single Molecule\nSequences (”reads”)", RIGHT_LABEL_FONT_SIZE),
    ((1065, 352, 1120, 383), (1060, 351, 1123, 385), "Automatic\nStorage", STORAGE_FONT_SIZE),
    ((1122, 366, 1216, 402), (1118, 364, 1210, 404), "fastq,bam", FILE_TYPE_FONT_SIZE),
    ((1200, 323, 1283, 383), (1210, 322, 1294, 385), "NO\n(For Dorado\n< v1.3.1)", METADATA_FONT_SIZE),
    ((1043, 414, 1150, 461), (1038, 413, 1154, 463), "Aligned Single Molecule\nSequences\n(”mapped reads”)", RIGHT_LABEL_FONT_SIZE),
    ((1065, 463, 1120, 495), (1060, 462, 1123, 495), "Automatic\nStorage", STORAGE_FONT_SIZE),
    ((1148, 470, 1192, 495), (1144, 468, 1196, 495), "bam", FILE_TYPE_FONT_SIZE),
    ((1200, 436, 1286, 495), (1197, 435, 1288, 495), "NO\n(For Dorado\n< v1.3.1)", METADATA_FONT_SIZE),
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def enlarge_right_side_labels(pdf_path: Path) -> None:
    doc = fitz.open(pdf_path)
    page = doc[0]
    for clear_rect, _, _, _ in RIGHT_SIDE_LABEL_REPLACEMENTS:
        page.add_redact_annot(fitz.Rect(*clear_rect), fill=(1, 1, 1))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    for _, text_rect, label, size in RIGHT_SIDE_LABEL_REPLACEMENTS:
        page.insert_textbox(
            fitz.Rect(*text_rect),
            label,
            fontsize=size,
            fontname="helv",
            align=fitz.TEXT_ALIGN_CENTER,
            color=(0, 0, 0),
        )
    tmp = pdf_path.with_suffix(".labels.pdf")
    doc.save(tmp)
    doc.close()
    tmp.replace(pdf_path)


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
    enlarge_right_side_labels(pdf_out)
    subprocess.run([
        "pdftocairo", "-png", "-singlefile", "-r", "300", str(pdf_out), str(png_out.with_suffix(""))
    ], check=True)
    subprocess.run([
        "pdftocairo", "-svg", str(pdf_out), str(svg_out)
    ], check=True)

    print("Packaged Figure 1")
    print(f"PDF sha256: {sha256(pdf_out)}")
    print(f"PNG sha256: {sha256(png_out)}")
    print(f"SVG sha256: {sha256(svg_out)}")


if __name__ == "__main__":
    main()
