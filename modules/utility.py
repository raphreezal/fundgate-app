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

def tampilkan_interaktif(df, judul="DATA", show_judul=False):
    # fungsi untuk menampilkan data dengan fitur /kei
    # SORTING dan SEARCHING bawaan /kei
    df_tampil = df.copy() # copy biar data asli gak rusak /kei
    
    pesan_error = "" #variabel untuk menampung pesan eror sementara /kei

    while True:
        clear_screen() #biar layar selalu bersih /kei
        header() #tampilkan header /kei
        if show_judul:
            print(f"────────────────────────── {judul} ───────────────────────────\n")
        # cek kalau data kosong /kei
        if df_tampil.empty:
            print("\n⚠️  Tidak ada data yang ditemukan (Hasil Filter/Search Kosong).")
            print("💡  Saran: Gunakan fitur [3] Reset untuk kembali.")
        else:
            # tampilkan tabel rapi /kei
            print(tabulate(df_tampil, headers='keys', tablefmt='psql', showindex=False))
        
        # tampilin pesan error jika ada, terus kosongiin lagi /kei
        if pesan_error:
            print(f"\n{pesan_error}")
            pesan_error = ""

        print("\n[MENU INTERAKTIF]")
        print("[1] Sort (Urutkan Data)")
        print("[2] Search (Cari Data)")
        print("[3] Reset (Kembalikan Awal)")
        print("[0] Kembali")
        
        aksi = input("Pilih aksi: ")

        if aksi == "":
            pesan_error = "⚠️  Pilihan tidak boleh kosong!"
            continue
        
        if aksi == "1":
            # --- FITUR SORTING --- /kei
            if df_tampil.empty:
                pesan_error = "⚠️  Data kosong, tidak bisa diurutkan"
                continue

            cols = list(df_tampil.columns)
            print("\n[Kolom tersedia]")
            for i, c in enumerate(cols):
                print(f"[{i + 1}] {c}") # penomoran user friendly (mulai dari 1) /kei

            i_kolom = input("Urutkan berdasarkan nomor kolom: ").strip()
            
            # fix bug: validasi harus pakai AND dan cek range yang benar (1 sampai len) /kei
            if i_kolom.isdigit() and 1 <= int(i_kolom) <= len(cols):
                index_pilih = int(i_kolom) - 1
                kolom = cols[index_pilih]
                
                # konfirmasi user (opsional, tapi bagus untuk safety ig?) /keidjaur axior
                print(f"Target sort: {kolom}")
                
                urutan = input("Ascending (a) atau Descending (d)? [Default: a]: ").strip().lower()
                is_ascending = True if urutan != 'd' else False # default ke A jika input aneh/kosong /kei
                
                df_tampil = df_tampil.sort_values(by=kolom, ascending=is_ascending)
                pesan_error = f"✅ Sukses mengurutkan berdasarkan '{kolom}'"
            
            else:
                pesan_error = "⚠️  Nomor kolom tidak valid!"
                continue

        elif aksi == "2":
            # FITUR SEARCHING /kei
            kata_kunci = input("Cari kata apa? : ").strip().lower() # tambah strip() biar spasi gak ganggu /kei
            
            if kata_kunci == "":
                pesan_error = "⚠️  Kata kunci tidak boleh kosong!"
                continue
            
            # 1. siapkan wadah kosong (anggap semua baris belum ketemu / False) /kei
            baris_yang_cocok = pd.Series(False, index=df_tampil.index)

            # 2. xek satu per satu kolom /kei
            for nama_kolom in df_tampil.columns:
                # ambil isi kolom, jadikan teks, dan huruf kecilkan /kei
                isi_kolom = df_tampil[nama_kolom].astype(str).str.lower()
                ada_gak = isi_kolom.str.contains(kata_kunci, na=False) # na=False biar aman kalau ada data yg NULL /kei
                baris_yang_cocok = baris_yang_cocok | ada_gak

            hasil_cari = df_tampil[baris_yang_cocok]
            
            # [UX] kasih feedback langsung berapa data ketemu /kei
            if len(hasil_cari) > 0:
                df_tampil = hasil_cari
                pesan_error = f"✅ Ditemukan {len(df_tampil)} data dengan kata kunci '{kata_kunci}'."
            else:
                pesan_error = f"⚠️  Kata kunci '{kata_kunci}' tidak ditemukan di kolom manapun."
                # jangn update df_tampil kalo kgk ketemu, atau update jdi kosong
                # Di sini gw biarin df_tampil tetap seperti sebelumnya biar user kgk kaget tabel nya ilang
                # tapi kalau mw strict (tabel jadi kosong), baris di bawah ini di uncomment aja:
                
                # df_tampil = hasil_cari 

        elif aksi == "3":
            # reset ke data awal /kei
            df_tampil = df.copy()
            pesan_error = "🔄 Data berhasil direset ke kondisi awal."

        elif aksi == "0":
            break
        
        else:
             pesan_error = "⚠️  Pilihan menu tidak valid!"

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

