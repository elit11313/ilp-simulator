import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # supaya common.py terbaca

from common import Instruction, run_analysis

KIND = "RAW"

INSTRUCTIONS = [
    Instruction("I1", "R1",  ["R2", "R3"],   "+"),
    Instruction("I2", "R4",  ["R1", "R5"],   "*"),   # baca R1 dari I1
    Instruction("I3", "R6",  ["R7", "R8"],   "-"),
    Instruction("I4", "R9",  ["R4", "R6"],   "+"),   # baca R4 (I2), R6 (I3)
    Instruction("I5", "R10", ["R11", "R12"], "+"),
    Instruction("I6", "R13", ["R9", "R10"],  "-"),   # baca R9 (I4), R10 (I5)
    Instruction("I7", "R14", ["R15", "R16"], "+"),
    Instruction("I8", "R17", ["R13", "R14"], "*"),   # baca R13 (I6), R14 (I7)
]


def main():
    return run_analysis(KIND, INSTRUCTIONS, graph_dir=HERE)


if __name__ == "__main__":
    main()
