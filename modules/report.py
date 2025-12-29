import os
from modules.data_store import baca_data #import datanya dari data store sebagai baca data/irfan
from tabulate import tabulate #pastikan sudah pip install tabulate /kei
import pandas as pd #pastikan sudah pip install pandas /kei

def menu_laporan(user_sedang_login):
    while True:
        print(f"\n=== LAPORAN (Mode: {user_sedang_login['role']}) ===")
        print("1. Lihat Rekapitulasi Divisi")
        print("2. Lihat Semua Data Pengajuan")
        print("3. Export Laporan ke Excel")
        print("0. Kembali")
        
        pilihan = input("Pilih menu: ")
        
        tabel_pengajuan = baca_data("pengajuan")
        if tabel_pengajuan.empty:
            print("Data masih kosong.")
            continue

        if pilihan == "1":
            print("\n=== REKAPITULASI DANA PER DIVISI ===")
            laporan_divisi = tabel_pengajuan.groupby(['divisi'])['nominal'].sum().reset_index()
            # Gunakan tabulate format 'grid' biar ada garis kotaknya
            print(tabulate(laporan_divisi, headers='keys', tablefmt='grid', showindex=False))
            
        elif pilihan == "2":
            print("\n--- DETAIL SEMUA DATA ---")
            print(tabulate(tabel_pengajuan, headers='keys', tablefmt='psql', showindex=False))
            
        elif pilihan == "3":
            folder = "laporan/"
            # buat folder dulu kalo belum ada /kei
            if not os.path.exists(folder):
                os.makedirs(folder)
            nama_file = "laporan_keuangan.xlsx"
            # menggunakan to_excel (perlu library openpyxl) /kei
            tabel_pengajuan.to_excel(folder + nama_file, index=False)
            print(f"Berhasil! Laporan disimpan sebagai '{nama_file}' di folder '{folder}'.")
            
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")