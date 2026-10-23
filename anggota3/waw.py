"""WAW (Write After Write) - program per anggota."""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, ".."))
sys.path.insert(0, BASE)
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_waw

MEMBER = os.path.basename(BASE).replace("anggota", "Anggota ")


def main():
    os.makedirs(os.path.join(BASE, "graphs"), exist_ok=True)
    print("Instruction Set:")
    for ins in INSTRUCTIONS:
        print(f"{ins.name}: {ins}")
    edges = find_waw(INSTRUCTIONS)
    print_dependencies(INSTRUCTIONS, edges, "WAW (Write After Write)")
    out = os.path.join(BASE, "graphs", "waw.png")
    level = draw_graph(INSTRUCTIONS, edges, f"{MEMBER} - Dependency Graph WAW", out)
    print_schedule(INSTRUCTIONS, level, "ILP EXECUTION - hanya WAW")
    print("\nGraph disimpan:", out)


if __name__ == "__main__":
    main()
