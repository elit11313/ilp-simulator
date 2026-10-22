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
def draw_graph(instructions, edges, title, filename):
    level = schedule(instructions, edges)
    cols = max(level)
    rows_in_col, pos = {}, {}
    for idx, lv in enumerate(level):
        r = rows_in_col.get(lv, 0)
        rows_in_col[lv] = r + 1
        pos[idx] = (lv, -r)
    max_rows = max(rows_in_col.values())

    COLW, ROWH = 2.7, 1.5          # inci per kolom / per baris
    fig_w, fig_h = COLW * cols + 0.6, ROWH * (max_rows + 1.3) + 0.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0.45, cols + 0.55)
    ax.set_ylim(-(max_rows - 1) - 1.0, 1.35)
    ax.axis("off")

    for c in range(1, cols + 1):
        ax.text(c, 1.15, f"Cycle {c}", ha="center", fontsize=10, color="#555",
                fontweight="bold")

    # ---- edges ----
    pair_k = {}
    for src, dst, reg, kind in edges:
        k = pair_k.get((src, dst), 0)
        pair_k[(src, dst)] = k + 1
    pair_seen = {}
    for src, dst, reg, kind in edges:
        x1, y1 = pos[src]
        x2, y2 = pos[dst]
        gap = max(abs(x2 - x1), 1)
        k = pair_seen.get((src, dst), 0)
        pair_seen[(src, dst)] = k + 1
        sign = 1 if kind == "RAW" else -1          # RAW di atas, WAR/WAW di bawah
        if gap == 1 and pair_k[(src, dst)] == 1:
            d = 0.0
        else:
            d = 0.45 + 0.22 * max(gap - 2, 0) + 0.3 * k
        length_in = max(((x2 - x1) * COLW) ** 2 + ((y2 - y1) * ROWH) ** 2, 1e-6) ** 0.5
        rad = -sign * 2 * d / length_in
        st = EDGE_STYLE[kind]
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
            color=st["color"], linestyle=st["style"], linewidth=1.8,
            connectionstyle=f"arc3,rad={rad}", shrinkA=34, shrinkB=34, zorder=1))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        off = sign * (d / ROWH if d else 0.09)
        ax.text(mx, my + off + (0.02 if sign > 0 else -0.02), reg, fontsize=8,
                color=st["color"], ha="center", va="bottom" if sign > 0 else "top",
                fontweight="bold", zorder=3,
                bbox=dict(fc="white", ec="none", pad=0.6))

    # ---- nodes (kotak berisi nama + instruksi) ----
    for idx, ins in enumerate(instructions):
        x, y = pos[idx]
        ax.text(x, y, f"{ins.name}\n{ins}", ha="center", va="center", fontsize=9,
                fontweight="bold", zorder=4,
                bbox=dict(boxstyle="round,pad=0.45", fc="#fff4d6", ec="#333", lw=1.4))

    kinds = sorted({e[3] for e in edges})
    handles = [plt.Line2D([0], [0], color=EDGE_STYLE[k]["color"],
                          linestyle=EDGE_STYLE[k]["style"], lw=2, label=k)
               for k in kinds]
    if handles:
        ax.legend(handles=handles, loc="lower right", fontsize=9, frameon=True)

    ax.set_title(f"{title}  ({cols} cycle)", fontsize=13, fontweight="bold", pad=6)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    return level
