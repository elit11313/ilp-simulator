"""Instruction set milik Anggota 1."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R1", ['R2', 'R3']),
    Instruction("I2", "R4", ['R1', 'R5']),
    Instruction("I3", "R1", ['R6', 'R7']),
    Instruction("I4", "R8", ['R1', 'R4']),
    Instruction("I5", "R4", ['R9', 'R10']),
    Instruction("I6", "R11", ['R8', 'R4']),
    Instruction("I7", "R12", ['R13', 'R14']),
]
