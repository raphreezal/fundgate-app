import pandas as pd
from datetime import datetime
from modules.utility import baca_data, format_rupiah, simpan_data, tampilkan_interaktif, tabel_rapih, clear_screen
import random

# menu kepala divisi rev / najwa
def menu_kepala_divisi(user_sedang_login):
    while True:
        print(f"\n=== MENU KEPALA DIVISI: {user_sedang_login['divisi']} ===")
        print("1. Buat Pengajuan Dana")
        print("2. Riwayat Pengajuan Dana")
        print("0. Logout")

        pilihan = input("Pilih menu (0-2): ")

        if pilihan == "1":
            buat_pengajuan_dana(user_sedang_login)
        elif pilihan == "2":
            riwayat_pengajuan(user_sedang_login)
        elif pilihan == "0":
            print("\n======= Logout Berhasil! =======")
            break
        else:
            print("⚠️ Pilihan tidak valid. Silakan pilih menu yang tersedia!")

def buat_pengajuan_dana(user):
    print("\n=== FORM PENGAJUAN DANA ===")

    print("Jenis Pengajuan:")
    print("1. Operasional")
    print("2. Inventaris")
    print("3. Lainnya")
    pilih = input("Pilih: ")

    if pilih == "3":
        jenis_pengajuan = input("Masukkan jenis pengajuan: ")
    else:
        jenis_pengajuan = ["Operasional", "Inventaris"][int(pilih)-1]

    # generate ID pengajuan
    if jenis_pengajuan == "Operasional":
        id_pengajuan = "OPT-" + datetime.now().strftime("%H%M%S") + str(random.randint(0,99))
    elif jenis_pengajuan == "Inventaris":
        id_pengajuan = "INV-" + datetime.now().strftime("%H%M%S") + str(random.randint(0,99))
    else:
        id_pengajuan = "LNS-" + datetime.now().strftime("%H%M%S") + str(random.randint(0,99))

    tanggal = datetime.now().strftime("%Y-%m-%d")

    rincian_list = []
    total = 0

    # Form pengajuan    /farah
    while True:
        while True:
            print("\nInput Rincian:")
            print("1. Barang")
            print("2. Jasa")
            print("0. Cancel")
            tipe = input("Pilih tipe (0/1/2): ")

            if tipe == "1":
                tipe = "Barang"
                break
            elif tipe == "2":
                tipe = "Jasa"
                break
            elif tipe == "0":
                clear_screen()
                return
            else:
                print("⚠️ Pilihan tidak valid. Silakan pilih menu yang tersedia!")

        nama = input("Nama: ")
        jumlah = int(input("Jumlah: "))
        harga = int(input("Harga satuan: "))
        subtotal = jumlah * harga
        total += subtotal

        id_rincian = "RIN-" + datetime.now().strftime("%H%M%S") + str(random.randint(0,99))

        rincian_list.append({
            "id_rincian": id_rincian,
            "id_pengajuan": id_pengajuan,
            "tipe": tipe,
            "nama_item": nama,
            "jumlah": jumlah,
            "harga_satuan": harga,
            "subtotal": subtotal
        })

        tabel_rapih(rincian_list, "LIST RINCIAN")

        if input("Tambah lagi? (y/n): ").lower() != "y":
            break

    # Ngecek limit
    data_keuangan = baca_data("keuangan")
    limit_pengajuan = data_keuangan.loc[0, "limit_pengajuan"]

    clear_screen()
    tabel_rapih(rincian_list, "RINGKASAN PENGAJUAN")

    print(f"\nTOTAL PENGAJUAN : {format_rupiah(total)}")
    print(f"LIMIT PENGAJUAN : {format_rupiah(limit_pengajuan)}")

    status_pengajuan = "Menunggu"
    catatan_manajer = ""

    # Nominal pengajuan lebih dari limit    /farah
    if total > limit_pengajuan:
        print("\n⚠️  Nominal pengajuan melebihi limit!")
        print("1. Ajukan sebagai Dana Darurat")
        print("2. Batalkan Pengajuan")

        while True:
            opsi = input("Pilih opsi (1/2): ")
            if opsi == "1":
                status_pengajuan = "Menunggu (Darurat)"
                catatan_manajer = "Pengajuan dana darurat (melebihi limit)"
                break
            elif opsi == "2":
                print("\n======= Pengajuan dibatalkan =======")
                return
            else:
                print("⚠️ Pilihan tidak valid. Silakan pilih menu yang tersedia!")
    else:
        if input("\nKonfirmasi pengajuan? (y/n): ").lower() != "y":
            return
    
    # Simpan data pengajuan     /farah
    data_pengajuan = {
        "id_pengajuan": id_pengajuan,
        "tanggal": tanggal,
        "id_kepala_divisi": user["id"],
        "nama_kepala_divisi": user["username"],
        "divisi": user["divisi"],
        "jenis_pengajuan": jenis_pengajuan,
        "status": status_pengajuan,
        "total": total,
        "catatan_manajer": catatan_manajer
    }

    df_pengajuan = pd.concat([
        baca_data("pengajuan"),
        pd.DataFrame([data_pengajuan])
    ], ignore_index=True)

    df_rincian = pd.concat([
        baca_data("rincian_pengajuan"),
        pd.DataFrame(rincian_list)
    ], ignore_index=True)

    simpan_data("pengajuan", df_pengajuan)
    simpan_data("rincian_pengajuan", df_rincian)

    print("\n======= Pengajuan berhasil dibuat! =======")



