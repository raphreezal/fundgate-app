import pandas as pd
from modules.utility import (
    baca_data, simpan_data,
    clear_screen, header,
    validasi_username, validasi_password,
    generate_id_user, tampilkan_interaktif
)

def menu_admin(user_login=None):
    while True:
        clear_screen()
        header()
        print("────────────── KELOLA USER ──────────────")
        print("[1] Lihat User")
        print("[2] Tambah User")
        print("[3] Edit User")
        print("[4] Hapus User")
        print("[0] Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            lihat_user()
        elif pilih == "2":
            tambah_user()
        elif pilih == "3":
            edit_user()
        elif pilih == "4":
            hapus_user()
        elif pilih == "0":
            break
        else:
            input("⚠️   Input tidak valid!\nTekan Enter untuk input ulang...\n")


def lihat_user():
    tabel = baca_data("users")

    if tabel.empty:
        input("⚠️   Data user kosong.\nTekan Enter untuk kembali...\n")
        return
    
    # sembunyikan password / najwa
    df_tampil = tabel.copy()
    if "password" in df_tampil.columns:
        df_tampil["password"] = "*****"

    # divisi yg kosong jd - / najwa
    if "divisi" in df_tampil.columns:
        df_tampil["divisi"] = df_tampil["divisi"].fillna("-")

    clear_screen()
    header()
    print("────────────────────────── DAFTAR USER ───────────────────────────\n")
    tampilkan_interaktif(df_tampil) 


def tambah_user():
    tabel = baca_data("users")
    tabel_divisi = baca_data("divisi")

    while True:
        clear_screen()
        header()
        print("────────────── TAMBAH USER ──────────────\n")

        username = input("Username (0 batal): ").strip()
        if username == "0":
            return

        valid, pesan = validasi_username(username)
        if not valid:
            input(f"⚠️   {pesan}\nTekan Enter untuk input ulang...\n")
            continue

        if not tabel.empty and username.lower() in tabel["username"].str.lower().values:
            input("⚠️   Username sudah digunakan!\nTekan Enter untuk input ulang...\n")
            continue

        break

    while True:
        print("\n=== Password harus terdiri dari minimal 8 karakter, huruf kapital, huruf kecil, angka, dan simbol. ===")
        password = input("Password (0 batal): ").strip()
        if password == "0":
            return

        if not password:
            input("⚠️   Password tidak boleh kosong!\nTekan Enter untuk input ulang...\n")
            continue

        if " " in password:
            input("⚠️   Password tidak boleh mengandung spasi!\nTekan Enter untuk input ulang...\n")
            continue

        valid, pesan = validasi_password(password)
        if not valid:
            input("⚠️   Inputan tidak valid!\nTekan Enter untuk input ulang...\n")
            continue

        while True:
            konfirmasi = input("Konfirmasi Password: ").strip()
            if not konfirmasi:
                input("⚠️   Konfirmasi password tidak boleh kosong!\nTekan Enter untuk input ulang...\n")
                continue
            if konfirmasi != password:
                input("⚠️   Konfirmasi password tidak sesuai!\nTekan Enter untuk input ulang...\n")
                continue
            break

        break

    # pilih role / najwa
    while True:
        clear_screen()
        header()
        print("────────────── PILIH ROLE ──────────────")
        print("[1] Direktur")
        print("[2] Manajer Keuangan")
        print("[3] Kepala Divisi")
        print("[4] Auditor")

        pilih_role = input("Pilih role (1-4): ").strip()

        if not pilih_role.isdigit():
            input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...\n")
            continue

        if pilih_role == "1":
            role = "Direktur"
            divisi = "-"
            break
        elif pilih_role == "2":
            role = "Manajer Keuangan"
            divisi = "-"
            break
        elif pilih_role == "3":
            role = "Kepala Divisi"

            # pilih divisi / najwa
            if tabel_divisi.empty:
                input("⚠️   Data divisi kosong!\nTekan Enter untuk kembali...\n")
                return

            while True:
                clear_screen()
                header()
                print("────────────── PILIH DIVISI ──────────────\n")
                print(f"{'No':<4} {'ID Divisi':<10} {'Nama Divisi'}")
                print("-" * 40)

                for i, row in tabel_divisi.iterrows():
                    print(f"{i+1:<4} {row['id_divisi']:<10} {row['nama_divisi']}")

                pilih_divisi = input("\nPilih nomor divisi: ").strip()

                if not pilih_divisi.isdigit():
                    input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...\n")
                    continue

                pilih_divisi = int(pilih_divisi)
                if 1 <= pilih_divisi <= len(tabel_divisi):
                    divisi = tabel_divisi.iloc[pilih_divisi - 1]["nama_divisi"]
                    break
                else:
                    input("⚠️   Nomor divisi tidak valid!\nTekan Enter untuk input ulang...\n")

            break

        elif pilih_role == "4":
            role = "Auditor"
            divisi = "-"
            break
        else:
            input("⚠️   Pilihan tidak valid!\nTekan Enter untuk input ulang...\n")

    # konfirmasi
    while True:
        clear_screen()
        header()
        print("────────────── KONFIRMASI DATA USER ──────────────\n")
        print(f"Username : {username}")
        print(f"Password : {(password)}")
        print(f"Role     : {role}")
        print(f"Divisi   : {divisi}")

        konfirmasi = input("\nSimpan user ini? (y/n): ").lower()
        if konfirmasi == "y":
            break
        elif konfirmasi == "n":
            input("⚠️   Penambahan dibatalkan.\nTekan Enter untuk kembali...\n")
            return
        else:
            input("⚠️   Input tidak valid! (y/n)\nTekan Enter untuk input ulang...\n")

    #simpen
    id_user = generate_id_user(tabel)

    data_baru = {
        "id": id_user,
        "username": username,
        "password": password,
        "role": role,
        "divisi": divisi
    }

    tabel = pd.concat([tabel, pd.DataFrame([data_baru])], ignore_index=True)
    simpan_data("users", tabel)

    input("✅  User berhasil ditambahkan!\nTekan Enter untuk kembali...\n")



def edit_user():
    tabel = baca_data("users")

    if tabel.empty:
        clear_screen()
        header()
        input("⚠️   Data user kosong.\nTekan Enter untuk kembali...\n")
        return

    while True:
        # PILIH USER
        while True:
            clear_screen()
            header()
            print("──────────────────────────── DAFTAR USER ─────────────────────────────\n")
            print(f"{'No':<4} {'ID':<8} {'Username':<15} {'Role':<20} {'Divisi'}")
            print("-" * 70)

            for i, row in tabel.iterrows():
                divisi = row['divisi'] if pd.notna(row['divisi']) else "-"
                print(f"{i+1:<4} {row['id']:<8} {row['username']:<15} {row['role']:<20} {divisi}")

            pilih = input("\nPilih nomor user (0 batal): ").strip()

            if pilih == "0":
                return
            if not pilih.isdigit():
                input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...\n")
                continue

            pilih = int(pilih)
            if 1 <= pilih <= len(tabel):
                index = tabel.index[pilih - 1]
                data = tabel.loc[index]
                break
            else:
                input("⚠️   Nomor tidak valid!\nTekan Enter untuk input ulang...\n")

        # FORM EDIT
        while True:
            clear_screen()
            header()
            print("────────────── EDIT USER ──────────────")
            print("DATA LAMA")
            print(f"ID       : {data['id']}")
            print(f"Username : {data['username']}")
            print(f"Password : {'*' * len(data['password'])}")
            print(f"Role     : {data['role']}")
            print(f"Divisi   : {data['divisi'] if pd.notna(data['divisi']) else '-'}")

            # USERNAME BARU
            username_baru = input("\nUsername baru (Enter untuk lewati): ").strip()
            if username_baru == "0":
                break
            if username_baru == "":
                username_baru = data['username']
            else:
                valid, pesan = validasi_username(username_baru)
                if not valid:
                    input(f"⚠️   {pesan}\nTekan Enter untuk input ulang...\n")
                    continue
                if username_baru.lower() in tabel["username"].str.lower().values and username_baru.lower() != data['username'].lower():
                    input("⚠️   Username sudah dipakai!\nTekan Enter untuk input ulang...\n")
                    continue

            # PASSWORD BARU
            print("\n=== Password harus terdiri dari minimal 8 karakter, huruf kapital, huruf kecil, angka, dan simbol. ===")
            password_baru = input("Password baru (Enter untuk lewati): ").strip()
            if password_baru == "0":
                break
            if password_baru == "":
                password_baru = data['password']
            else:
                valid, pesan = validasi_password(password_baru)
                if not valid:
                    input("⚠️   Inputan tidak valid!\nTekan Enter untuk input ulang...\n\n")
                    continue

                # KONFIRMASI PASSWORD
                konfirmasi = input("Konfirmasi password baru: ").strip()
                if konfirmasi == "":
                    input("⚠️   Konfirmasi password tidak boleh kosong!\nTekan Enter untuk input ulang...\n\n")
                    continue
                if konfirmasi != password_baru:
                    input("⚠️   Konfirmasi password tidak sesuai!\nTekan Enter untuk input ulang...\n")
                    continue

            role_baru = input("Role baru (Enter untuk lewati): ").strip()
            if role_baru == "":
                role_baru = data['role']

            divisi_baru = input("Divisi baru (Enter untuk lewati): ").strip()
            if divisi_baru == "":
                divisi_baru = data['divisi']

            while True:
                konfirmasi = input("\nYakin simpan perubahan? (y/n): ").lower()
                if konfirmasi == "y":
                    tabel.at[index, "username"] = username_baru
                    tabel.at[index, "password"] = password_baru
                    tabel.at[index, "role"] = role_baru
                    tabel.at[index, "divisi"] = divisi_baru
                    simpan_data("users", tabel)
                    input("✅  User berhasil diperbarui!\nTekan Enter untuk melanjutkan...\n")
                    return
                elif konfirmasi == "n":
                    break
                else:
                    input("⚠️   Input tidak valid!\nTekan Enter untuk input ulang...\n")


def hapus_user():
    tabel = baca_data("users")

    if tabel.empty:
        clear_screen()
        header()
        input("⚠️   Data user kosong.\nTekan Enter...\n")
        return

    while True:
        # pilih user
        while True:
            clear_screen()
            header()
            print("──────────────────────────── DAFTAR USER ─────────────────────────────\n")
            print(f"{'No':<4} {'ID':<8} {'Username':<15} {'Role':<20} {'Divisi'}")
            print("-" * 70)

            for i, row in tabel.iterrows():
                print(f"{i+1:<4} {row['id']:<8} {row['username']:<15} {row['role']:<20} {row['divisi']}")

            pilih = input("\nPilih nomor user (0 batal): ").strip()

            if not pilih.isdigit():
                input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...\n")
                continue

            pilih = int(pilih)

            if pilih == 0:
                return

            if 1 <= pilih <= len(tabel):
                index = tabel.index[pilih - 1]
                data = tabel.loc[index]
                break
            else:
                input("⚠️   Nomor tidak valid!\nTekan Enter untuk input ulang...\n")

        # konfirmasi hapus
        while True:
            clear_screen()
            header()
            print("────────────── HAPUS USER ──────────────")
            print("ID       :", data["id"])
            print("Username :", data["username"])

            konfirmasi = input("\nYakin hapus user ini? (y/n): ").lower()

            if konfirmasi == "y":
                tabel = tabel.drop(index)
                simpan_data("users", tabel)
                input("✅  User berhasil dihapus!\nTekan Enter untuk melanjutkan...\n")
                return

            elif konfirmasi == "n":
                break  # kembali ke pilih nomor user

            else:
                input("⚠️   Input tidak valid!\nTekan Enter untuk input ulang...\n")
