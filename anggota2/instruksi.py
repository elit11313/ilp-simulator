"""Instruction set milik Anggota 2."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import Instruction

INSTRUCTIONS = [
    Instruction("I1", "R1", ['R2', 'R3']),
    Instruction("I2", "R3", ['R1', 'R4']),
    Instruction("I3", "R2", ['R3', 'R5']),
    Instruction("I4", "R1", ['R6', 'R2']),
    Instruction("I5", "R3", ['R7', 'R1']),
    Instruction("I6", "R2", ['R1', 'R8']),
    Instruction("I7", "R4", ['R2', 'R3']),
    Instruction("I8", "R1", ['R4', 'R9']),
    Instruction("I9", "R3", ['R1', 'R2']),
    Instruction("I10", "R2", ['R4', 'R5']),
    Instruction("I11", "R4", ['R3', 'R6']),
    Instruction("I12", "R1", ['R2', 'R4']),
]
