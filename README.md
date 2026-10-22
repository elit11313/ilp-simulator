# ILP Simulator - RAW, WAR, WAW (3 anggota x 4 program = 12 program)

Pengembangan dari https://github.com/harshitasingh4863/instruction-level-parallelism-simulator

| Folder | Isi |
|---|---|
| `anggota1/`, `anggota2/`, `anggota3/` | Masing-masing: `instruksi.py` (instruction set sendiri), `raw.py`, `war.py`, `waw.py`, `semua.py`, `graphs/` |
| `common.py` | Scheduler ILP + penggambar dependency graph |
| `hazards.py` | Deteksi RAW, WAR, WAW |
| `run_all.py` | Menjalankan ke-12 program |

## Menjalankan
```bash
pip install -r requirements.txt
python anggota1/raw.py        # satu program
python run_all.py             # semua 12 program
python generate_report.py --members "Nama1 (NIM)" "Nama2 (NIM)" "Nama3 (NIM)" --github https://github.com/USER/REPO
```
