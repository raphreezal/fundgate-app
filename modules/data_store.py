import pandas as pd
import os

# tentuin nama folder tempat menyimpan file
FOLDER_DATA = "data/"

# siapkan struktur kolomnya biar rapi
KOLOM_USER = ["username", "password", "role", "divisi"]
KOLOM_PENGAJUAN = ["id", "tanggal", "pemohon", "divisi", "kategori", "nominal", "status"]
KOLOM_ANGGARAN = ["kategori", "total_anggaran"]

def siapkan_folder_dan_file():
    """
    Fungsi ini dijalankan pertama kali untuk memastikan 
    folder 'data/' dan file-file csv sudah tersedia.
    """
    # 1. cek apakah folder 'data/' ada? Kalau tidak, buat dulu /kei
    if os.path.exists(FOLDER_DATA) == False:
        os.makedirs(FOLDER_DATA)
        print("[INFO] Folder 'data/' berhasil dibuat.")

    # 2. cek file users.csv /kei
    path_user = FOLDER_DATA + "users.csv"
    if os.path.exists(path_user) == False:
        # Bikin tabel kosong
        df_user = pd.DataFrame(columns=KOLOM_USER)
        # tambahkan 1 admin default biar bisa login /kei
        admin_baru = {
            "username": "admin", 
            "password": "123", 
            "role": "manajer_keuangan", 
            "divisi": "Finance"
        }
        # masukkan ke tabel (pakai list of dictionaries) dan simpan /kei
        df_user = pd.DataFrame([admin_baru]) 
        df_user.to_csv(path_user, index=False)
        print("[INFO] File users.csv dibuat (User default: admin/123)")

    # 3. cek file pengajuan.csv (Sama kayak diatas) /kei
    path_pengajuan = FOLDER_DATA + "pengajuan.csv"
    if os.path.exists(path_pengajuan) == False:
        df_pengajuan = pd.DataFrame(columns=KOLOM_PENGAJUAN)
        df_pengajuan.to_csv(path_pengajuan, index=False)

    # 4. cek file anggaran.csv /kei
    path_anggaran = FOLDER_DATA + "anggaran.csv"
    if os.path.exists(path_anggaran) == False:
        df_anggaran = pd.DataFrame(columns=KOLOM_ANGGARAN)
        df_anggaran.to_csv(path_anggaran, index=False)

# di file modules/data_store.py /kei

def baca_data(nama_file):
    """Membaca file CSV dan menjadikannya tabel Pandas"""
    lokasi_lengkap = FOLDER_DATA + nama_file + ".csv"
    
    data = pd.read_csv(lokasi_lengkap, dtype=str)
    
    return data

def simpan_data(nama_file, data_frame_baru):
    """Menyimpan tabel Pandas kembali ke file CSV"""
    lokasi_lengkap = FOLDER_DATA + nama_file + ".csv"
    data_frame_baru.to_csv(lokasi_lengkap, index=False)