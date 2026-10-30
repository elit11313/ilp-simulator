"""
run_all.py
Menjalankan skrip tiap anggota (anggota1/, anggota2/, anggota3/), mencatat
status OK/GAGAL beserta waktunya, lalu menampilkan tabel ringkasan.
"""

import importlib.util
import os
import sys
import time
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)   # agar common.py dan hazards.py terbaca

SCRIPTS = [
    ("anggota1", "anggota1_raw.py"),
    ("anggota2", "anggota2_war.py"),
    ("anggota3", "anggota3_waw.py"),
]


def load_module(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    results, status = [], []

    for folder, filename in SCRIPTS:
        path = os.path.join(ROOT, folder, filename)
        label = f"{folder}/{filename}"
        start = time.perf_counter()
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File tidak ditemukan: {path}")
            results.append(load_module(path).main())
            status.append((label, "OK", time.perf_counter() - start))
        except Exception:
            traceback.print_exc()
            status.append((label, "GAGAL", time.perf_counter() - start))

    print("\n\n" + "#" * 78)
    print("STATUS SKRIP")
    print("#" * 78)
    for label, st, sec in status:
        print(f"  {label:<30} {st:<6} ({sec:.2f} detik)")

    if results:
        print("\n" + "#" * 78)
        print("RINGKASAN PERBANDINGAN")
        print("#" * 78)
        header = (f"{'Hazard':<7}{'Dep':>5}{'Crit':>6}{'Seq':>5}{'Ideal':>7}"
                  f"{'Hazard':>8}{'Rename':>8}{'Speedup':>9}{'Eff%':>8}")
        print(header)
        print("-" * len(header))
        for r in results:
            print(f"{r['kind']:<7}{r['deps']:>5}{r['critical']:>6}{r['n']:>5}"
                  f"{r['ideal']:>7}{r['hazard']:>8}{r['renamed']:>8}"
                  f"{r['speedup']:>8.2f}x{r['efficiency']:>8.2f}")

        print("\nKesimpulan singkat:")
        print("- RAW (true dependence): tidak berubah setelah renaming.")
        print("- WAR/WAW (name dependence): turun ke cycle ideal setelah renaming.")

    if any(s[1] == "GAGAL" for s in status):
        sys.exit(1)


if __name__ == "__main__":
    main()
