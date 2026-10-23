# ILP Simulator - RAW, WAR, WAW

Simulator Instruction-Level Parallelism (ILP) untuk mendeteksi hazard RAW, WAR, dan WAW
serta menggambar dependency graph. Tugas INF-1316 Organisasi dan Arsitektur Komputer.

Pengembangan dari https://github.com/harshitasingh4863/instruction-level-parallelism-simulator

## Struktur

| Folder / File | Isi |
|---|---|
| anggota1/, anggota2/, anggota3/ | Masing-masing: instruksi.py, raw.py, war.py, waw.py, semua.py, graphs/ |
| common.py | Scheduler ILP dan penggambar dependency graph |
| hazards.py | Deteksi RAW, WAR, WAW |
| run_all.py | Menjalankan ke-12 program |
| requirements.txt | Library yang dibutuhkan |

## Menjalankan

    pip install -r requirements.txt
    python anggota1/raw.py
    python run_all.py

## Jenis hazard

- RAW (Read After Write): instruksi berikutnya membaca register yang ditulis instruksi sebelumnya.
- WAR (Write After Read): instruksi berikutnya menulis register yang dibaca instruksi sebelumnya.
- WAW (Write After Write): dua instruksi menulis register yang sama.

Pada dependency graph: panah merah solid = RAW, biru putus-putus = WAR, hijau titik-titik = WAW.
