"""
generate_report.py - laporan PDF untuk 12 program (3 anggota x 4 program).
  python run_all.py
  python generate_report.py --members "Nama1 (NIM)" "Nama2 (NIM)" "Nama3 (NIM)" --github URL
"""
import argparse
import importlib.util
import os

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

import common
from hazards import find_raw, find_war, find_waw

ap = argparse.ArgumentParser()
ap.add_argument("--members", nargs="*", default=["[Nama Anggota 1 - NIM]",
                "[Nama Anggota 2 - NIM]", "[Nama Anggota 3 - NIM]"])
ap.add_argument("--github", default="[tempel link GitHub di sini]")
ap.add_argument("--out", default="Laporan_ILP_RAW_WAR_WAW.pdf")
args = ap.parse_args()

base = os.path.dirname(os.path.abspath(__file__))
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13, spaceBefore=6, spaceAfter=4)
H3 = ParagraphStyle("H3", parent=ss["Heading3"], fontSize=11, spaceBefore=6, spaceAfter=3)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10, leading=14)
CELL = ParagraphStyle("CELL", parent=B, fontSize=8.5, leading=11)
SM = ParagraphStyle("SM", parent=B, fontSize=8.5, leading=11, textColor=colors.HexColor("#444"))
W = A4[0] - 4 * cm


def img(path, width=W, max_h=8.5 * cm):
    w, h = PILImage.open(path).size
    height = width * h / w
    if height > max_h:
        width, height = width * max_h / height, max_h
    return Image(path, width=width, height=height)


def table(data, widths=None):
    data = [[Paragraph(c, CELL) if isinstance(c, str) and len(c) > 22 else c for c in r] for r in data]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#999")),
                           ("FONTSIZE", (0, 0), (-1, -1), 9), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]))
    return t


def load_ins(k):
    spec = importlib.util.spec_from_file_location(f"ins{k}", os.path.join(base, f"anggota{k}", "instruksi.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.INSTRUCTIONS


def dep_rows(ins, edges):
    rows = [["Tipe", "Dari", "Ke", "Reg", "Penjelasan"]]
    for s, d, reg, k in edges:
        a, b = ins[s], ins[d]
        t = {"RAW": f"{b.name} membaca {reg} yang ditulis {a.name}",
             "WAR": f"{b.name} menulis {reg} yang dibaca {a.name}",
             "WAW": f"{b.name} dan {a.name} sama-sama menulis {reg}"}[k]
        rows.append([k, a.name, b.name, reg, t])
    return rows


def sched_text(ins, level):
    return "; ".join(f"<b>C{c}</b>: " + ", ".join(i.name for i, lv in zip(ins, level) if lv == c)
                     for c in range(1, max(level) + 1))


story = [Paragraph("Laporan Tugas Kelompok: RAW, WAR, dan WAW pada Simulator ILP", H1),
         Paragraph("Mata kuliah: Paralelisme CPU - Instruction-level Parallelism (ILP)", B),
         Spacer(1, 6), Paragraph("<b>Anggota kelompok:</b>", B)]
for i, m in enumerate(args.members, 1):
    story.append(Paragraph(f"{i}. {m}", B))
story += [Spacer(1, 4),
          Paragraph(f"<b>Link GitHub:</b> <a href='{args.github}' color='blue'>{args.github}</a>", B),
          Spacer(1, 8), Paragraph("Ringkasan Program (3 anggota x 4 program = 12 program)", H2),
          table([["Anggota", "Program", "Fungsi"]] + [
              [f"Anggota {k}", f"anggota{k}/{p}.py", d] for k in (1, 2, 3) for p, d in
              [("raw", "Dependency graph + jadwal RAW"), ("war", "Dependency graph + jadwal WAR"),
               ("waw", "Dependency graph + jadwal WAW"), ("semua", "Gabungan RAW+WAR+WAW + perbandingan")]],
                [2.5 * cm, 4.5 * cm, 10 * cm]),
          Spacer(1, 6), Paragraph("Definisi", H2),
          table([["Hazard", "Nama lain", "Definisi", "Kondisi di kode"],
                 ["RAW", "True dependency", "Instruksi membaca register yang ditulis instruksi sebelumnya",
                  "earlier.destination in later.sources"],
                 ["WAR", "Anti-dependency", "Instruksi menulis register yang masih dibaca instruksi sebelumnya",
                  "later.destination in earlier.sources"],
                 ["WAW", "Output dependency", "Dua instruksi menulis register yang sama",
                  "earlier.destination == later.destination"]], [1.6 * cm, 3 * cm, 6.4 * cm, 6 * cm]),
          Spacer(1, 4),
          Paragraph("Catatan: edge dibuat ke penulis/pembaca terdekat saja (tanpa edge transitif). Satu cycle = "
                    "satu langkah; instruksi boleh jalan jika semua predecessor selesai di cycle sebelumnya. "
                    "Jadwal pada graph RAW/WAR/WAW dihitung terpisah (hanya hazard tersebut) untuk melihat "
                    "pengaruh masing-masing; jadwal yang benar secara keseluruhan ada pada graph gabungan.", SM),
          PageBreak()]

for k in (1, 2, 3):
    ins = load_ins(k)
    n = len(ins)
    raw, war, waw = find_raw(ins), find_war(ins), find_waw(ins)
    comb = raw + war + waw
    story += [Paragraph(f"Anggota {k}: {args.members[k - 1]}", H2),
              Paragraph("Instruction set:", B),
              table([["Instruksi", "Operasi"]] + [[i.name, str(i)] for i in ins], [3 * cm, 6 * cm]),
              Spacer(1, 6)]
    for name, title, edges in [("raw", "Program 1: RAW", raw), ("war", "Program 2: WAR", war),
                               ("waw", "Program 3: WAW", waw), ("semua", "Program 4: Gabungan RAW + WAR + WAW", comb)]:
        level = common.schedule(ins, edges)
        story.append(KeepTogether([
            Paragraph(f"{title} (anggota{k}/{name}.py) - {max(level)} cycle", H3),
            img(os.path.join(base, f"anggota{k}", "graphs", f"{name}.png")),
            Spacer(1, 3), table(dep_rows(ins, edges), [1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 11 * cm]),
            Spacer(1, 3), Paragraph("Jadwal: " + sched_text(ins, level), SM), Spacer(1, 8)]))
    rows = [["Skenario", "Cycle", "Speedup"]]
    for nm, e in [("Sequential", None), ("RAW saja (renaming ideal)", raw), ("RAW + WAR", raw + war),
                  ("RAW + WAW", raw + waw), ("RAW + WAR + WAW (tanpa renaming)", comb)]:
        c = n if e is None else max(common.schedule(ins, e))
        rows.append([nm, str(c), f"{n / c:.2f}x"])
    story += [Paragraph(f"Perbandingan performa - Anggota {k}", H3), table(rows, [9 * cm, 3 * cm, 3 * cm]),
              PageBreak()]

story += [Paragraph("Kesimpulan", H2),
          Paragraph("Hanya RAW yang merupakan dependency sejati. WAR dan WAW adalah name dependency akibat "
                    "pemakaian ulang nama register, sehingga dapat dihilangkan dengan register renaming. Pada "
                    "ketiga instruction set, menjalankan RAW saja (renaming ideal) memberi cycle paling sedikit, "
                    "sedangkan menambahkan WAR/WAW menambah cycle karena memaksa urutan eksekusi.", B)]

SimpleDocTemplate(args.out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                  bottomMargin=1.8 * cm, title="Laporan ILP RAW WAR WAW").build(story)
print("PDF dibuat:", args.out)
