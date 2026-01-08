import pandas as pd
import re
from modules.utility import (
    baca_data, simpan_data, tabel_rapih,
    tampilkan_interaktif, clear_screen, header
)

# validasi nama divisi / najwa
def validasi_nama_divisi(nama):
    return bool(re.fullmatch(r"[A-Za-z]+( [A-Za-z]+)*", nama))


# buat id divisi otomatis / najwa
def generate_id_divisi(tabel):
    if tabel.empty:
        return "D001"
    terakhir = tabel["id_divisi"].astype(str).str[1:].astype(int).max()
    return f"D{terakhir + 1:03d}"

def menu_divisi(user_sedang_login=None):
    while True:
        clear_screen()
        header(subjudul="kelola divisi", user=user_sedang_login)
        # print("────────────── KELOLA DIVISI ──────────────")
        print("[1] Lihat Divisi")
        print("[2] Tambah Divisi")
        print("[3] Edit Divisi")
        print("[4] Hapus Divisi")
        print("[0] Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            lihat_divisi(user_sedang_login)
        elif pilih == "2":
            tambah_divisi(user_sedang_login)
        elif pilih == "3":
            edit_divisi(user_sedang_login)
        elif pilih == "4":
            hapus_divisi()
        elif pilih == "0":
            break
        else:
            print("⚠️   Input tidak valid!")
            input("Tekan Enter untuk input ulang...")

# lihat divisi / najwa
def lihat_divisi(user_login=None):
    tabel = baca_data("divisi")

    if tabel.empty:
        input("⚠️   Data divisi masih kosong.\nTekan Enter untuk kembali...")
        return

    clear_screen()
    header(subjudul="lihat divisi", user=user_login)
    tampilkan_interaktif(tabel, judul="DAFTAR DIVISI", show_judul=True)


# tambah divisi / najwa
def tambah_divisi(user_login=None):
    tabel = baca_data("divisi")

    while True:
        clear_screen()
        header(subjudul="tambah divisi", user=user_login)

        # tampilin daftar divisi yang sudah ada / najwa
        # print("──────────────────────────── DAFTAR DIVISI ─────────────────────────────\n")
        # print(f"{'No':<4} {'ID Divisi':<10} {'Nama Divisi'}")
        # print("-" * 50)

        # for i, row in tabel.iterrows():
        #     print(f"{i+1:<4} {row['id_divisi']:<10} {row['nama_divisi']}")
        
        # ganti ke tabulate / kei
        tabel_rapih(tabel[["id_divisi", "nama_divisi"]], judul="DAFTAR DIVISI")

        # print("\n────────────── TAMBAH DIVISI ──────────────")

        nama = input("\nNama divisi baru (0 batal): ").strip()

        if nama == "0":
            return

        if not nama:
            print("\n⚠️   Nama divisi tidak boleh kosong!")
            input("Tekan Enter untuk input ulang...")
            continue

        if not validasi_nama_divisi(nama):
            print("\n⚠️   Nama divisi hanya boleh huruf dan spasi!")
            input("Tekan Enter untuk input ulang...")
            continue

        if not tabel.empty and nama.lower() in tabel["nama_divisi"].str.lower().values:
            print("\n⚠️   Divisi sudah ada!")
            input("Tekan Enter untuk input ulang...")
            continue
        break

    if input("\nSimpan divisi ini? (y/n): ").lower() != "y":
        print("⚠️    Penambahan dibatalkan.")
        input("Tekan Enter untuk melanjutkan...")
        return

    id_divisi = generate_id_divisi(tabel)

    tabel = pd.concat(
        [tabel, pd.DataFrame([{
            "id_divisi": id_divisi,
            "nama_divisi": nama
        }])],
        ignore_index=True
    )

    simpan_data("divisi", tabel)

    print("\n✅  Divisi berhasil ditambahkan!")
    input("Tekan Enter untuk melanjutkan...")


# edit divisi / najwa
def edit_divisi(user_login=None):
    tabel = baca_data("divisi")

    if tabel.empty:
        clear_screen()
        header(subjudul="kelola divisi", user=user_login)
        print("⚠️    Data divisi kosong.")
        input("Tekan Enter untuk kembali...")
        return

    # pilih divisi / najwa
    while True:
        clear_screen()
        header(subjudul="edit divisi", user=user_login)
        # print("──────────────────────────── DAFTAR DIVISI ─────────────────────────────\n")
        # print(f"{'No':<4} {'ID Divisi':<10} {'Nama Divisi'}")
        # print("-" * 50)

        # for i, row in tabel.iterrows():
        #     print(f"{i+1:<4} {row['id_divisi']:<10} {row['nama_divisi']}")
        
        # ganti ke tabulate / kei
        tabel_rapih(tabel[["id_divisi", "nama_divisi"]], judul="DAFTAR DIVISI")
        
        print("\nPilih yang ingin diedit")
        pilih = input("Nomor divisi (0 batal): ").strip()

        if not pilih.isdigit():
            input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...")
            continue

        pilih = int(pilih)

        if pilih == 0:
            return

        if not (1 <= pilih <= len(tabel)):
            input("⚠️   Nomor tidak valid!\nTekan Enter untuk input ulang...")
            continue

        index = tabel.index[pilih - 1]

        # form edit / najwa
        while True:
            clear_screen()
            header(subjudul="edit divisi", user=user_login)

            data_lama = tabel.loc[index]

            # print("────────────── EDIT DIVISI ──────────────")
            print("ID Divisi   :", data_lama["id_divisi"])
            print("Nama Lama   :", data_lama["nama_divisi"])

            nama_baru = input("\nNama divisi baru (Enter/0 kembali): ").strip()

            if nama_baru == "" or nama_baru == "0": #kembali ke pilih nomor / najwa
                break

            if not validasi_nama_divisi(nama_baru):
                input("⚠️   Nama hanya boleh huruf dan spasi!\nTekan Enter untuk input ulang...")
                continue

            if nama_baru.lower() in tabel["nama_divisi"].str.lower().values:
                input("⚠️   Nama divisi sudah ada!\nTekan Enter untuk input ulang...")
                continue

            # konfirmasi simpan perubahan / najwa
            while True:
                konfirmasi = input("\nYakin ingin menyimpan perubahan? (y/n): ").lower()

                if konfirmasi == "y":
                    tabel.at[index, "nama_divisi"] = nama_baru
                    simpan_data("divisi", tabel)
                    input("✅  Divisi berhasil diperbarui!\nTekan Enter untuk melanjutkan...")
                    return

                elif konfirmasi == "n":
                    break

                else:
                    input("⚠️   Input tidak valid! (y/n)\nTekan Enter untuk input ulang...")


# hapus divisi / najwa
def hapus_divisi(user_login=None):
    tabel = baca_data("divisi")

    if tabel.empty:
        clear_screen()
        header(subjudul="daftar divisi", user=user_login)
        print("⚠️    Data divisi kosong.")
        input("Tekan Enter untuk kembali...")
        return

    while True:  # 🔁 loop utama hapus divisi
        # pilih divisi / najwa
        while True:
            clear_screen()
            header(subjudul="hapus divisi", user=user_login)
            # print("──────────────────────────── DAFTAR DIVISI ─────────────────────────────\n")
            # print(f"{'No':<4} {'ID Divisi':<10} {'Nama Divisi'}")
            # print("-" * 50)

            # for i, row in tabel.iterrows():
            #     print(f"{i+1:<4} {row['id_divisi']:<10} {row['nama_divisi']}")
            
            # ganti ke tabulate / kei
            tabel_rapih(tabel[["id_divisi", "nama_divisi"]], judul="DAFTAR DIVISI")
            
            print("\nPilih yang ingin dihapus")
            pilih = input("Nomor divisi (0 batal): ").strip()

            if not pilih.isdigit():
                input("⚠️   Input harus angka!\nTekan Enter untuk input ulang...")
                continue

            pilih = int(pilih)

            if pilih == 0:
                return  # keluar dari hapus_divisi

            if 1 <= pilih <= len(tabel):
                index = tabel.index[pilih - 1]
                data = tabel.loc[index]
                break
            else:
                input("⚠️   Nomor tidak valid!\nTekan Enter untuk input ulang...")

        # konfirmasi hapus / najwa
        while True:
            clear_screen()
            header(subjudul="hapus divisi", user=user_login)
            # print("────────────── HAPUS DIVISI ──────────────")
            print("ID Divisi   :", data["id_divisi"])
            print("Nama Divisi :", data["nama_divisi"])

            konfirmasi = input("\nYakin hapus divisi ini? (y/n): ").lower().strip()

            if konfirmasi == "y":
                tabel = tabel.drop(index)
                simpan_data("divisi", tabel)
                input("✅  Divisi berhasil dihapus!\nTekan Enter untuk melanjutkan...")
                return

            elif konfirmasi == "n":
                break  # 🔙 KEMBALI KE PILIH NOMOR DIVISI

            else:
                input("⚠️   Input tidak valid! (hanya y / n)\nTekan Enter untuk input ulang...")