"""
common.py
Bagian bersama: definisi instruksi, scheduler ILP, dan penggambar dependency graph.
"""

from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list

    def __str__(self):
        return f"{self.destination} = {' + '.join(self.sources)}"


EDGE_STYLE = {
    "RAW": {"color": "#d62728", "style": "-"},
    "WAR": {"color": "#1f77b4", "style": "--"},
    "WAW": {"color": "#2ca02c", "style": ":"},
}


# -------------------------------------------------
# Scheduler ILP
# -------------------------------------------------
def schedule(instructions, edges):
    """
    Penjadwalan ASAP. edges = list (src_idx, dst_idx, register, tipe).
    Sebuah instruksi baru boleh jalan setelah semua predecessor-nya
    selesai (cycle sebelumnya). Return: list level (cycle) tiap instruksi.
    """
    level = [0] * len(instructions)
    for j in range(len(instructions)):
        preds = [e[0] for e in edges if e[1] == j]
        level[j] = 1 + max((level[i] for i in preds), default=0)
    return level


def print_schedule(instructions, level, title):
    print("\n" + "=" * 56)
    print(title)
    print("=" * 56)
    for c in range(1, max(level) + 1):
        group = [ins for ins, lv in zip(instructions, level) if lv == c]
        print(f"Cycle {c}:")
        for ins in group:
            print(f"  -> {ins.name}: {ins}")
    print(f"Total cycles: {max(level)}")
    return max(level)


def print_dependencies(instructions, edges, label):
    print("\n" + "=" * 56)
    print(f"DEPENDENCY ANALYSIS - {label}")
    print("=" * 56)
    if not edges:
        print("Tidak ada dependency.")
    for src, dst, reg, kind in edges:
        print(f"{kind}: {instructions[dst].name} bergantung pada "
              f"{instructions[src].name} (register {reg})")


# -------------------------------------------------
# Dependency graph
# -------------------------------------------------
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

NODE_INDEP = "#c8f0c8"   # hijau  : instruksi independen (tanpa dependensi)
NODE_DEP = "#ffe9a8"     # kuning : instruksi dependen


