import pandas as pd
from modules.data_store import baca_data, simpan_data

# ===============================
# MENU ADMIN
# ===============================
def menu_admin(user_sedang_login):
    while True:
        print("\n=== KELOLA PENGGUNA (USER) ===")
        print("1. Lihat Daftar User")
        print("2. Tambah User")
        print("3. Edit User")
        print("4. Hapus User")
        print("0. Kembali")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            lihat_user()
        elif pilihan == "2":
            tambah_user_baru()
        elif pilihan == "3":
            edit_user()
        elif pilihan == "4":
            hapus_user()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid!")

# ===============================
# READ
# ===============================
def lihat_user():
    tabel = baca_data("users")
    if tabel.empty:
        print("Data user masih kosong.")
    else:
        print(tabel.to_string(index=False))

# ===============================
# CREATE
# ===============================
def tambah_user_baru():
    print("\n--- TAMBAH USER ---")
    username = input("Username baru: ")
    password = input("Password: ")

    # Role pakai penomoran (list)
    daftar_role = [
        "kepala_divisi",
        "auditor",
        "direktur"
    ]

    print("\nPilih Role:")
    for i, role in enumerate(daftar_role, start=1):
        print(f"{i}. {role}")

    pilihan_role = int(input("Pilihan: "))
    role = daftar_role[pilihan_role - 1]

    divisi = input("Divisi: ")

    tabel_users = baca_data("users")

    # Generate ID otomatis
    if tabel_users.empty:
        id_baru = 1
    else:
        id_baru = tabel_users["id"].max() + 1

    data_user_baru = {
        "id": id_baru,
        "username": username,
        "password": password,
        "role": role,
        "divisi": divisi
    }

    tabel_baru = pd.DataFrame([data_user_baru])
    tabel_gabungan = pd.concat([tabel_users, tabel_baru], ignore_index=True)

    simpan_data("users", tabel_gabungan)
    print("User berhasil ditambahkan!")

# ===============================
# UPDATE
# ===============================
def edit_user():
    tabel = baca_data("users")
    if tabel.empty:
        print("Data kosong.")
        return

    print(tabel.to_string(index=False))
    id_edit = int(input("\nMasukkan ID user yang ingin diedit: "))

    if id_edit not in tabel["id"].values:
        print("ID tidak ditemukan!")
        return

    index = tabel[tabel["id"] == id_edit].index[0]

    username = input("Username baru: ")
    password = input("Password baru: ")

    daftar_role = ["kepala_divisi", "auditor", "direktur"]
    print("\nPilih Role:")
    for i, role in enumerate(daftar_role, start=1):
        print(f"{i}. {role}")
    pilihan_role = int(input("Pilihan: "))
    role = daftar_role[pilihan_role - 1]

    divisi = input("Divisi baru: ")

    tabel.at[index, "username"] = username
    tabel.at[index, "password"] = password
    tabel.at[index, "role"] = role
    tabel.at[index, "divisi"] = divisi

    simpan_data("users", tabel)
    print("Data user berhasil diupdate!")

# ===============================
# DELETE
# ===============================
def hapus_user():
    tabel = baca_data("users")
    if tabel.empty:
        print("Data kosong.")
        return

    print(tabel.to_string(index=False))
    id_hapus = int(input("\nMasukkan ID user yang ingin dihapus: "))

    if id_hapus not in tabel["id"].values:
        print("ID tidak ditemukan!")
        return

    tabel = tabel[tabel["id"] != id_hapus]
    simpan_data("users", tabel)

    print("User berhasil dihapus!")