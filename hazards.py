"""
hazards.py - deteksi RAW, WAR, WAW (dipakai semua program anggota).
Edge berupa tuple (idx_dari, idx_ke, register, tipe).
"""


def has_raw(earlier, later):
    """RAW: `later` membaca register yang ditulis `earlier`."""
    return earlier.destination in later.sources


def has_war(earlier, later):
    """WAR: `later` menulis register yang dibaca `earlier`."""
    return later.destination in earlier.sources


def has_waw(earlier, later):
    """WAW: keduanya menulis register yang sama."""
    return earlier.destination == later.destination


def find_raw(ins):
    """RAW: hanya penulis terakhir sebelum j (dependensi data asli)."""
    edges = set()
    for j, cur in enumerate(ins):
        for reg in cur.sources:
            for i in range(j - 1, -1, -1):
                if ins[i].destination == reg:
                    edges.add((i, j, reg, "RAW"))
                    break
    return sorted(edges, key=lambda e: (e[1], e[0]))


def find_war(ins):
    """WAR: SEMUA pasangan (i membaca reg, j > i menulis reg yang sama)."""
    edges = set()
    for i, reader in enumerate(ins):
        for reg in reader.sources:
            for j in range(i + 1, len(ins)):
                if ins[j].destination == reg:
                    edges.add((i, j, reg, "WAR"))
    return sorted(edges, key=lambda e: (e[1], e[0]))


def find_waw(ins):
    """WAW: SEMUA pasangan (i dan j > i menulis register yang sama)."""
    edges = set()
    for i, first in enumerate(ins):
        for j in range(i + 1, len(ins)):
            if has_waw(first, ins[j]):
                edges.add((i, j, first.destination, "WAW"))
    return sorted(edges, key=lambda e: (e[1], e[0]))
