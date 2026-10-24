"""WAR (Write After Read) - program per anggota."""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, ".."))
sys.path.insert(0, BASE)
from common import draw_graph, print_dependencies, print_schedule
from instruksi import INSTRUCTIONS
from hazards import find_war

MEMBER = os.path.basename(BASE).replace("anggota", "Anggota ")


def main():
    os.makedirs(os.path.join(BASE, "graphs"), exist_ok=True)
    print("Instruction Set:")
    for ins in INSTRUCTIONS:
        print(f"{ins.name}: {ins}")
    edges = find_war(INSTRUCTIONS)
    print_dependencies(INSTRUCTIONS, edges, "WAR (Write After Read)")
    out = os.path.join(BASE, "graphs", "war.png")
    level = draw_graph(INSTRUCTIONS, edges, f"{MEMBER} - Dependency Graph WAR", out)
    print_schedule(INSTRUCTIONS, level, "ILP EXECUTION - hanya WAR")
    print("\nGraph disimpan:", out)


if __name__ == "__main__":
    main()
