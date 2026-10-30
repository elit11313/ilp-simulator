import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from common import Instruction, run_analysis

KIND = "WAW"

INSTRUCTIONS = [
    Instruction("I1",  "R1",  ["R2", "R3"],   "+"),   # tulis R1 (pertama)
    Instruction("I2",  "R4",  ["R5", "R6"],   "*"),   # tulis R4 (pertama)
    Instruction("I3",  "R1",  ["R7", "R8"],   "-"),   # tulis R1 (kedua), WAW dgn I1
    Instruction("I4",  "R9",  ["R10", "R11"], "+"),   # tulis R9 (pertama)
    Instruction("I5",  "R4",  ["R12", "R13"], "+"),   # tulis R4 (kedua), WAW dgn I2
    Instruction("I6",  "R1",  ["R14", "R15"], "*"),   # tulis R1 (ketiga), WAW dgn I1, I3
    Instruction("I7",  "R9",  ["R16", "R17"], "+"),   # tulis R9 (kedua), WAW dgn I4
    Instruction("I8",  "R20", ["R18", "R19"], "-"),   # tulis R20 (pertama)
    Instruction("I9",  "R1",  ["R21", "R22"], "+"),   # tulis R1 (keempat), WAW dgn I1, I3, I6
    Instruction("I10", "R4",  ["R23", "R24"], "*"),   # tulis R4 (ketiga), WAW dgn I2, I5
    Instruction("I11", "R25", ["R26", "R27"], "+"),   # tulis R25 (pertama)
    Instruction("I12", "R20", ["R28", "R29"], "-"),   # tulis R20 (kedua), WAW dgn I8
    Instruction("I13", "R25", ["R30", "R31"], "+"),   # tulis R25 (kedua), WAW dgn I11
    Instruction("I14", "R9",  ["R32", "R33"], "*"),   # tulis R9 (ketiga), WAW dgn I4, I7
    Instruction("I15", "R1",  ["R34", "R35"], "+"),   # tulis R1 (kelima), WAW dgn I1, I3, I6, I9
]


def main():
    return run_analysis(KIND, INSTRUCTIONS, graph_dir=HERE)


if __name__ == "__main__":
    main()
