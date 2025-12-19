import csv
import os

file_pengajuan = "pengajuan.csv"

# Cek File CSV
def cek_file_pengajuan():
    if not os.path.exists(file_pengajuan):
        with open(file_pengajuan, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "kode",
                "pengaju",
                "divisi",
                "barang",
                "deskripsi",
                "total_estimasi",
                "status"
            ])

# Cek Kode Pengajuan
def kode_sudah_ada(kode):
    with open(file_pengajuan, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["kode"] == kode:
                return True
    return False

# Form Pengajuan Dana
def form_pengajuan_dana(user):
    print("\n======= FORM PENGAJUAN DANA =======")

    while True:
        kode = input("Kode Pengajuan : ")
        if kode_sudah_ada(kode):
            print("Kode sudah digunakan!")
        else:
            break

    daftar_barang = []
    total_estimasi = 0

    while True:
        nama = input("Nama barang/jasa : ")
        qty = int(input("Kuantitas       : "))
        harga = int(input("Harga satuan    : "))

        subtotal = qty * harga
        total_estimasi += subtotal

        daftar_barang.append(f"{nama} x{qty} @{harga}")

        if input("Tambah barang? (y/n): ").lower() != "y":
            break

    deskripsi = input("Deskripsi pengajuan: ")

    data = {
        "kode": kode,
        "pengaju": user["username"],
        "divisi": user["divisi"],
        "barang": "; ".join(daftar_barang),
        "deskripsi": deskripsi,
        "total_estimasi": total_estimasi,
        "status": "pending"
    }

    with open(file_pengajuan, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

    print("\nPengajuan berhasil dikirim!")
    print(f"Kode Pengajuan : {kode}")
    print(f"Total Estimasi : Rp{total_estimasi}")

# Cek Status Pengajuan
def cek_status_pengajuan(user):
    print("\n===== STATUS PENGAJUAN =====")

    with open(file_pengajuan, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        ada = False

        for row in reader:
            if row["pengaju"] == user["username"]:
                ada = True
                print("----------------------------")
                print(f"Divisi         : {row['divisi']}")
                print(f"Kode           : {row['kode']}")
                print(f"Barang         : {row['barang']}")
                print(f"Total Estimasi : Rp{row['total_estimasi']}")
                print(f"Status         : {row['status']}")

        if not ada:
            print("Belum ada pengajuan.")

# Menu Kepala Divisi
def menu_kepala_divisi(user):
    cek_file_pengajuan()

    while True:
        print("\n===== MENU KEPALA DIVISI =====")
        print("1. Pengajuan Dana")
        print("2. Status Pengajuan")
        print("3. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            form_pengajuan_dana(user)
        elif pilihan == "2":
            cek_status_pengajuan(user)
        elif pilihan == "3":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid!")