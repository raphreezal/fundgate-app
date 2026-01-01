import pandas as pd
from modules.utility import baca_data, simpan_data, tampilkan_interaktif

def menu_divisi():
    while True:
        print("\n=== KELOLA DIVISI ===")
        print("1. Lihat Divisi")
        print("2. Tambah Divisi")
        print("3. Edit Divisi")
        print("4. Hapus Divisi")
        print("0. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            lihat_divisi()
        elif pilih == "2":
            tambah_divisi()
        elif pilih == "3":
            edit_divisi()
        elif pilih == "4":
            hapus_divisi()
        elif pilih == "0":
            break
        else:
            print("❌ Pilihan tidak valid")

def lihat_divisi():
    tabel = baca_data("divisi")
    if tabel.empty:
        print("Data divisi masih kosong.")
        return

    tampilkan_interaktif(tabel, judul="DAFTAR DIVISI")

def tambah_divisi():
    tabel = baca_data("divisi")

    while True:
        nama = input("Nama divisi (0 batal): ").strip()
        if nama == "0":
            return
        if not nama:
            print("❌ Nama divisi tidak boleh kosong")
            continue
        if not tabel.empty and nama in tabel["nama_divisi"].values:
            print("❌ Divisi sudah ada")
            continue
        break

    konfirmasi = input("Simpan divisi ini? (y/n): ").lower()
    if konfirmasi != "y":
        print("❌ Penambahan dibatalkan")
        return

    data_baru = {"nama_divisi": nama}
    tabel = pd.concat([tabel, pd.DataFrame([data_baru])], ignore_index=True)

    simpan_data("divisi", tabel)
    print("✅ Divisi berhasil ditambahkan")

def edit_divisi():
    tabel = baca_data("divisi")
    if tabel.empty:
        print("Data kosong.")
        return

    tampilkan_interaktif(tabel, judul="DAFTAR DIVISI")

    nama_lama = input("Nama divisi yang ingin diedit (0 batal): ")
    if nama_lama == "0":
        return

    if nama_lama not in tabel["nama_divisi"].values:
        print("❌ Divisi tidak ditemukan")
        return

    nama_baru = input(f"Nama baru [{nama_lama}]: ").strip()
    if nama_baru == "":
        print("❌ Tidak ada perubahan")
        return

    if nama_baru in tabel["nama_divisi"].values:
        print("❌ Nama divisi sudah digunakan")
        return

    konfirmasi = input("Simpan perubahan? (y/n): ").lower()
    if konfirmasi != "y":
        print("❌ Perubahan dibatalkan")
        return

    tabel.loc[tabel["nama_divisi"] == nama_lama, "nama_divisi"] = nama_baru
    simpan_data("divisi", tabel)

    print("✅ Divisi berhasil diperbarui")

def hapus_divisi():
    tabel = baca_data("divisi")
    if tabel.empty:
        print("Data kosong.")
        return

    tampilkan_interaktif(tabel, judul="DAFTAR DIVISI")

    nama = input("Nama divisi yang akan dihapus (0 batal): ")
    if nama == "0":
        return

    if nama not in tabel["nama_divisi"].values:
        print("❌ Divisi tidak ditemukan")
        return

    konfirmasi = input("Yakin hapus divisi ini? (y/n): ").lower()
    if konfirmasi != "y":
        print("❌ Penghapusan dibatalkan")
        return

    tabel = tabel[tabel["nama_divisi"] != nama]
    simpan_data("divisi", tabel)

    print("✅ Divisi berhasil dihapus")
