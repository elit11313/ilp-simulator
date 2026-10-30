from ilp_core import Instruction, run_full_analysis

instructions = [
    Instruction("I1", "R1",  ["R2", "R3"],   "+"),   # baca R2 dan R3
    Instruction("I2", "R2",  ["R4", "R5"],   "-"),   # tulis R2 (dibaca I1)
    Instruction("I3", "R6",  ["R7", "R8"],   "*"),   # baca R7
    Instruction("I4", "R7",  ["R9", "R10"],  "+"),   # tulis R7 (dibaca I3)
    Instruction("I5", "R11", ["R12", "R13"], "-"),   # baca R12
    Instruction("I6", "R12", ["R14", "R15"], "+"),   # tulis R12 (dibaca I5)
    Instruction("I7", "R3",  ["R16", "R17"], "+"),   # tulis R3 (dibaca I1)
    Instruction("I8", "R16", ["R18", "R19"], "*"),   # tulis R16 (dibaca I7)
]

if __name__ == "__main__":
    run_full_analysis("WAR", instructions, "war_graph.dot")
