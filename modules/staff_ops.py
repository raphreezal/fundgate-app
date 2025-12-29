import pandas as pd
from datetime import datetime
from modules.data_store import baca_data, simpan_data

def menu_kepala_divisi(user_sedang_login):
    while True:
        print(f"\n=== MENU KEPALA DIVISI: {user_sedang_login['divisi']} ===")
        print("1. Buat Pengajuan Dana Baru")
        print("2. Lihat Riwayat Pengajuan Saya")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu (0-2): ")
        
        if pilihan == "1":
            form_tambah_pengajuan(user_sedang_login)
        elif pilihan == "2":
            lihat_status_saya(user_sedang_login)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak ada.")

            # MERUBAH FORM PENGAJUAN
            # nanti bakal aku tambahin codingan disini

def form_tambah_pengajuan(user):
    print("\n--- FORM PENGAJUAN DANA ---")
    kategori_input = input("Untuk keperluan apa? : ")
    nominal_input = input("Berapa butuhnya (Rp)? : ")
    
    # id untuk jam./mars
    id_unik = "REQ-" + datetime.now().strftime("%H%M%S")
    tanggal_sekarang = datetime.now().strftime("%Y-%m-%d")

    # data baru bentuk Dictionary /mars
    data_baru = {
        "id": id_unik,
        "tanggal": tanggal_sekarang,
        "pemohon": user['username'],
        "divisi": user['divisi'],
        "kategori": kategori_input,
        "nominal": int(nominal_input), 
        "status": "Menunggu"
    }

    # load data lama
    tabel_lama = baca_data("pengajuan")
    
    # ubah dictionary data_baru menjadi DataFrame (tabel kecil 1 baris)
    tabel_baru = pd.DataFrame([data_baru])
    
    # gabungkan tabel lama dengan tabel baru
    tabel_gabungan = pd.concat([tabel_lama, tabel_baru], ignore_index=True)
    
    # dimpan ke file
    simpan_data("pengajuan", tabel_gabungan)
    print(f"Sukses! Pengajuan dengan ID {id_unik} berhasil disimpan.")

def lihat_status_saya(user):
    print("\n--- RIWAYAT SAYA ---")
    tabel_pengajuan = baca_data("pengajuan")
    
    # filter: Ambil cuma yang kolom 'pemohon' sama dengan nama user
    data_milik_saya = tabel_pengajuan[tabel_pengajuan['pemohon'] == user['username']]
    
    if data_milik_saya.empty:
        print("Belum ada riwayat pengajuan.")
    else:
        # Tampilkan kolom yang penting aja biar gak kepanjangan /mars
        print(data_milik_saya[['id', 'tanggal', 'nominal', 'status']].to_string(index=False))