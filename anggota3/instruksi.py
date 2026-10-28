"""Instruction set milik Anggota 3."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R2", ['R1', 'R3']),
    Instruction("I2", "R1", ['R2', 'R4']),
    Instruction("I3", "R3", ['R5', 'R1']),
    Instruction("I4", "R2", ['R3', 'R6']),
    Instruction("I5", "R1", ['R2', 'R7']),
    Instruction("I6", "R4", ['R1', 'R3']),
    Instruction("I7", "R3", ['R4', 'R8']),
    Instruction("I8", "R2", ['R3', 'R1']),
    Instruction("I9", "R1", ['R4', 'R9']),
    Instruction("I10", "R4", ['R2', 'R5']),
    Instruction("I11", "R3", ['R1', 'R4']),
    Instruction("I12", "R2", ['R3', 'R6']),
]
