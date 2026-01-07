import os
from modules.utility import baca_data,clear_screen, format_rupiah, tampilkan_interaktif, header
import pandas as pd #pastikan sudah pip install pandas /kei

# funsi konfirmasi inputan / najwa
def konfirmasi_yn(pesan):
    while True:
        jawab = input(pesan).strip().lower()
        if jawab in ("y", "n"):
            return jawab
        print("⚠️   Input tidak valid! Harus y atau n.")
        input("Tekan Enter untuk input ulang...\n")
        
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
        header()
        print("───────────── DASHBOARD LAPORAN ─────────────")
        print(f"Selamat datang, {user_sedang_login['username']}! Anda masuk sebagai {user_sedang_login['role']}.")
        print("─────────────────────────────────────────────")
        print("[1] Laporan Detail (Semua Data)")
        print("[2] Rekapitulasi Per DIVISI")
        print("[3] Rekapitulasi Per BULAN")
        print("[4] Rekapitulasi Per TAHUN")
        print("[0] Logout")
        
        pilihan = input("Pilih Menu: ").strip()
        
        if pilihan == "":
            input("\n⚠️    Pilihan tidak boleh kosong!\nTekan Enter untuk input ulang...")
            continue

        if not pilihan.isdigit():
            input("\n⚠️    Pilihan harus berupa angka!\nTekan Enter untuk input ulang...")
            continue

        if pilihan not in ["0", "1", "2", "3", "4"]:
            input("\n⚠️    Pilihan tidak valid!\nTekan Enter untuk input ulang...")
            continue

        if df.empty and pilihan != "0":
            input("\n⚠️    Belum ada data pengajuan sama sekali!\nTekan Enter untuk kembali...")
            continue

        if pilihan == "1":
            clear_screen()
            print("══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
            print("|                                                                 F U N D G A T E                                                                    |")
            print("|                                                      Sistem Pengajuan & Manajemen Keuangan                                                         |")
            print("|────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────|")
            print("|                                                                DASHBOARD LAPORAN                                                                   |")
            print(f"|                                                      User: {user_sedang_login['username']} | Role: {user_sedang_login['role']}                                                          |")
            print("══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n")
            # tampilkan semua data mentah tapi interaktif /kei
            # mengapus kolom bantuan biar kgk penuh /kei
            print("────────────────────────────────────────────────────────────── SEMUA DATA PENGAJUAN ──────────────────────────────────────────────────────────────────")
            view_df = df.drop(columns=['tahun', 'bulan', 'bulan_angka'], errors='ignore')
            view_df['total'] = view_df['total'].map(format_rupiah)
            tampilkan_interaktif(view_df[["id_pengajuan","tanggal","jenis_pengajuan","nama_kepala_divisi","divisi","total", "status", "catatan_manajer"]])
            
        elif pilihan == "2":
            clear_screen()
            print("══════════════════════════════════════════")
            print("|            F U N D G A T E             |")
            print("|  Sistem Pengajuan & Manajemen Keuangan |")
            print("|────────────────────────────────────────|")
            print("|           DASHBOARD LAPORAN            |")
            print(f"|   User: {user_sedang_login['username']} | Role: {user_sedang_login['role']} |")
            print("══════════════════════════════════════════\n")
            # Group by divisi /kei
            print("────── TOTAL PENGELUARAN PER DIVISI ──────")
            rekap = df.groupby(['divisi'])['total'].sum().reset_index()
            rekap['total'] = rekap['total'].map(format_rupiah)
            tampilkan_interaktif(rekap)
            
        elif pilihan == "3":
            clear_screen()
            print("══════════════════════════════════════════")
            print("|            F U N D G A T E             |")
            print("|  Sistem Pengajuan & Manajemen Keuangan |")
            print("|────────────────────────────────────────|")
            print("|           DASHBOARD LAPORAN            |")
            print(f"|   User: {user_sedang_login['username']} | Role: {user_sedang_login['role']} |")
            print("══════════════════════════════════════════\n")
            print("────── TOTAL PENGELUARAN PER BULAN ──────")
            # Group by tahun dan Bulan (biar Jan 2024 beda sama Jan 2025) /kei
            rekap = df.groupby(['tahun', 'bulan_angka', 'bulan'])['total'].sum().reset_index()
            # Sort dulu berdasarkan tahun dan bulan angka biar urut /kei
            rekap = rekap.sort_values(by=['tahun', 'bulan_angka'])
            
            # tampilkan kolom yg perlu aja /kei
            view_rekap = rekap[['tahun', 'bulan', 'total']].copy()
            # Mengubah penulisan nominal format Indonesia (ada titik)  /farah
            #perbaiikan format rupiah /kei
            view_rekap['total'] = view_rekap['total'].apply(format_rupiah)
            tampilkan_interaktif(view_rekap)

        elif pilihan == "4":
            clear_screen()
            print("══════════════════════════════════════════")
            print("|            F U N D G A T E             |")
            print("|  Sistem Pengajuan & Manajemen Keuangan |")
            print("|────────────────────────────────────────|")
            print("|           DASHBOARD LAPORAN            |")
            print(f"|   User: {user_sedang_login['username']} | Role: {user_sedang_login['role']} |")
            print("══════════════════════════════════════════\n")
            print("─────── TOTAL PENGELUARAN TAHUNAN ────────")
            # Group by tahun /kei
            rekap = df.groupby(['tahun'])['total'].sum().reset_index()
            # Mengubah nominal scientific jadi yang bisa dibaca  /farah
            # perbaikan format rupiah /kei
            rekap['total'] = rekap['total'].map(format_rupiah)
            tampilkan_interaktif(rekap)
            
        elif pilihan == "0":
            jawab = konfirmasi_yn("\nApakah yakin ingin logout? (y/n): ")
            if jawab == "n":
                continue 
            else:
                print("\n✅  Berhasil logout.")
                break 
                        
        else:
            print("\n⚠️      Pilihan tidak valid!")
            input("Tekan Enter untuk input ulang...\n")