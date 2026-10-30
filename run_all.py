"""
run_all.py
Menjalankan skrip tiap anggota (di folder anggota1/2/3), mencatat status
(OK/GAGAL) dan waktu, lalu menampilkan tabel ringkasan RAW vs WAR vs WAW.
"""

import importlib
import os
import sys
import time
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))

# Daftarkan folder utama dan folder tiap anggota agar modul bisa di-import
for folder in ("", "anggota1", "anggota2", "anggota3"):
    path = os.path.join(ROOT, folder)
    if path not in sys.path:
        sys.path.insert(0, path)

SCRIPTS = ["anggota1_raw", "anggota2_war", "anggota3_waw"]


def main():
    results, status = [], []

    for name in SCRIPTS:
        start = time.perf_counter()
        try:
            module = importlib.import_module(name)
            results.append(module.main())
            status.append((name, "OK", time.perf_counter() - start))
        except Exception:
            traceback.print_exc()
            status.append((name, "GAGAL", time.perf_counter() - start))

    print("\n\n" + "#" * 78)
    print("STATUS SKRIP")
    print("#" * 78)
    for name, st, sec in status:
        print(f"  {name + '.py':<20} {st:<6} ({sec:.2f} detik)")

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
