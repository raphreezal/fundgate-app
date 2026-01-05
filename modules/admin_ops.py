import pandas as pd

from modules.utility import (
    baca_data, simpan_data, clear_screen,
    tampilkan_interaktif, validasi_username,
    generate_id_user, header
)
from modules.auth import validasi_password
from modules.divisi_ops import menu_divisi

# ===============================
# MENU ADMIN
# ===============================
def menu_admin(user_sedang_login):
    while True:
        clear_screen()
        header()
        print("─────────────── KELOLA USER ─────────────────")
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

# read
def lihat_user():
    clear_screen()
    header()

    tabel = baca_data("users").copy()

    if tabel.empty:
        print("Data user masih kosong.")
        input("Enter...")
        return

    # 🔐 Sembunyikan password
    tabel["password"] = tabel["password"].apply(
        lambda x: "*" * len(str(x))
    )

    tampilkan_interaktif(tabel)  

def tambah_user_baru():
    # ===============================
    # INPUT USERNAME
    # ===============================
    clear_screen()
    header()
    print("─────────────── TAMBAH USER ─────────────────")
    tabel_users = baca_data("users")
    while True:
        username = input("Username (0 batal): ").strip()
        if username == "0":
            return

        if not username:
            print("❌ Username tidak boleh kosong\n")
            continue

        valid, msg = validasi_username(username)
        if not valid:
            print(f"❌ {msg}")
            continue

        if username in tabel_users["username"].values:
            print("❌ Username sudah digunakan!")
            input("Enter...")
            clear_screen()
            header()
            continue

        print("✅ Username tersedia dan dapat digunakan")
        input("Enter...")
        clear_screen()
        header()
        break


    # ===============================
    # INPUT PASSWORD
    # ===============================
    while True:
        password = input("Password (0 batal): ")
        if password == "0":
            return

        valid, pesan = validasi_password(password)
        if not valid:
            print(f"❌ {pesan}")
            input("Enter...")
            clear_screen()
            header()
            continue

        print("✅ Password valid dan dapat digunakan")
        input("Enter...")
        clear_screen()
        header()
        break


    while True:
        konfirmasi = input("Konfirmasi Password: ")
        if konfirmasi != password:
            print("❌ Konfirmasi tidak sesuai")
            continue
        break

    # ===============================
    # PILIH ROLE
    # ===============================
    daftar_role = ["kepala_divisi", "auditor", "direktur"]

    print("\nPilih Role:")
    for i, r in enumerate(daftar_role, start=1):
        print(f"{i}. {r}")

    pilihan_role = int(input("Pilihan: "))
    role = daftar_role[pilihan_role - 1]

    # ===============================
    # PILIH DIVISI
    # ===============================
    if role == "kepala_divisi":
        tabel_divisi = baca_data("divisi")
        print("\nPilih Divisi:")
        for i, d in enumerate(tabel_divisi["nama_divisi"], start=1):
            print(f"{i}. {d}")

        while True:
            pilih = input("Pilih nomor divisi (0 batal): ")
            if pilih == "0":
                return

            if not pilih.isdigit():
                print("Input harus angka")
                continue

            idx = int(pilih) - 1
            if idx < 0 or idx >= len(tabel_divisi):
                print("Pilihan tidak valid")
                continue

            divisi = tabel_divisi.iloc[idx]["nama_divisi"]
            break
    else:
        divisi = "-"

    # ===============================
    # SIMPAN USER
    # ===============================
    id_user = generate_id_user(tabel_users)

    user_baru = {
        "id": id_user,
        "username": username,
        "password": password,
        "role": role,
        "divisi": divisi
    }

    tabel_users = tabel_users.append(user_baru, ignore_index=True)
    simpan_data("users", tabel_users)

    print("✅ User berhasil dibuat!")
    input("Enter....")

