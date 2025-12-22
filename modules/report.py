from modules.data_store import baca_data#import datanya dari data store sebagai baca data/irfan

def menu_laporan(user_sedang_login):
    from modules.data_store import baca_data

def menu_laporan(user_sedang_login):
    print(f"\n=== LAPORAN (Mode: {user_sedang_login['role']}) ===")
    
    tabel_pengajuan = baca_data("pengajuan")
    
    if tabel_pengajuan.empty:
        print("Data masih kosong.")
        return

    print("\n REKAPITULASI DATA DANA PER DIVISI ===")
    # Groupby itu seperti mengelompokkan kartu
    # Disini dikelompokan berdasarkan 'divisi', 
    # lalu jumlahkan kolom 'nominal'-nya./irfan
    laporan_divisi = tabel_pengajuan.groupby(['divisi'])['nominal'].sum().reset_index()
    
    print(laporan_divisi.to_string(index=False))
    
    print("\n--- DETAIL SEMUA DATA ---")
    print(tabel_pengajuan.to_string())
    
    input("\nTekan Enter untuk kembali ke menu sebelumnya...")

    return None