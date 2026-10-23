"""Gabungan RAW + WAR + WAW - program per anggota."""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, ".."))
sys.path.insert(0, BASE)
import common
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_raw, find_war, find_waw

MEMBER = os.path.basename(BASE).replace("anggota", "Anggota ")


def main():
    os.makedirs(os.path.join(BASE, "graphs"), exist_ok=True)
    ins = INSTRUCTIONS
    n = len(ins)
    raw, war, waw = find_raw(ins), find_war(ins), find_waw(ins)
    comb = raw + war + waw
    print("Instruction Set:")
    for i in ins:
        print(f"{i.name}: {i}")
    print_dependencies(ins, comb, "RAW + WAR + WAW")
    out = os.path.join(BASE, "graphs", "semua.png")
    level = draw_graph(ins, comb, f"{MEMBER} - Dependency Graph RAW + WAR + WAW", out)
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
