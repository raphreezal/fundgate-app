import os
from modules.data_store import baca_data,clear_screen, tampilkan_interaktif #import datanya dari data store sebagai baca data/irfan
import pandas as pd #pastikan sudah pip install pandas /kei



# ==========================================
# LOGIKA UTAMA LAPORAN
# ==========================================
def siapkan_data_laporan():
    """Load data dan convert tanggal biar bisa diolah per bulan/tahun"""
    df = baca_data("pengajuan")
    if not df.empty:
        # ubah kolom 'tanggal' dari string jadi datetime /kei
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        
        # bikin kolom bantuan tahun dan bulan /kei
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
            tampilkan_interaktif(view_df[["id_pengajuan","tanggal","jenis_pengajuan","nama_kepala_divisi","divisi","total", "status", "catatan_manajer"]], judul="SEMUA DATA PENGAJUAN")
            
        elif pilihan == "2":
            # Group by divisi /kei
            rekap = df.groupby(['divisi'])['total'].sum().reset_index()
            tampilkan_interaktif(rekap, judul="TOTAL PENGELUARAN PER DIVISI")
            
        elif pilihan == "3":
            # Group by tahun dan Bulan (biar Jan 2024 beda sama Jan 2025) /kei
            rekap = df.groupby(['tahun', 'bulan_angka', 'bulan'])['total'].sum().reset_index()
            # Mengubah penulisan nominal format Indonesia (ada titik)  /farah
            rekap['total'] = rekap['total'].map(lambda x: f"{int(x):,}".replace(",", "."))
            # Sort dulu berdasarkan tahun dan bulan angka biar urut /kei
            rekap = rekap.sort_values(by=['tahun', 'bulan_angka'])
            
            # tampilkan kolom yg perlu aja /kei
            view_rekap = rekap[['tahun', 'bulan', 'total']]
            # Mengubah penulisan nominal format Indonesia (ada titik)  /farah
            view_rekap['total'] = view_rekap['total'].map(lambda x: f"{int(x):,}".replace(",", "."))
            tampilkan_interaktif(view_rekap, judul="TOTAL PENGELUARAN PER BULAN")
            
        elif pilihan == "4":
            # Group by tahun /kei
            rekap = df.groupby(['tahun'])['total'].sum().reset_index()
            # Mengubah nominal scientific jadi yang bisa dibaca  /farah
            rekap['total'] = rekap['total'].map(lambda x: f"{int(x):,}".replace(",", "."))
            tampilkan_interaktif(rekap, judul="TOTAL PENGELUARAN TAHUNAN")
            
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")