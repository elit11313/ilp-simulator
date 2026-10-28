"""Instruction set milik Anggota 2."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R4", ['R2', 'R1']),
    Instruction("I2", "R1", ['R3', 'R4']),
    Instruction("I3", "R4", ['R1', 'R2']),
    Instruction("I4", "R20", ['R21', 'R22']),
    Instruction("I5", "R2", ['R1', 'R4']),
    Instruction("I6", "R1", ['R7', 'R2']),
    Instruction("I7", "R4", ['R3', 'R6']),
    Instruction("I8", "R2", ['R7', 'R1']),
    Instruction("I9", "R4", ['R2', 'R7']),
    Instruction("I10", "R23", ['R24', 'R25']),
    Instruction("I11", "R2", ['R1', 'R4']),
    Instruction("I12", "R26", ['R27', 'R28']),
]
