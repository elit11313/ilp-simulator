"""
Inti simulator ILP: model instruksi, penjadwalan per cycle, register renaming,
dependency graph, dan analisis lengkap satu jenis hazard.
Dikembangkan dari simulator ILP Pak Mulya Agung (RAW saja -> RAW/WAR/WAW).
"""

import os
import re
from dataclasses import dataclass

from hazards import find_dependencies

ISSUE_WIDTH = 4
KINDS = ("RAW", "WAR", "WAW")
COLORS = {"RAW": "red", "WAR": "blue", "WAW": "green"}


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list
    op: str = "+"

    def text(self):
        return f"{self.destination} = {f' {self.op} '.join(self.sources)}"


def schedule(instructions, deps, width=ISSUE_WIDTH):
    """Instruksi jalan jika semua yang ditunggu selesai di cycle sebelumnya."""
    preds = {ins.name: set() for ins in instructions}
    for d in deps:
        preds[d.second].add(d.first)

    done, remaining, cycles = set(), list(instructions), []
    while remaining:
        ready = [i for i in remaining if preds[i.name] <= done][:width]
        cycles.append(ready)
        done.update(i.name for i in ready)
        remaining = [i for i in remaining if i.name not in done]
    return cycles


def print_schedule(title, cycles):
    print("\n" + "=" * 58)
    print(title)
    print("=" * 58)
    for n, group in enumerate(cycles, 1):
        print(f"Cycle {n}: " + ", ".join(i.name for i in group))
        for i in group:
            print(f"   -> {i.name}: {i.text()}")
    print(f"Total cycles: {len(cycles)}")
    return len(cycles)


def rename(instructions):
    """Register renaming (slide 6: F0 -> F8, F4 -> F9)."""
    numbers = [int(m.group(1))
               for ins in instructions
               for r in [ins.destination] + list(ins.sources)
               for m in [re.fullmatch(r"R(\d+)", r)] if m]
    nxt = max(numbers) + 1

    table, out = {}, []
    for ins in instructions:
        srcs = [table.get(s, s) for s in ins.sources]
        new = f"R{nxt}"
        nxt += 1
        table[ins.destination] = new
        out.append(Instruction(ins.name, new, srcs, ins.op))
    return out


def draw_graph(instructions, deps, filename, title):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib belum terpasang: pip install -r requirements.txt")
        return

    levels = schedule(instructions, deps, width=len(instructions))
    pos = {}
    for y, group in enumerate(levels):
        for k, ins in enumerate(group):
            pos[ins.name] = ((k - (len(group) - 1) / 2) * 2.8, -y * 2.2)

    xs = [p[0] for p in pos.values()]
    fig, ax = plt.subplots(figsize=((max(xs) - min(xs) + 8) * 0.62,
                                    (len(levels) * 2.2 + 1.5) * 0.62))

    for ins in instructions:
        x, y = pos[ins.name]
        ax.text(x, y, f"{ins.name}\n{ins.text()}", ha="center", va="center",
                fontsize=9, zorder=3,
                bbox=dict(boxstyle="round,pad=0.4", fc="#f5f5f5", ec="black"))

    for d in deps:
        (x1, y1), (x2, y2) = pos[d.first], pos[d.second]
        rad = 0.25 if abs(y1 - y2) > 2.3 else 0.0
        col = COLORS[d.kind]
        ax.annotate("", xy=(x2, y2 + 0.4), xytext=(x1, y1 - 0.4), zorder=1,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5,
                                    connectionstyle=f"arc3,rad={rad}"))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{d.kind} ({d.register})",
                color=col, fontsize=8, ha="center", va="center", zorder=2,
                bbox=dict(fc="white", ec="none", pad=0.5))

    for y in range(len(levels)):
        ax.text(min(xs) - 3.6, -y * 2.2, f"Cycle {y + 1}", fontsize=9,
                color="gray", ha="left", va="center")

    ax.set_xlim(min(xs) - 4.5, max(xs) + 2.5)
    ax.set_ylim(-(len(levels) - 1) * 2.2 - 1.2, 1.2)
    ax.set_title(title, fontsize=12)
    ax.axis("off")
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Dependency graph (PNG) disimpan: {filename}")


def export_dot(instructions, deps, filename):
    lines = ["digraph G {", "  rankdir=TB;", "  node [shape=box, style=rounded];"]
    for i in instructions:
        lines.append(f'  {i.name} [label="{i.name}\\n{i.text()}"];')
    for d in deps:
        c = COLORS[d.kind]
        lines.append(f'  {d.first} -> {d.second} [label="{d.kind} ({d.register})", '
                     f'color={c}, fontcolor={c}];')
    lines.append("}")
    with open(filename, "w") as f:
        f.write("\n".join(lines))
    print(f"Dependency graph (DOT) disimpan: {filename}")


def run_analysis(kind, instructions, graph_dir="."):
    os.makedirs(graph_dir, exist_ok=True)
    n = len(instructions)

    print("\n" + "*" * 62)
    print(f"      SIMULATOR ILP - ANALISIS HAZARD {kind}")
    print("*" * 62)

    print("\nDaftar instruksi:")
    for ins in instructions:
        print(f"  {ins.name}: {ins.text()}")

    deps = find_dependencies(instructions, (kind,))
    print(f"\nANALISIS DEPENDENSI ({kind})")
    for d in deps:
        print(f"  {d.second} {d.kind}-depends on {d.first}  (register {d.register})")
    print(f"  Jumlah dependensi {kind}: {len(deps)}")
    others = {k: len(find_dependencies(instructions, (k,))) for k in KINDS if k != kind}
    print(f"  Hazard jenis lain pada program ini: {others}")

    ideal = print_schedule("ILP IDEAL (tanpa hazard)", schedule(instructions, []))
    haz = print_schedule(f"ILP DENGAN HAZARD {kind}", schedule(instructions, deps))
    critical = len(schedule(instructions, deps, width=n))

    speedup = n / haz
    print("\n" + "=" * 58)
    print("PERFORMANCE COMPARISON")
    print("=" * 58)
    print(f"Sequential cycles                 : {n}")
    print(f"ILP ideal (tanpa hazard)          : {ideal}")
    print(f"ILP dengan hazard {kind}            : {haz}")
    print(f"Penalti akibat hazard             : {haz - ideal} cycle")
    print(f"Critical path                     : {critical} instruksi")
    print(f"Speedup vs sekuensial             : {speedup:.2f}x")
    print(f"Speedup ideal                     : {n / ideal:.2f}x")
    print(f"ILP Efficiency (rumus Pak Agung)  : {speedup / n * 100:.2f}%")
    print(f"Efisiensi terhadap ideal          : {ideal / haz * 100:.2f}%")

    draw_graph(instructions, deps,
               os.path.join(graph_dir, f"{kind.lower()}_graph.png"),
               f"Dependency Graph {kind}")
    export_dot(instructions, deps,
               os.path.join(graph_dir, f"{kind.lower()}_graph.dot"))

    renamed = rename(instructions)
    print("\nSETELAH REGISTER RENAMING")
    for ins in renamed:
        print(f"  {ins.name}: {ins.text()}")
    left = {k: len(find_dependencies(renamed, (k,))) for k in KINDS}
    print(f"  Sisa dependensi: {left}")
    after = print_schedule("ILP SETELAH RENAMING",
                           schedule(renamed, find_dependencies(renamed)))

    return {"kind": kind, "n": n, "deps": len(deps), "critical": critical,
            "ideal": ideal, "hazard": haz, "renamed": after,
            "speedup": speedup, "efficiency": speedup / n * 100}
