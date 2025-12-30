import os
from modules.data_store import baca_data,clear_screen #import datanya dari data store sebagai baca data/irfan
from tabulate import tabulate #pastikan sudah pip install tabulate /kei
import pandas as pd #pastikan sudah pip install pandas /kei


def tampilkan_interaktif(df, judul="DATA"):
    # fungsi untuk menampilkan data dengan fitur /kei
    # SORTING dan SEARCHING bawaan /kei
    df_tampil = df.copy() # copy biar data asli gak rusak /kei
    
    while True:
        clear_screen()
        print(f"\n=== {judul} ===")
        
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
            print("\nKolom tersedia:", ", ".join(cols))
            kolom = input("Urutkan berdasarkan kolom apa? : ")
            
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

# ==========================================
# LOGIKA UTAMA LAPORAN
# ==========================================
def siapkan_data_laporan():
    """Load data dan convert tanggal biar bisa diolah per bulan/tahun"""
    df = baca_data("pengajuan")
    if not df.empty:
        # ubah kolom 'tanggal' dari string jadi datetime /kei
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        
        # Bikin kolom bantuan tahun dan bulan
        df['tahun'] = df['tanggal'].dt.year
        df['bulan'] = df['tanggal'].dt.strftime('%B') # nama bulan (january, dll) /kei
        df['bulan_angka'] = df['tanggal'].dt.month # urutanm bulan (1-12) /kei
    return df

def menu_laporan(user_sedang_login):
    while True:
        df = siapkan_data_laporan()
        
        clear_screen()
        print(f"\n=== DASHBOARD DIREKTUR/AUDITOR ===")
        print(f"User: {user_sedang_login['username']} | Role: {user_sedang_login['role']}")
        print("-" * 40)
        print("1. Laporan Detail (Semua Data)")
        print("2. Rekapitulasi Per DIVISI")
        print("3. Rekapitulasi Per BULAN")
        print("4. Rekapitulasi Per TAHUN")
        print("0. Kembali")
        
        pilihan = input("Pilih Menu: ")
        
        if df.empty and pilihan != "0":
            print("Belum ada data pengajuan sama sekali.")
            input("Enter...")
            continue

        if pilihan == "1":
            # tampilkan semua data mentah tapi interaktif /kei
            # mengapus kolom bantuan biar kgk penuh /kei 
            view_df = df.drop(columns=['tahun', 'bulan', 'bulan_angka'], errors='ignore')
            tampilkan_interaktif(view_df, judul="SEMUA DATA PENGAJUAN")
            
        elif pilihan == "2":
            # Group by divisi /kei
            rekap = df.groupby(['divisi'])['nominal'].sum().reset_index()
            tampilkan_interaktif(rekap, judul="TOTAL PENGELUARAN PER DIVISI")
            
        elif pilihan == "3":
            # Group by tahun dan Bulan (biar Jan 2024 beda sama Jan 2025) /kei
            rekap = df.groupby(['tahun', 'bulan_angka', 'bulan'])['nominal'].sum().reset_index()
            # Sort dulu berdasarkan tahun dan bulan angka biar urut /kei
            rekap = rekap.sort_values(by=['tahun', 'bulan_angka'])
            
            # tampilkan kolom yg perlu aja /kei
            view_rekap = rekap[['tahun', 'bulan', 'nominal']]
            tampilkan_interaktif(view_rekap, judul="TOTAL PENGELUARAN PER BULAN")
            
        elif pilihan == "4":
            # Group by tahun /kei
            rekap = df.groupby(['tahun'])['nominal'].sum().reset_index()
            tampilkan_interaktif(rekap, judul="TOTAL PENGELUARAN TAHUNAN")
            
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")