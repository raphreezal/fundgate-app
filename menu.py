from auth import login
from logic import (
    ajukan_dana,
    proses_pengajuan,
    tampilkan_laporan,
    set_anggaran,
    tampilkan_semua_user,
    hapus_user
)

def menu_login():
    print("=== LOGIN SISTEM KEUANGAN ===")
    u = input("Username: ")
    p = input("Password: ")

    user = login(u, p)
    if not user:
        print("Login gagal")
        return

    role = user['role']

    # KEPALA DIVISI
    if role == "kepala_divisi":
        kode_divisi = input("Kode Divisi: ")
        nominal = input("Nominal: ")
        tujuan = input("Tujuan: ")
        ajukan_dana(user['id_kepala_divisi'], kode_divisi, nominal, tujuan)

    # MANAJER KEUANGAN
    elif role == "manajer_keuangan":
        while True:
            print("\n=== MENU MANAJER KEUANGAN ===")
            print("1. Penyetujuan Pengajuan Dana")
            print("2. Laporan")
            print("3. Manajemen User")
            print("4. Manajemen Anggaran")
            print("5. Manajemen Divisi")
            print("6. Logout")

            pilih = input("Pilih menu: ")

            if pilih == "1":
                tampilkan_laporan()
                kode = input("Masukkan kode pengajuan: ")
                keputusan = input("Disetujui / Ditolak: ")
                proses_pengajuan(kode, keputusan, user['id_manajer_keuangan'])

            elif pilih == "2":
                tampilkan_laporan()

            elif pilih == "3":
                print("\n1. Lihat User")
                print("2. Hapus User")
                sub = input("Pilih: ")

                if sub == "1":
                    tampilkan_semua_user()
                elif sub == "2":
                    file = input("File CSV user: ")
                    username = input("Username: ")
                    hapus_user(file, username)

            elif pilih == "4":
                tahun = input("Tahun: ")
                total = input("Total Anggaran: ")
                set_anggaran(tahun, total)

            elif pilih == "6":
                print("Logout berhasil")
                break

    # DIREKTUR & AUDITOR
    elif role in ["direktur", "auditor"]:
        tampilkan_laporan()
