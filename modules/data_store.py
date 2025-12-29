import pandas as pd
import os

# tentuin nama folder tempat menyimpan file
FOLDER_DATA = "data/"

# ===============================
# STRUKTUR KOLOM
# ===============================
KOLOM_USER = ["id", "username", "password", "role", "divisi"]
KOLOM_PENGAJUAN = ["id", "tanggal", "pemohon", "divisi", "kategori", "nominal", "status"]
KOLOM_ANGGARAN = ["kategori", "total_anggaran"]
KOLOM_KEUANGAN = ["saldo", "limit_pengajuan"]

def siapkan_folder_dan_file():
    """
    Fungsi ini dijalankan pertama kali untuk memastikan 
    folder 'data/' dan file-file csv sudah tersedia.
    """

    # ===============================
    # CEK FOLDER
    # ===============================
    if os.path.exists(FOLDER_DATA) == False:
        os.makedirs(FOLDER_DATA)
        print("[INFO] Folder 'data/' berhasil dibuat.")

    # ===============================
    # CEK users.csv
    # ===============================
    path_user = FOLDER_DATA + "users.csv"
    if os.path.exists(path_user) == False:
        # tabel kosong dengan kolom lengkap
        df_user = pd.DataFrame(columns=KOLOM_USER)

        # admin default
        admin_baru = {
            "id": 1,
            "username": "admin",
            "password": "123",
            "role": "manajer_keuangan",
            "divisi": "Finance"
        }

        df_user = pd.DataFrame([admin_baru])
        df_user.to_csv(path_user, index=False)
        print("[INFO] File users.csv dibuat (admin/123)")

    # ===============================
    # CEK pengajuan.csv
    # ===============================
    path_pengajuan = FOLDER_DATA + "pengajuan.csv"
    if os.path.exists(path_pengajuan) == False:
        df_pengajuan = pd.DataFrame(columns=KOLOM_PENGAJUAN)
        df_pengajuan.to_csv(path_pengajuan, index=False)

    # ===============================
    # CEK anggaran.csv
    # ===============================
    path_anggaran = FOLDER_DATA + "anggaran.csv"
    if os.path.exists(path_anggaran) == False:
        df_anggaran = pd.DataFrame(columns=KOLOM_ANGGARAN)
        df_anggaran.to_csv(path_anggaran, index=False)
    
    # ===============================
    # CEK keuangan.csv
    # ===============================
    path_keuangan = FOLDER_DATA + "keuangan.csv"
    if os.path.exists(path_keuangan) == False:
        data_awal = [{
            "saldo": 100000000,
            "limit_pengajuan": 5000000
        }]
        df_keuangan = pd.DataFrame(data_awal)
        df_keuangan.to_csv(path_keuangan, index=False)



# ===============================
# OPERASI FILE
# ===============================
def baca_data(nama_file):
    """Membaca file CSV dan menjadikannya tabel Pandas"""
    lokasi_lengkap = FOLDER_DATA + nama_file + ".csv"
    return pd.read_csv(lokasi_lengkap)

def simpan_data(nama_file, data_frame_baru):
    """Menyimpan tabel Pandas kembali ke file CSV"""
    lokasi_lengkap = FOLDER_DATA + nama_file + ".csv"
    data_frame_baru.to_csv(lokasi_lengkap, index=False)

# ==========================================
# FUNGSI BANTUAN (UTILITY)
# ==========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')