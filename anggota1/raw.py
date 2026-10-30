import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # supaya common.py terbaca

from common import Instruction, run_analysis

KIND = "RAW"

INSTRUCTIONS = [
    Instruction("I1",  "R1",  ["R2", "R3"],   "+"),   # independen, tulis R1
    Instruction("I2",  "R4",  ["R1", "R5"],   "*"),   # baca R1 dari I1
    Instruction("I3",  "R6",  ["R7", "R8"],   "-"),   # independen, tulis R6
    Instruction("I4",  "R9",  ["R4", "R6"],   "+"),   # baca R4 (I2), R6 (I3)
    Instruction("I5",  "R10", ["R11", "R12"], "+"),   # independen, tulis R10
    Instruction("I6",  "R13", ["R9", "R10"],  "-"),   # baca R9 (I4), R10 (I5)
    Instruction("I7",  "R14", ["R15", "R16"], "+"),   # independen, tulis R14
    Instruction("I8",  "R17", ["R13", "R14"], "*"),   # baca R13 (I6), R14 (I7)
    Instruction("I9",  "R18", ["R19", "R20"], "+"),   # independen, tulis R18
    Instruction("I10", "R21", ["R17", "R18"], "-"),   # baca R17 (I8), R18 (I9)
    Instruction("I11", "R22", ["R23", "R24"], "+"),   # independen, tulis R22
    Instruction("I12", "R25", ["R21", "R22"], "*"),   # baca R21 (I10), R22 (I11)
    Instruction("I13", "R26", ["R27", "R28"], "+"),   # independen, tulis R26
    Instruction("I14", "R29", ["R25", "R26"], "-"),   # baca R25 (I12), R26 (I13)
    Instruction("I15", "R30", ["R29", "R31"], "+"),   # baca R29 (I14), R31 dari luar
]


def main():
    return run_analysis(KIND, INSTRUCTIONS, graph_dir=HERE)


if __name__ == "__main__":
    main()
