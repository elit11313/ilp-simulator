"""Instruction set milik Anggota 1."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R1", ['R2', 'R3']),
    Instruction("I2", "R2", ['R1', 'R4']),
    Instruction("I3", "R1", ['R5', 'R6']),
    Instruction("I4", "R3", ['R2', 'R1']),
    Instruction("I5", "R2", ['R3', 'R7']),
    Instruction("I6", "R1", ['R2', 'R8']),
    Instruction("I7", "R3", ['R1', 'R5']),
    Instruction("I8", "R4", ['R3', 'R2']),
    Instruction("I9", "R2", ['R4', 'R6']),
    Instruction("I10", "R1", ['R3', 'R9']),
    Instruction("I11", "R3", ['R2', 'R4']),
    Instruction("I12", "R4", ['R1', 'R3']),
]
