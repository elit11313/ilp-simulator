"""
Anggota 1 - WAW (Write After Write)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_waw


def main():
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs"), exist_ok=True)
    print("Instruction Set:")
    for ins in INSTRUCTIONS:
        print(f"{ins.name}: {ins}")
    edges = find_waw(INSTRUCTIONS)
    print_dependencies(INSTRUCTIONS, edges, "WAW (Write After Write)")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs", "waw.png")
    level = draw_graph(INSTRUCTIONS, edges, "Anggota 1 - Dependency Graph WAW", out)
    print_schedule(INSTRUCTIONS, level, "ILP EXECUTION - hanya WAW")
    print("\nGraph disimpan:", out)


if __name__ == "__main__":
    main()
