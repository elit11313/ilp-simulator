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


def schedule(instructions, edges):
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


NODE_INDEP = "#c8f0c8"
NODE_DEP = "#ffe9a8"


def draw_graph(instructions, edges, title, filename):
    level = schedule(instructions, edges)
    n, cols = len(instructions), max(level)

    LABEL_W, COLW, ROWH = 3.2, 1.55, 0.85
    BW, BH = 0.70, 0.50
    TOP, BOTTOM = 1.25, 1.25
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

    y_top, y_bot = H - TOP + 0.25, BOTTOM - 0.25
    for c in range(1, cols + 1):
        if c % 2 == 1:
            ax.add_patch(Rectangle((LABEL_W + COLW * (c - 1), y_bot), COLW,
                                   y_top - y_bot, fc="#f1f3f6", ec="none", zorder=0))
        ax.text(X(c), H - TOP + 0.45, f"Cycle {c}", ha="center", va="center",
                fontsize=12, fontweight="bold", color="#333")

    for i, ins in enumerate(instructions):
        ax.plot([0.1, W - 0.1], [Y(i) - ROWH / 2] * 2, color="#e3e3e3", lw=0.8, zorder=0)
        ax.text(0.2, Y(i), f"{ins.name}:  {ins}", ha="left", va="center",
                fontsize=12, fontweight="bold", family="monospace", color="#111")

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
    order = sorted(range(len(edges)),
                   key=lambda t: (level[edges[t][1]] - level[edges[t][0]],
                                  edges[t][1] - edges[t][0]))

    off_out, off_in, off_in_x = {}, {}, {}
    for node in range(n):
        outs = sorted([t for t, e in enumerate(edges) if e[0] == node],
                      key=lambda t: -edges[t][1])
        ins_ = sorted([t for t, e in enumerate(edges) if e[1] == node],
                      key=lambda t: -edges[t][0])
        for lst, dct in ((outs, off_out), (ins_, off_in)):
            # jarak antar titik dibatasi supaya semua titik tetap di dalam kotak
            step = min(0.26, (BH - 0.14) / max(len(lst) - 1, 1))
            for pos_i, t in enumerate(lst):
                dct[t] = (pos_i - (len(lst) - 1) / 2) * step
        ins_x = sorted([t for t, e in enumerate(edges) if e[1] == node],
                       key=lambda t: (level[edges[t][0]], edges[t][0]))
        step_x = min(0.40, (BW - 0.16) / max(len(ins_x) - 1, 1))
        for pos_i, t in enumerate(ins_x):
            off_in_x[t] = (pos_i - (len(ins_x) - 1) / 2) * step_x

    def inside(px, py, i):
        return (abs(px - X(level[i])) <= BW / 2 + 0.03
                and abs(py - Y(i)) <= BH / 2 + 0.03)

    for t in order:
        src, dst, reg, kind = edges[t]
        k = seen.get((src, dst), 0)
        seen[(src, dst)] = k + 1
        p0 = (X(level[src]), Y(src) + off_out[t])
        p2 = (X(level[dst]) + off_in_x[t], Y(dst) + off_in[t])
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
            outside = sum(1 for (px, py) in pts
                          if px < 0.3 or px > W - 0.3 or py < 0.3 or py > H - 0.3)
            score = hits(pts, {src, dst}) * 100 + lab * 30 + close * 6 + abs(rad) * 5 \
                + (0 if rad * pref >= 0 else 2) + (40 * k if abs(rad) < 0.1 * (k + 1) else 0) \
                + outside * 200
            if best is None or score < best[0]:
                best = (score, rad, mid)
        _, rad, mid = best
        taken_labels.append(mid)
        drawn_pts.extend(curve_pts(p0, p2, rad)[8:-8])
        st = EDGE_STYLE[kind]

        pts = curve_pts(p0, p2, rad, m=1500)
        i0 = 0
        while i0 < len(pts) - 1 and inside(pts[i0][0], pts[i0][1], src):
            i0 += 1
        i1 = len(pts) - 1
        while i1 > i0 and inside(pts[i1][0], pts[i1][1], dst):
            i1 -= 1
        seg = pts[i0:i1 + 1]
        tip = seg[-1]
        h = len(seg) - 1
        while h > 0 and ((seg[h][0] - tip[0]) ** 2 + (seg[h][1] - tip[1]) ** 2) ** 0.5 < 0.15:
            h -= 1

        ax.plot([q[0] for q in seg[:h + 1]], [q[1] for q in seg[:h + 1]],
                color=st["color"], linestyle=st["style"], linewidth=2.2,
                solid_capstyle="butt", dash_capstyle="butt", zorder=3)
        ax.add_patch(FancyArrowPatch(
            seg[h], tip, arrowstyle="-|>", mutation_scale=22,
            color=st["color"], linestyle="-", linewidth=2.2,
            shrinkA=0, shrinkB=0, zorder=4))

        ax.text(mid[0], mid[1], reg, ha="center", va="center", fontsize=11,
                fontweight="bold", color=st["color"], zorder=7,
                bbox=dict(fc="white", ec=st["color"], lw=0.8, pad=1.5,
                          boxstyle="round,pad=0.15"))

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
