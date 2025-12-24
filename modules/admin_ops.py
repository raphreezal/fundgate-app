import pandas as pd
from modules.data_store import baca_data, simpan_data

def menu_admin(user_sedang_login):
    while True:
        print("\n=== KELOLA PENGGUNA (USER) ===")
        print("1. Lihat Daftar User")
        print("2. Tambah User Baru")
        print("0. Kembali")
        
        pilihan = input("Pilih: ")
        if pilihan == "1":
            tabel = baca_data("users")
            print(tabel.to_string(index=False))
        elif pilihan == "2":
            tambah_user_baru()
        elif pilihan == "0":
            break

def tambah_user_baru():
    print("\n--- TAMBAH USER ---")
    username = input("Username baru: ")
    password = input("Password: ")
    role = input("Role (kepala_divisi / direktur / auditor): ")
    divisi = input("Nama Divisi (contoh: IT, HRD, Marketing): ")

    data_user_baru = {
        "username": username,
        "password": password,
        "role": role,
        "divisi": divisi
    }
    
    tabel_users = baca_data("users")
    tabel_baru = pd.DataFrame([data_user_baru])
    tabel_gabungan = pd.concat([tabel_users, tabel_baru], ignore_index=True)
    
    simpan_data("users", tabel_gabungan)
    print(f"User {username} berhasil ditambahkan!")