"""
Anggota 1 - RAW (Read After Write)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_raw


def main():
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs"), exist_ok=True)
    print("Instruction Set:")
    for ins in INSTRUCTIONS:
        print(f"{ins.name}: {ins}")
    edges = find_raw(INSTRUCTIONS)
    print_dependencies(INSTRUCTIONS, edges, "RAW (Read After Write)")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs", "raw.png")
    level = draw_graph(INSTRUCTIONS, edges, "Anggota 1 - Dependency Graph RAW", out)
    print_schedule(INSTRUCTIONS, level, "ILP EXECUTION - hanya RAW")
    print("\nGraph disimpan:", out)


if __name__ == "__main__":
    main()