# ===============================
# UPDATE
# ===============================
def edit_user():
    tabel = baca_data("users")
    if tabel.empty:
        print("Data kosong.")
        return

    tampilkan_interaktif(tabel, judul="DAFTAR USER")

    id_edit = input("\nMasukkan ID user yang ingin diedit (0 batal): ")
    if id_edit == "0":
        return

    if id_edit not in tabel["id"].astype(str).values:
        print("❌ ID tidak ditemukan!")
        return

    index = tabel[tabel["id"].astype(str) == id_edit].index[0]
    data_lama = tabel.loc[index]

    print("\nTekan ENTER jika tidak ingin mengubah data")

    # ===============================
    # EDIT USERNAME
    # ===============================
    while True:
        username = input(f"Username baru [{data_lama['username']}]: ").strip()
        if username == "":
            username = data_lama["username"]
            break

        valid, msg = validasi_username(username)
        if not valid:
            print(f"❌ {msg}")
            continue

        if username in tabel["username"].values and username != data_lama["username"]:
            print("❌ Username sudah digunakan!")
            continue
        break

    # ===============================
    # EDIT PASSWORD
    # ===============================
    password = data_lama["password"]
    ubah_pw = input("Ubah password? (y/n): ").lower()

    if ubah_pw == "y":
        while True:
            pw_baru = input("Password baru: ")
            valid, pesan = validasi_password(pw_baru)
            if not valid:
                print(f"❌ {pesan}")
                continue

            konfirmasi = input("Konfirmasi password: ")
            if konfirmasi != pw_baru:
                print("❌ Konfirmasi tidak sesuai")
                continue

            password = pw_baru
            break

    # ===============================
    # EDIT ROLE
    # ===============================
    daftar_role = ["kepala_divisi", "auditor", "direktur"]
    print("\nRole saat ini:", data_lama["role"])
    ganti_role = input("Ubah role? (y/n): ").lower()

    role = data_lama["role"]
    divisi = data_lama["divisi"]

    if ganti_role == "y":
        for i, r in enumerate(daftar_role, start=1):
            print(f"{i}. {r}")
        pilih = int(input("Pilih role: "))
        role = daftar_role[pilih - 1]

        if role == "kepala_divisi":
            tabel_divisi = baca_data("divisi")
            for i, d in enumerate(tabel_divisi["nama_divisi"], start=1):
                print(f"{i}. {d}")
            idx = int(input("Pilih divisi: ")) - 1
            divisi = tabel_divisi.iloc[idx]["nama_divisi"]
        else:
            divisi = "-"

    # ===============================
    # KONFIRMASI UPDATE
    # ===============================
    print("\n--- KONFIRMASI PERUBAHAN ---")
    print("Username :", data_lama["username"], "→", username)
    print("Role     :", data_lama["role"], "→", role)
    print("Divisi   :", data_lama["divisi"], "→", divisi)

    konfirmasi = input("Simpan perubahan? (y/n): ").lower()
    if konfirmasi != "y":
        print("❌ Perubahan dibatalkan")
        return

    # ===============================
    # SIMPAN
    # ===============================
    tabel.at[index, "username"] = username
    tabel.at[index, "password"] = password
    tabel.at[index, "role"] = role
    tabel.at[index, "divisi"] = divisi

    simpan_data("users", tabel)
    print("✅ Data user berhasil diperbarui!")
    input("Enter...")


# ===============================
# DELETE
# ===============================
def hapus_user():
    tabel_users = baca_data("users")
    if tabel_users.empty:
        print("Data kosong.")
        return

    tampilkan_interaktif(tabel_users, judul="DAFTAR USER")

    id_target = input("Masukkan ID user yang akan dihapus (0 batal): ")
    if id_target == "0":
        return

    if id_target not in tabel_users["id"].astype(str).values:
        print("❌ ID tidak ditemukan")
        return

    konfirmasi = input("Yakin ingin menghapus user ini? (y/n): ").lower()
    if konfirmasi != "y":
        print("❌ Penghapusan dibatalkan")
        return

    tabel_users = tabel_users[tabel_users["id"].astype(str) != id_target]
    simpan_data("users", tabel_users)

    print("✅ User berhasil dihapus")