"""
Anggota 1 - WAR (Write After Read)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_war


def main():
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs"), exist_ok=True)
    print("Instruction Set:")
    for ins in INSTRUCTIONS:
        print(f"{ins.name}: {ins}")
    edges = find_war(INSTRUCTIONS)
    print_dependencies(INSTRUCTIONS, edges, "WAR (Write After Read)")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs", "war.png")
    level = draw_graph(INSTRUCTIONS, edges, "Anggota 1 - Dependency Graph WAR", out)
    print_schedule(INSTRUCTIONS, level, "ILP EXECUTION - hanya WAR")
    print("\nGraph disimpan:", out)


if __name__ == "__main__":
    main()
