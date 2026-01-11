import pandas as pd
from modules.utility import (
    baca_data, simpan_data,
    clear_screen, header, tabel_rapih,
    validasi_username, validasi_password,
    generate_id_user, tampilkan_interaktif
)

def menu_admin(user_login=None):
    while True:
        clear_screen()
        header(subjudul="kelola user", user=user_login)
        # print("────────────── KELOLA USER ──────────────")
        print("[1] Lihat User")
        print("[2] Tambah User")
        print("[3] Edit User")
        print("[4] Hapus User")
        print("[0] Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            lihat_user(user_login)
        elif pilih == "2":
            tambah_user(user_login)
        elif pilih == "3":
            edit_user(user_login)
        elif pilih == "4":
            hapus_user(user_login)
        elif pilih == "0":
            break
        else:
            input("⚠️   Input tidak valid!\nTekan Enter untuk input ulang...\n")


def lihat_user(user_login=None):
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
    header(subjudul="daftar user", user=user_login)
    tampilkan_interaktif(df_tampil, judul="DAFTAR USER", show_judul=False)


def tambah_user(user_login=None):
    tabel = baca_data("users")
    tabel_divisi = baca_data("divisi")

    while True:
        clear_screen()
        header(subjudul="tambah user", user=user_login)
        # print("────────────── TAMBAH USER ──────────────\n")

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
            konfirmasi = input("Konfirmasi Password (0 batal): ").strip()
            if konfirmasi == "0":
                return
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
        header(subjudul="pilih role", user=user_login)
        # print("────────────── PILIH ROLE ──────────────")
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
                header(subjudul="pilih divisi", user=user_login)
                # print("────────────── PILIH DIVISI ──────────────\n")
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
        header(subjudul="konfirmasi data user", user=user_login)
        # print("────────────── KONFIRMASI DATA USER ──────────────\n")
        print(f"Username : {username}")
        print(f"Password : {(password)}")
        print(f"Role     : {role}")
        print(f"Divisi   : {divisi}")

        konfirmasi = input("\nSimpan user ini? (y/n): ").lower()
        if konfirmasi == "y":
            break
        elif konfirmasi == "n":
            input("⚠️   Penambahan dibatalkan.\nTekan Enter untuk input ulang...\n")
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



def edit_user(user_login=None):
    tabel = baca_data("users")
    tabel_display = tabel.copy()

    if tabel.empty:
        clear_screen()
        header(subjudul="edit user", user=user_login)
        input("⚠️   Data user kosong.\nTekan Enter untuk kembali...\n")
        return

    while True:
        clear_screen()
        header(subjudul="edit user", user=user_login)
        # print("──────────────────────────── DAFTAR USER ─────────────────────────────\n")
        # print(f"{'No':<4} {'ID':<8} {'Username':<15} {'Role':<20} {'Divisi'}")
        # print("-" * 70)

        # for i, row in tabel.iterrows():
        #     divisi = row['divisi'] if pd.notna(row['divisi']) and row['divisi'] != "" else "-"
        #     print(f"{i+1:<4} {row['id']:<8} {row['username']:<15} {row['role']:<20} {divisi}")
        
        for i in range(len(tabel_display)):
            tabel_display.at[i, 'No'] = i + 1
        tabel_display = tabel_display[["No", "id", "username", "role", "divisi"]]
        
        tabel_rapih(tabel_display, judul="DAFTAR USER")

        pilih = input("\nPilih nomor user (0 kembali): ").strip()

        if pilih == "0":
            return
        if not pilih.isdigit() or not (1 <= int(pilih) <= len(tabel)):
            input("⚠️   Pilihan tidak valid!\nTekan Enter untuk input ulang...\n")
            continue

        index = tabel.index[int(pilih) - 1]
        data = tabel.loc[index]
        batal_edit = False


        while True:
            clear_screen()
            header(subjudul="edit user", user=user_login)
            # print("────────────── EDIT USER ──────────────\n")
            print("DATA LAMA")
            print(f"ID       : {data['id']}")
            print(f"Username : {data['username']}")
            print(f"Password : {'*' * len(str(data['password']))}")
            print(f"Role     : {data['role']}")
            print(f"Divisi   : {data['divisi'] if pd.notna(data['divisi']) else '-'}")

            username_baru = input("\nUsername baru (Enter lewati | 0 kembali): ").strip()
            if username_baru == "0":
                break
            daftar_username = (
                tabel[tabel.index != index]["username"]
                .str.lower()
                .values
            )

            if username_baru != "":
                valid, pesan = validasi_username(username_baru)
                if not valid:
                    input(f"⚠️   {pesan}\nTekan Enter...\n")
                    continue

                if username_baru.lower() in daftar_username:
                    input("⚠️   Username sudah digunakan!\nTekan Enter untuk input ulang...\n")
                    continue
            else:
                username_baru = data['username']


            while True:
                print("\n=== Password minimal 8 karakter, huruf besar, kecil, angka & simbol ===")
                password_baru = input("Password baru (Enter lewati | 0 kembali): ").strip()

                if password_baru == "0":
                    batal_edit = True
                    break

                if password_baru == "":
                    password_baru = data['password']
                    break

                valid, pesan = validasi_password(password_baru)
                if not valid:
                    input("⚠️   Input tidak valid!\nTekan Enter untuk input ulang...")
                    continue

                while True:
                    konfirmasi = input("Konfirmasi password baru: ").strip()
                    if konfirmasi != password_baru:
                        input("⚠️   Konfirmasi tidak sesuai!\nTekan Enter untuk input ulang...")
                        continue
                    break

                break
            if batal_edit:
                break   # kembali ke daftar user, TANPA perubahan

            batal_edit = False
            while True:
                clear_screen()
                header(subjudul="pilih role", user=user_login)
                # print("────────────── PILIH ROLE ──────────────")
                print("[1] Direktur")
                print("[2] Manajer Keuangan")
                print("[3] Kepala Divisi")
                print("[4] Auditor")
                print("[Enter] Lewati (tetap sama)")
                print("[0] Kembali")

                pilih_role = input("Pilih role: ").strip()

                if pilih_role == "0":
                    batal_edit = True
                    break
                elif pilih_role == "":
                    role_baru = data['role']
                    break
                elif pilih_role == "1":
                    role_baru = "Direktur"
                elif pilih_role == "2":
                    role_baru = "Manajer Keuangan"
                elif pilih_role == "3":
                    role_baru = "Kepala Divisi"
                elif pilih_role == "4":
                    role_baru = "Auditor"
                else:
                    input("⚠️   Role tidak valid!\nTekan Enter untuk input ulang...")
                    continue

                break
            if batal_edit:
                break


            if role_baru == "Kepala Divisi":
                tabel_divisi = baca_data("divisi")

                if tabel_divisi.empty:
                    input("⚠️   Data divisi kosong!\nTekan Enter untuk input ulang...")
                    continue

                while True:
                    clear_screen()
                    header(subjudul="pilih divisi", user=user_login)
                    # print("────────────── PILIH DIVISI ──────────────")
                    for i, row in tabel_divisi.iterrows():
                        print(f"[{i+1}] {row['nama_divisi']}")
                    print("[Enter] Lewati (tetap sama)")
                    print("[0] Kembali")

                    pilih_divisi = input("Pilih divisi: ").strip()

                    if pilih_divisi == "0":
                        batal_edit = True
                        break
                    elif pilih_divisi == "":
                        divisi_baru = data['divisi']
                        break
                    elif pilih_divisi.isdigit() and 1 <= int(pilih_divisi) <= len(tabel_divisi):
                        divisi_baru = tabel_divisi.iloc[int(pilih_divisi) - 1]["nama_divisi"]
                        break
                    else:
                        input("⚠️   Divisi tidak valid!\nTekan Enter  untuk input ulang...")
                        continue
            else:
                divisi_baru = "-"
            if batal_edit:
                break


            clear_screen()
            header(subjudul="konfirmasi perubahan", user=user_login)
            # print("────────────── KONFIRMASI PERUBAHAN ──────────────\n")

            def status(lama, baru):
                return " (berubah)" if lama != baru else " (tetap)"

            print("DATA LAMA")
            print(f"Username : {data['username']}")
            print(f"Password : {'*' * len(str(data['password']))}")
            print(f"Role     : {data['role']}")
            print(f"Divisi   : {data['divisi'] if pd.notna(data['divisi']) else '-'}")

            print("\nDATA BARU")
            print(f"Username : {username_baru}{status(data['username'], username_baru)}")
            print(f"Password : {'*' * len(str(password_baru))}{status(data['password'], password_baru)}")
            print(f"Role     : {role_baru}{status(data['role'], role_baru)}")
            print(f"Divisi   : {divisi_baru}{status(data['divisi'], divisi_baru)}")

            while True:
                konfirmasi = input("\nYakin simpan perubahan? (y/n): ").lower()
                if konfirmasi == "y":
                    tabel.at[index, "username"] = username_baru
                    tabel.at[index, "password"] = password_baru
                    tabel.at[index, "role"] = role_baru
                    tabel.at[index, "divisi"] = divisi_baru
                    simpan_data("users", tabel)
                    input("✅  User berhasil diperbarui!\nTekan Enter untuk kembali...\n")
                    return
                elif konfirmasi == "n":
                    break
                else:
                    input("⚠️   Input tidak valid!\nTekan Enter untuk kembali...\n")

def hapus_user(user_login=None):
    tabel = baca_data("users")
    tabel_display = tabel.copy()

    if tabel.empty:
        clear_screen()
        header(subjudul="hapus user", user=user_login)
        input("⚠️   Data user kosong.\nTekan Enter untuk kembali...\n")
        return

    while True:
        # pilih user
        while True:
            clear_screen()
            header(subjudul="hapus user", user=user_login)
            # print("──────────────────────────── DAFTAR USER ─────────────────────────────\n")
            
            for i in range(len(tabel_display)):
                tabel_display.at[i, 'No'] = i + 1
            tabel_display = tabel_display[["No", "id", "username", "role", "divisi"]]
            
            tabel_rapih(tabel_display, judul="DAFTAR USER")

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
            header(subjudul="hapus user", user=user_login)
            # print("────────────── HAPUS USER ──────────────")
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
