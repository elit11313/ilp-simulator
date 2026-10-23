"""run_all.py - menjalankan ke-12 program (3 anggota x 4 program)."""
import os
import subprocess
import sys

base = os.path.dirname(os.path.abspath(__file__))
berhasil, lewat, gagal = [], [], []

for k in (1, 2, 3):
    for prog in ("raw", "war", "waw", "semua"):
        nama = f"anggota{k}/{prog}.py"
        path = os.path.join(base, f"anggota{k}", f"{prog}.py")
        print(f"\n######## {nama} ########")
        if not os.path.isfile(path):
            print(f"[LEWAT] File tidak ditemukan: {nama}")
            lewat.append(nama)
            continue
        hasil = subprocess.run([sys.executable, path], cwd=base)
        if hasil.returncode == 0:
            berhasil.append(nama)
        else:
            print(f"[GAGAL] {nama} error, lihat pesan di atas")
            gagal.append(nama)

print("\n" + "=" * 56)
print("RINGKASAN")
print("=" * 56)
print(f"Berhasil : {len(berhasil)} dari 12")
print(f"Tidak ada: {lewat if lewat else '-'}")
print(f"Error    : {gagal if gagal else '-'}")
