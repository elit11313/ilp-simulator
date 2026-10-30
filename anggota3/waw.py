import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from common import Instruction, run_analysis

KIND = "WAW"

INSTRUCTIONS = [
    Instruction("I1", "R1", ["R2", "R3"],   "+"),    # tulis R1
    Instruction("I2", "R4", ["R5", "R6"],   "*"),    # tulis R4
    Instruction("I3", "R1", ["R7", "R8"],   "-"),    # tulis R1 lagi (WAW dgn I1)
    Instruction("I4", "R9", ["R10", "R11"], "+"),    # tulis R9
    Instruction("I5", "R4", ["R12", "R13"], "+"),    # tulis R4 lagi (WAW dgn I2)
    Instruction("I6", "R1", ["R14", "R15"], "*"),    # tulis R1 ketiga
    Instruction("I7", "R1", ["R16", "R17"], "+"),    # tulis R1 keempat
    Instruction("I8", "R9", ["R18", "R19"], "-"),    # tulis R9 lagi (WAW dgn I4)
]


def main():
    return run_analysis(KIND, INSTRUCTIONS, graph_dir=HERE)


if __name__ == "__main__":
    main()
