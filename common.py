"""
common.py
Bagian bersama: definisi instruksi, scheduler ILP, dan penggambar dependency graph.
"""

from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D


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
NODE_INDEP = "#c8f0c8"   # hijau  : instruksi independen (tanpa dependensi)
NODE_DEP = "#ffe9a8"     # kuning : instruksi dependen


def draw_graph(instructions, edges, title, filename):
    """
    Tata letak: baris = instruksi, kolom = cycle.
    Panah berbentuk siku-siku: keluar dari sisi kanan kotak asal, turun lewat
    jalur (lane) tersendiri di sela kolom, lalu masuk ke sisi kiri kotak tujuan.
    Karena tiap baris hanya berisi satu kotak, garis tidak pernah menembus kotak
    lain, dan ujung panah selalu menempel di kotak tujuan.
    """
    level = schedule(instructions, edges)
    n, cols = len(instructions), max(level)
    n_edges = len(edges)
    dense = n_edges > 30

    # ---- jalur vertikal (lane): satu jalur per panah, jalur dipakai bersama
    #      hanya oleh panah yang rentang barisnya tidak bertumpuk ----
    lane_of, nlanes = {}, {}
    for c in range(1, cols + 1):
        idx = [t for t, e in enumerate(edges) if level[e[1]] == c]
        idx.sort(key=lambda t: (edges[t][0], -edges[t][1]))
        lanes_end = []                     # baris terakhir yang dipakai tiap lane
        for t in idx:
            s_row, d_row = edges[t][0], edges[t][1]
            for li, last in enumerate(lanes_end):
                if last < s_row:
                    lanes_end[li] = d_row
                    lane_of[t] = li
                    break
            else:
                lanes_end.append(d_row)
                lane_of[t] = len(lanes_end) - 1
        nlanes[c] = max(len(lanes_end), 1)

    BW, BH = 0.70, (0.80 if dense else 0.66)
    LANE_SP = 0.16
    need = max(nlanes.values()) * LANE_SP + 0.5
    COLW = max(1.9, BW + need)
    ROWH = 1.25 if dense else 1.0
    LABEL_W, TOP, BOTTOM = 3.4, 1.35, 1.35
    W = LABEL_W + COLW * cols + 0.4
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
        ax.text(X(c), H - TOP + 0.5, f"Cycle {c}", ha="center", va="center",
                fontsize=12, fontweight="bold", color="#333")

    # ---- baris: garis tipis + teks instruksi ----
    for i, ins in enumerate(instructions):
        ax.plot([0.1, W - 0.1], [Y(i) - ROWH / 2] * 2, color="#e3e3e3", lw=0.8, zorder=0)
        ax.text(0.2, Y(i), f"{ins.name}:  {ins}", ha="left", va="center",
                fontsize=12, fontweight="bold", family="monospace", color="#111")

    # ---- titik keluar / masuk panah, disebar di sisi kotak ----
    span = BH - 0.14
    off_out, off_in = {}, {}
    for node in range(n):
        outs = sorted([t for t, e in enumerate(edges) if e[0] == node],
                      key=lambda t: (edges[t][1], edges[t][3]))
        ins_ = sorted([t for t, e in enumerate(edges) if e[1] == node],
                      key=lambda t: (edges[t][0], edges[t][3]))
        for lst, dct in ((outs, off_out), (ins_, off_in)):
            k = len(lst)
            for pos_i, t in enumerate(lst):
                dct[t] = ((k - 1) / 2 - pos_i) * (span / (k - 1)) if k > 1 else 0.0

    # ---- node ----
    has_pred = {e[1] for e in edges}
    for i, ins in enumerate(instructions):
        x, y = X(level[i]), Y(i)
        ax.add_patch(FancyBboxPatch(
            (x - BW / 2, y - BH / 2), BW, BH,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            fc=NODE_DEP if i in has_pred else NODE_INDEP,
            ec="#222", lw=1.8, zorder=5))
        ax.text(x, y, ins.name, ha="center", va="center", fontsize=13,
                fontweight="bold", zorder=6)

    # ---- panah siku-siku ----
    lw = 1.7 if dense else 2.2
    fs_label = 8 if dense else 10
    HEAD = 0.17
    labels = []
    for t, (src, dst, reg, kind) in enumerate(edges):
        st = EDGE_STYLE[kind]
        c_d = level[dst]
        x0 = X(level[src]) + BW / 2 + 0.03
        y0 = Y(src) + off_out[t]
        x3 = X(c_d) - BW / 2 - 0.03
        y3 = Y(dst) + off_in[t]
        xl = X(c_d) - BW / 2 - 0.30 - lane_of[t] * LANE_SP     # posisi lane
        xl = min(xl, x3 - HEAD - 0.04)
        xl = max(xl, x0 + 0.08)
        ax.plot([x0, xl, xl, x3 - HEAD], [y0, y0, y3, y3], color=st["color"],
                linestyle=st["style"], linewidth=lw, solid_capstyle="butt",
                dash_capstyle="butt", solid_joinstyle="round", zorder=3)
        ax.add_patch(FancyArrowPatch(
            (x3 - HEAD, y3), (x3, y3), arrowstyle="-|>",
            mutation_scale=16 if dense else 20, color=st["color"],
            linestyle="-", linewidth=lw, shrinkA=0, shrinkB=0, zorder=4))
        # label di jalur vertikal, posisinya diacak agar tidak bertumpuk
        f = 0.35 + 0.30 * ((lane_of[t] * 3 + t) % 5) / 4
        labels.append((xl, y0 + (y3 - y0) * f, reg, st["color"]))

    for lx, ly, reg, col in labels:
        ax.text(lx, ly, reg, ha="center", va="center", fontsize=fs_label,
                fontweight="bold", color=col, zorder=7,
                bbox=dict(fc="white", ec=col, lw=0.8, pad=1.0,
                          boxstyle="round,pad=0.10"))

    # ---- catatan: instruksi yang hasilnya ditimpa sebelum sempat dibaca ----
    notes = []
    out_nodes = {e[0] for e in edges}
    for i, ins in enumerate(instructions):
        if i in out_nodes:
            continue
        for j in range(i + 1, n):
            if ins.destination in instructions[j].sources:
                break
            if instructions[j].destination == ins.destination:
                notes.append(f"{ins.name} tidak punya panah keluar: {ins.destination} "
                             f"ditimpa {instructions[j].name} sebelum dibaca instruksi mana pun.")
                break
    for q, txt in enumerate(notes):
        ax.text(0.2, BOTTOM - 0.55 - 0.28 * q, "Catatan: " + txt, ha="left",
                va="center", fontsize=10, style="italic", color="#444")

    # ---- judul + legenda ----
    ax.text(W / 2, H - 0.4, f"{title}  ({cols} cycle, {n_edges} dependensi)",
            ha="center", va="center", fontsize=15, fontweight="bold")
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
