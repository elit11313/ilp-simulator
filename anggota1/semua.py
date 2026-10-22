"""
Anggota 1 - Gabungan RAW + WAR + WAW
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
import common
from hazards import find_raw, find_war, find_waw


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base, "graphs"), exist_ok=True)
    ins = INSTRUCTIONS
    n = len(ins)
    raw, war, waw = find_raw(ins), find_war(ins), find_waw(ins)
    comb = raw + war + waw
    print("Instruction Set:")
    for i in ins:
        print(f"{i.name}: {i}")
    print_dependencies(ins, comb, "RAW + WAR + WAW")
    out = os.path.join(base, "graphs", "semua.png")
    level = draw_graph(ins, comb, "Anggota 1 - Dependency Graph RAW + WAR + WAW", out)
    print_schedule(ins, level, "ILP EXECUTION - RAW + WAR + WAW")

    print("\n" + "=" * 56)
    print("PERFORMANCE COMPARISON")
    print("=" * 56)
    print(f"{'Skenario':<38}{'Cycle':>6}{'Speedup':>9}")
    for name, e in [("Sequential", None), ("RAW saja (renaming ideal)", raw),
                    ("RAW + WAR", raw + war), ("RAW + WAW", raw + waw),
                    ("RAW + WAR + WAW (tanpa renaming)", comb)]:
        c = n if e is None else max(common.schedule(ins, e))
        print(f"{name:<38}{c:>6}{n / c:>8.2f}x")


if __name__ == "__main__":
    main()
