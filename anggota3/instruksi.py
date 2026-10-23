"""Instruction set milik Anggota 3."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R1", ['R2', 'R3']),
    Instruction("I2", "R1", ['R4', 'R5']),
    Instruction("I3", "R6", ['R1', 'R7']),
    Instruction("I4", "R1", ['R8', 'R9']),
    Instruction("I5", "R10", ['R1', 'R6']),
    Instruction("I6", "R2", ['R11', 'R12']),
    Instruction("I7", "R13", ['R14', 'R15']),
]
