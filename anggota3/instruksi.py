"""Instruction set milik Anggota 3."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R20", ['R21', 'R22']),
    Instruction("I2", "R2", ['R4', 'R6']),
    Instruction("I3", "R23", ['R24', 'R25']),
    Instruction("I4", "R3", ['R2', 'R1']),
    Instruction("I5", "R2", ['R3', 'R5']),
    Instruction("I6", "R1", ['R2', 'R3']),
    Instruction("I7", "R1", ['R2', 'R4']),
    Instruction("I8", "R2", ['R6', 'R1']),
    Instruction("I9", "R3", ['R1', 'R5']),
    Instruction("I10", "R26", ['R27', 'R28']),
    Instruction("I11", "R1", ['R3', 'R2']),
    Instruction("I12", "R2", ['R6', 'R1']),
]
