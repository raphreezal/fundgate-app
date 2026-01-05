import re
import pandas as pd
import os
from tabulate import tabulate # pastikan pip install tabulate /kei

# tentuin nama folder tempat menyimpan file
FOLDER_DATA = "data/"

# ===============================
# STRUKTUR KOLOM
# ===============================
KOLOM_USER = ["id", "username", "password", "role", "divisi"]
KOLOM_PENGAJUAN = ["id", "tanggal", "pemohon", "divisi", "kategori", "nominal", "status"]
KOLOM_ANGGARAN = ["kategori", "total_anggaran"]
KOLOM_KEUANGAN = ["saldo", "limit_pengajuan"]
KOLOM_RINCIAN_PENGAJUAN = ["id_rincian","id_pengajuan", "tipe", "nama_item", "jumlah", "harga_satuan", "subtotal"]

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
    # CEK rincian_pengajuan.csv
    # ===============================
    path_rincian = FOLDER_DATA + "rincian_pengajuan.csv"
    if os.path.exists(path_rincian) == False:
        df_rincian = pd.DataFrame(columns=KOLOM_RINCIAN_PENGAJUAN)
        df_rincian.to_csv(path_rincian, index=False)

    # # ===============================
    # # CEK anggaran.csv
    # # ===============================
    # path_anggaran = FOLDER_DATA + "anggaran.csv"
    # if os.path.exists(path_anggaran) == False:
    #     df_anggaran = pd.DataFrame(columns=KOLOM_ANGGARAN)
    #     df_anggaran.to_csv(path_anggaran, index=False)
    
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

def tampilkan_interaktif(df):
    # fungsi untuk menampilkan data dengan fitur /kei
    # SORTING dan SEARCHING bawaan /kei
    df_tampil = df.copy() # copy biar data asli gak rusak /kei
    
    while True:
        # cek kalau data kosong /kei
        if df_tampil.empty:
            print("Tidak ada data yang ditemukan.")
        else:
            # tampilkan tabel rapi /kei
            print(tabulate(df_tampil, headers='keys', tablefmt='psql', showindex=False))
        
        print("\n[MENU INTERAKTIF]")
        print("1. Sort (Urutkan Data)")
        print("2. Search (Cari Data)")
        print("3. Reset (Kembalikan Awal)")
        print("0. Kembali")
        
        aksi = input("Pilih aksi: ")
        
        if aksi == "1":
            # --- FITUR SORTING --- /kei
            cols = list(df_tampil.columns)
            print("\nKolom tersedia:")
            for i, c in enumerate(cols):
                print(f"{i}. {c}")
                
            i_kolom = input("Urutkan berdasarkan kolom apa? : ")
            
            if i_kolom.isdigit() and 0 <= int(i_kolom) < len(cols):
                kolom = cols[int(i_kolom)]
            else:
                input("Nomor kolom salah! Enter untuk lanjut...")
                continue

            if kolom in cols:
                urutan = input("Ascending (a) atau Descending (d)? : ").lower()
                is_asc = True if urutan == 'a' else False
                
                # Proses sorting
                df_tampil = df_tampil.sort_values(by=kolom, ascending=is_asc)
            else:
                input("Nama kolom salah! Enter untuk lanjut...")

        elif aksi == "2":
            # FITUR SEARCHING /kei
            kata_kunci = input("Cari kata apa? : ").lower()
            
            # 1. siapkan wadah kosong (anggap semua baris belum ketemu / False) /kei
            baris_yang_cocok = pd.Series(False, index=df_tampil.index)

            # 2. xek satu per satu kolom /kei
            for nama_kolom in df_tampil.columns:
                # ambil isi kolom, jadikan teks, dan huruf kecilkan /kei
                isi_kolom = df_tampil[nama_kolom].astype(str).str.lower()
                
                # cek apakah kata kunci ada di dalam kolom ini? /kei
                ada_gak = isi_kolom.str.contains(kata_kunci)
                
                # 3. gabungkan hasil pencarian /kei
                # kalo ketemu di kolom ini atau (|) kolom sebelumnya, tandai sebagai true /kei
                baris_yang_cocok = baris_yang_cocok | ada_gak

            # 4. ambil cuma baris yang cocok tadi /kei
            df_tampil = df_tampil[baris_yang_cocok]
            
            print(f"Ketemu {len(df_tampil)} data.")
            input("Tekan Enter untuk melihat hasil...")

        elif aksi == "3":
            # reset ke data awal /kei
            df_tampil = df.copy()
            print("Data di-reset.")

        elif aksi == "0":
            break
        else:
            print("Pilihan tidak valid.")

def tabel_rapih(df, judul="DATA"):
    df_tampil = df.copy()
    # mengembalikan string tabel yang rapi dari DataFrame /kei
    print(tabulate(df_tampil, headers='keys', tablefmt='psql', showindex=False))

def format_rupiah(angka):
    return f"Rp {int(angka):,}".replace(",", ".")
    
def header():
    print("═════════════════════════════════════════════")
    print("|              F U N D G A T E              |")
    print("|    Sistem Pengajuan & Manajemen Keuangan  |")
    print("═════════════════════════════════════════════\n")
  
# Validasi username dan password / najwa
def validasi_username(username):
    if not username:
        return False, "Username tidak boleh kosong!"
    if len(username) > 20:
        return False, "Username maksimal 20 karakter!"
    if not re.fullmatch(r"[A-Za-z ]+", username):
        return False, "Username hanya boleh terdiri dari huruf saja!"
    return True, "Valid"

def validasi_password(password):
    if not password:
        return False, "Password tidak boleh kosong!"
    if " " in password:
        return False, "Password tidak boleh mengandung spasi!"
    if len(password) < 8:
        return False, "Password minimal 8 karakter!"
    if not re.search(r"[A-Z]", password):
        return False, "Harus ada huruf kapital!"
    if not re.search(r"[a-z]", password):
        return False, "Harus ada huruf kecil!"
    if not re.search(r"[0-9]", password):
        return False, "Harus ada angka!"
    if not re.search(r"[!@#$%^&*()\-_=+{}[\]|:;\"'<>,.?/]", password):
        return False, "Harus ada simbol!"
    return True, "Password valid & dapat digunakan"

# buat id user secara otomatis / najwa
def generate_id_user(df):
    if df.empty:
        return "USR001"
    last_id = df.iloc[-1]["id"]
    nomor = int(last_id[3:])
    return f"USR{nomor+1:03}"