# riwayat
def riwayat_pengajuan(user):
    clear_screen()
    pengajuan = baca_data("pengajuan")
    rincian = baca_data("rincian_pengajuan")

    data = pengajuan[pengajuan["id_kepala_divisi"] == user["id"]]

    if data.empty:
        print("Belum ada pengajuan.")
        return

    # print("\n=== RIWAYAT PENGAJUAN ===")
    # print(data[["id_pengajuan", "tanggal", "total", "status"]].to_string(index=False))

    data_view = data.copy()
    data_view["total"] = data_view["total"].map(format_rupiah)
    tabel_rapih(data_view[["id_pengajuan","tanggal", "jenis_pengajuan", "total", "status"]], "RIWAYAT PENGAJUAN")

    print("\n1. Lihat Detail")
    print("2. Edit Pengajuan")
    print("3. Hapus Pengajuan")
    print("0. Kembali")

    pilih = input("Pilih: ")

    if pilih == "1":
        lihat_detail_pengajuan(rincian)
    elif pilih == "2":
        edit_pengajuan(user, pengajuan, rincian)
    elif pilih == "3":
        hapus_pengajuan(user, pengajuan, rincian)


# detail
def lihat_detail_pengajuan(rincian):
    while True:
        idp = input("\nMasukkan ID Pengajuan (0 untuk kembali): ")
        # biar bisa back    /farah
        if idp == "0":
            return

        detail = rincian[rincian["id_pengajuan"] == idp]

        if detail.empty:
            print("⚠️  Detail tidak ditemukan. Coba lagi!")
        else:
            tampilkan_interaktif(
                detail[["tipe", "nama_item", "jumlah", "harga_satuan", "subtotal"]],
                "Detail Pengajuan"
            )
            return

# edit form (jika status masih menunggu) / najwa
def edit_pengajuan(user, pengajuan, rincian):
    idp = input("ID pengajuan yang diedit: ")

    data = pengajuan[pengajuan["id_pengajuan"] == idp]
    if data.empty:
        print("ID tidak ditemukan.")
        return

    if data.iloc[0]["status"] != "Menunggu":
        print("======= Tidak dapat diedit. Pengajuan sudah diproses. =======")
        return

    rincian = rincian[rincian["id_pengajuan"] != idp]

    total = 0
    rincian_baru = []

    while True:
        print("\nInput Rincian:")
        print("1. Barang")
        print("2. Jasa")
        print("0. Cancel")
        tipe = input("\nPilih tipe (0/1/2): ")
        if tipe == "1":
            tipe = "Barang"
            break
        elif tipe == "2":
            tipe = "Jasa"
            break
        elif tipe == "0":
            clear_screen()
            return
        else:
            print("Pilihan tidak valid.")

        nama = input("Nama: ")
        jumlah = int(input("Jumlah: "))
        harga = int(input("Harga satuan: "))
        subtotal = jumlah * harga

        total += subtotal

        rincian_baru.append({
            "id_pengajuan": idp,
            "tipe": tipe,
            "nama_item": nama,
            "jumlah": jumlah,
            "harga_satuan": harga,
            "subtotal": subtotal
        })

        if input("Tambah lagi? (y/n): ").lower() != "y":
            break

    idx = pengajuan[pengajuan["id_pengajuan"] == idp].index[0]
    pengajuan.at[idx, "total"] = total

    rincian = pd.concat([rincian, pd.DataFrame(rincian_baru)], ignore_index=True)

    simpan_data("pengajuan", pengajuan)
    simpan_data("rincian_pengajuan", rincian)

    print("======= Pengajuan berhasil diedit! =======")


# hapus form (jika status masih menunggu) / najwa
def hapus_pengajuan(user, pengajuan, rincian):
    idp = input("ID pengajuan yang dihapus: ")

    data = pengajuan[pengajuan["id_pengajuan"] == idp]
    if data.empty:
        print("ID tidak ditemukan.")
        return

    if data.iloc[0]["status"] != "Menunggu":
        print("======= Tidak dapat dihapus. =======")
        return

    pengajuan = pengajuan[pengajuan["id_pengajuan"] != idp]
    rincian = rincian[rincian["id_pengajuan"] != idp]

    simpan_data("pengajuan", pengajuan)
    simpan_data("rincian_pengajuan", rincian)

    print("======= Pengajuan berhasil dihapus! =======")