def draw_graph(instructions, edges, title, filename):
    """
    Tata letak: baris = instruksi, kolom = cycle.
    Teks instruksi ada di kolom kiri, kotak hanya berisi nama (I1, I2, ...),
    panah berhenti tepat di tepi kotak sehingga kepala panah terlihat jelas.
    """
    level = schedule(instructions, edges)
    n, cols = len(instructions), max(level)

    LABEL_W, COLW, ROWH = 3.2, 1.55, 0.85
    BW, BH = 0.70, 0.50
    TOP, BOTTOM = 1.25, 0.95
    W = LABEL_W + COLW * cols + 0.3
    H = TOP + ROWH * n + BOTTOM

    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    def X(c):
        return LABEL_W + COLW * (c - 0.5)

    def Y(i):
        return H - TOP - ROWH * (i + 0.5)

    # ---- latar kolom cycle + judul kolom ----
    y_top, y_bot = H - TOP + 0.25, BOTTOM - 0.25
    for c in range(1, cols + 1):
        if c % 2 == 1:
            ax.add_patch(Rectangle((LABEL_W + COLW * (c - 1), y_bot), COLW,
                                   y_top - y_bot, fc="#f1f3f6", ec="none", zorder=0))
        ax.text(X(c), H - TOP + 0.45, f"Cycle {c}", ha="center", va="center",
                fontsize=12, fontweight="bold", color="#333")

    # ---- baris: garis tipis + teks instruksi ----
    for i, ins in enumerate(instructions):
        ax.plot([0.1, W - 0.1], [Y(i) - ROWH / 2] * 2, color="#e3e3e3", lw=0.8, zorder=0)
        ax.text(0.2, Y(i), f"{ins.name}:  {ins}", ha="left", va="center",
                fontsize=12, fontweight="bold", family="monospace", color="#111")

    # ---- node ----
    has_pred = {e[1] for e in edges}
    box = {}
    for i, ins in enumerate(instructions):
        x, y = X(level[i]), Y(i)
        p = FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH,
                           boxstyle="round,pad=0.02,rounding_size=0.12",
                           fc=NODE_DEP if i in has_pred else NODE_INDEP,
                           ec="#222", lw=1.8, zorder=5)
        ax.add_patch(p)
        ax.text(x, y, ins.name, ha="center", va="center", fontsize=13,
                fontweight="bold", zorder=6)
        box[i] = p

    # ---- panah dependensi (lengkungan dipilih otomatis agar tidak menabrak kotak) ----
    def curve_pts(p0, p2, rad, m=40):
        (x1, y1), (x2, y2) = p0, p2
        cx = (x1 + x2) / 2 + rad * (y2 - y1)
        cy = (y1 + y2) / 2 - rad * (x2 - x1)
        pts = []
        for j in range(m + 1):
            t = j / m
            pts.append(((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2,
                        (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2))
        return pts

    def hits(pts, skip, margin=0.10):
        n_hit = 0
        for j, (px, py) in enumerate(pts):
            if j < 6 or j > len(pts) - 7:
                continue
            for i2 in range(n):
                if i2 in skip:
                    continue
                bx, by = X(level[i2]), Y(i2)
                if abs(px - bx) < BW / 2 + margin and abs(py - by) < BH / 2 + margin:
                    n_hit += 1
                    break
        return n_hit

    taken_labels = []
    drawn_pts = []
    seen = {}
    # garis pendek diproses lebih dulu, garis panjang mencari jalur yang tidak menabrak
    order = sorted(edges, key=lambda e: (level[e[1]] - level[e[0]], e[1] - e[0]))
    for src, dst, reg, kind in order:
        k = seen.get((src, dst), 0)
        seen[(src, dst)] = k + 1
        p0, p2 = (X(level[src]), Y(src)), (X(level[dst]), Y(dst))
        pref = 1 if kind == "RAW" else -1
        cands = [0.0]
        for r in (0.18, 0.32, 0.46, 0.62, 0.80):
            cands += [pref * r, -pref * r]
        best = None
        for rad in cands:
            pts = curve_pts(p0, p2, rad)
            mid = pts[len(pts) // 2]
            lab = sum(1 for (lx, ly) in taken_labels
                      if abs(lx - mid[0]) < 0.45 and abs(ly - mid[1]) < 0.28)
            lab += sum(1 for i2 in range(n) if i2 not in (src, dst)
                       and abs(mid[0] - X(level[i2])) < BW / 2 + 0.25
                       and abs(mid[1] - Y(i2)) < BH / 2 + 0.2)
            mid_pts = pts[8:-8]
            close = sum(1 for (px, py) in mid_pts
                        if any(abs(px - qx) < 0.16 and abs(py - qy) < 0.16
                               for (qx, qy) in drawn_pts))
            score = hits(pts, {src, dst}) * 100 + lab * 30 + close * 6 + abs(rad) * 5 \
                + (0 if rad * pref >= 0 else 2) + (40 * k if abs(rad) < 0.1 * (k + 1) else 0)
            if best is None or score < best[0]:
                best = (score, rad, mid)
        _, rad, mid = best
        taken_labels.append(mid)
        drawn_pts.extend(curve_pts(p0, p2, rad)[8:-8])
        st = EDGE_STYLE[kind]
        ax.add_patch(FancyArrowPatch(
            p0, p2, patchA=box[src], patchB=box[dst],
            arrowstyle="-|>", mutation_scale=22, color=st["color"],
            linestyle=st["style"], linewidth=2.2,
            connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1, zorder=3))
        ax.text(mid[0], mid[1], reg, ha="center", va="center", fontsize=11,
                fontweight="bold", color=st["color"], zorder=7,
                bbox=dict(fc="white", ec=st["color"], lw=0.8, pad=1.5,
                          boxstyle="round,pad=0.15"))

    # ---- judul + legenda ----
    ax.text(W / 2, H - 0.35, f"{title}  ({cols} cycle)", ha="center", va="center",
            fontsize=15, fontweight="bold")
    handles = [Line2D([0], [0], color=EDGE_STYLE[k]["color"],
                      linestyle=EDGE_STYLE[k]["style"], lw=2.5, label=k)
               for k in sorted({e[3] for e in edges})]
    handles += [Rectangle((0, 0), 1, 1, fc=NODE_INDEP, ec="#222", label="Independen"),
                Rectangle((0, 0), 1, 1, fc=NODE_DEP, ec="#222", label="Dependen")]
    ax.legend(handles=handles, loc="lower center", ncol=len(handles), fontsize=11,
              frameon=False, bbox_to_anchor=(0.5, 0.0))

    fig.savefig(filename, dpi=150, bbox_inches="tight", pad_inches=0.25,
                facecolor="white")
    plt.close(fig)
    return level
