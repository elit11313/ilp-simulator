"""
hazards.py
Deteksi tiga jenis data hazard antar instruksi.
a = instruksi lebih awal, b = instruksi lebih akhir (urutan program).
"""

from collections import namedtuple

Dependency = namedtuple("Dependency", "first second kind register")


def find_raw(instructions):
    """RAW: b MEMBACA register yang DITULIS a (true dependence)."""
    deps = []
    for i, a in enumerate(instructions):
        for b in instructions[i + 1:]:
            if a.destination in b.sources:
                deps.append(Dependency(a.name, b.name, "RAW", a.destination))
    return deps


def find_war(instructions):
    """WAR: b MENULIS register yang DIBACA a (anti-dependence)."""
    deps = []
    for i, a in enumerate(instructions):
        for b in instructions[i + 1:]:
            if b.destination in a.sources:
                deps.append(Dependency(a.name, b.name, "WAR", b.destination))
    return deps


def find_waw(instructions):
    """WAW: a dan b sama-sama MENULIS register yang sama (output dependence)."""
    deps = []
    for i, a in enumerate(instructions):
        for b in instructions[i + 1:]:
            if a.destination == b.destination:
                deps.append(Dependency(a.name, b.name, "WAW", a.destination))
    return deps


FINDERS = {"RAW": find_raw, "WAR": find_war, "WAW": find_waw}


def find_dependencies(instructions, kinds=("RAW", "WAR", "WAW")):
    deps = []
    for kind in kinds:
        deps.extend(FINDERS[kind](instructions))
    return deps
