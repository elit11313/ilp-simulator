import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from common import Instruction, run_analysis

KIND = "WAR"

INSTRUCTIONS = [
    Instruction("I1",  "R1",  ["R2", "R3"],   "+"),   # baca R2, R3
    Instruction("I2",  "R2",  ["R4", "R5"],   "-"),   # tulis R2 (dibaca I1)
    Instruction("I3",  "R6",  ["R7", "R8"],   "*"),   # baca R7, R8
    Instruction("I4",  "R7",  ["R9", "R10"],  "+"),   # tulis R7 (dibaca I3)
    Instruction("I5",  "R11", ["R12", "R13"], "-"),   # baca R12, R13
    Instruction("I6",  "R12", ["R14", "R15"], "+"),   # tulis R12 (dibaca I5)
    Instruction("I7",  "R3",  ["R16", "R17"], "+"),   # tulis R3 (dibaca I1), baca R16
    Instruction("I8",  "R16", ["R18", "R19"], "*"),   # tulis R16 (dibaca I7)
    Instruction("I9",  "R20", ["R21", "R22"], "+"),   # baca R21, R22
    Instruction("I10", "R21", ["R23", "R24"], "-"),   # tulis R21 (dibaca I9)
    Instruction("I11", "R25", ["R26", "R27"], "+"),   # baca R26, R27
    Instruction("I12", "R26", ["R28", "R29"], "*"),   # tulis R26 (dibaca I11)
    Instruction("I13", "R27", ["R30", "R31"], "+"),   # tulis R27 (dibaca I11), baca R30
    Instruction("I14", "R30", ["R32", "R33"], "-"),   # tulis R30 (dibaca I13), baca R32
    Instruction("I15", "R32", ["R34", "R35"], "+"),   # tulis R32 (dibaca I14)
]


def main():
    return run_analysis(KIND, INSTRUCTIONS, graph_dir=HERE)


if __name__ == "__main__":
    main()
