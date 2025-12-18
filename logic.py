# --- ANGGARAN (MANAGER KEUANGAN)
def set_anggaran(tahun, total):
    data = [{"tahun": tahun, "total_anggaran": total}]
    tulis_csv("anggaran.csv", data[0].keys(), data)
    print("Anggaran berhasil disimpan")
