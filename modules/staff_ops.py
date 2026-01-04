import pandas as pd
from datetime import datetime
import random
from modules.utility import (
    baca_data, simpan_data, format_rupiah,
    clear_screen, header, tabel_rapih
)

# menu utama kepala divisi  /najwa
def menu_kepala_divisi(user):
    while True:
        # clear screen & header biar rapih  /farah
        clear_screen()
        header()
        print(f"─────── MENU KEPALA DIVISI: {user['divisi']} ───────")
        print("1. 💰 Buat Pengajuan Dana")
        print("2. 📊 Riwayat Pengajuan Dana")
        print("0. 🔒 Logout")

        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            buat_pengajuan_dana(user)
        elif pilih == "2":
            riwayat_pengajuan(user)
        elif pilih == "0":
            return
        else:
            input("\n⚠️  Pilihan tidak valid! Tekan Enter untuk input ulang...")


# form pengajuan dana
def buat_pengajuan_dana(user):

    # jenis pengajuan
    while True:
        # clear screen & header biar rapih  /farah
        clear_screen()
        header()
        print("──────────── FORM PENGAJUAN DANA ────────────")
        print("Jenis        :")
        print("1. Operasional")
        print("2. Inventaris")
        print("3. Lainnya")
        print("0. Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "0":
            return
        elif pilih == "1":
            jenis = "Operasional"
            prefix = "OPT"
            break
        elif pilih == "2":
            jenis = "Inventaris"
            prefix = "INV"
            break
        elif pilih == "3":
            jenis = input("Masukkan jenis pengajuan: ").strip()
            if jenis:
                prefix = "LNS"
                break
            input("\n⚠️  Tidak boleh kosong! Tekan Enter untuk input ulang...")
        else:
            input("\n⚠️  Pilihan tidak valid! Tekan Enter untuk input ulang...")

    id_pengajuan = f"{prefix}-{datetime.now().strftime('%H%M%S')}{random.randint(10,99)}"
    id_rincian = f"RIN-{datetime.now().strftime('%H%M%S')}{random.randint(10,99)}"
    tanggal = datetime.now().strftime("%Y-%m-%d")

    rincian = []
    total = 0

    # loop rincian
    while True:

        # tipe pengajuan
        while True:
            clear_screen()
            header()
            print("──────────── FORM PENGAJUAN DANA ────────────")
            print(f"Jenis        : {jenis}")
            print("Tipe         :")
            print("1. Barang")
            print("2. Jasa")
            print("0. Batal")

            pilih_tipe = input("Pilih: ").strip()

            if pilih_tipe == "0":
                goto_simpan = True
                break
            elif pilih_tipe == "1":
                tipe = "Barang"
                goto_simpan = False
                break
            elif pilih_tipe == "2":
                tipe = "Jasa"
                goto_simpan = False
                break
            else:
                input("\n⚠️  Pilihan tidak valid! Tekan Enter untuk input ulang...")

        if goto_simpan:
            break

        # nama
        while True:
            clear_screen()
            header()
            print("──────────── FORM PENGAJUAN DANA ────────────")
            print(f"Jenis        : {jenis}")
            print(f"Tipe         : {tipe}")
            nama = input("Nama item    : ").strip()

            if nama:
                break
            input("\n⚠️  Nama tidak boleh kosong! Tekan Enter untuk input ulang...")

        # jumlah item
        while True:
            clear_screen()
            header()
            print("──────────── FORM PENGAJUAN DANA ────────────")
            print(f"Jenis        : {jenis}")
            print(f"Tipe         : {tipe}")
            print(f"Nama item    : {nama}")
            jumlah = input("Jumlah       : ").strip()

            if jumlah.isdigit() and int(jumlah) > 0:
                jumlah = int(jumlah)
                break
            input("\n⚠️  Jumlah harus angka > 0! Tekan Enter untuk input ulang...")

        # harga satuan
        while True:
            clear_screen()
            header()
            print("──────────── FORM PENGAJUAN DANA ────────────")
            print(f"Jenis        : {jenis}")
            print(f"Tipe         : {tipe}")
            print(f"Nama item    : {nama}")
            print(f"Jumlah       : {jumlah}")
            harga = input("Harga satuan : ").strip()

            if harga.isdigit() and int(harga) > 0:
                harga = int(harga)
                break
            input("\n⚠️  Harga harus angka > 0! Tekan Enter untuk input ulang...")

        subtotal = jumlah * harga
        total += subtotal

        rincian.append({
            "id_rincian": id_rincian,
            "id_pengajuan": id_pengajuan,
            "tipe": tipe,
            "nama_item": nama,
            "jumlah": jumlah,
            "harga_satuan": harga,
            "subtotal": subtotal
        })

        # tambah item
        clear_screen()
        header()
        tabel_rapih(rincian, "RINCIAN SAAT INI")
        print("\n1. Tambah item")
        print("0. Simpan pengajuan")

        if input("Pilih: ").strip() != "1":
            break

    if not rincian:
        return

    # cek limit
    data_keuangan = baca_data("keuangan")
    limit = data_keuangan.loc[0, "limit_pengajuan"]

    clear_screen()
    header()
    tabel_rapih(rincian, "RINGKASAN PENGAJUAN")
    print(f"\nTOTAL : {format_rupiah(total)}")
    print(f"LIMIT : {format_rupiah(limit)}")

    status = "Menunggu"
    catatan = ""

    # lebih dari limit = dana darurat atau tidak  /farah
    if total > limit:
        print("\n⚠️  Nominal melebihi limit!")
        print("1. Ajukan sebagai DANA DARURAT")
        print("0. Batalkan pengajuan")

        while True:
            pilih = input("Pilih: ").strip()
            if pilih == "1":
                status = "Menunggu (Darurat)"
                catatan = "Melebihi limit"
                break
            elif pilih == "0":
                return
            else:
                input("\n⚠️  Pilihan tidak valid! Tekan Enter...")
    else:
        if input("\nKonfirmasi simpan pengajuan? (y/n): ").lower() != "y":
            return

    # simpan pengajuan dana
    df_pengajuan = pd.concat([
        baca_data("pengajuan"),
        pd.DataFrame([{
            "id_pengajuan": id_pengajuan,
            "tanggal": tanggal,
            "id_kepala_divisi": user["id"],
            "nama_kepala_divisi": user["username"],
            "divisi": user["divisi"],
            "jenis_pengajuan": jenis,
            "status": status,
            "total": total,
            "catatan_manajer": catatan
        }])
    ], ignore_index=True)

    df_rincian = pd.concat([
        baca_data("rincian_pengajuan"),
        pd.DataFrame(rincian)
    ], ignore_index=True)

    simpan_data("pengajuan", df_pengajuan)
    simpan_data("rincian_pengajuan", df_rincian)

    input("\n✅ Pengajuan berhasil diproses! Tekan Enter...")

# riwayat
def riwayat_pengajuan(user):
    clear_screen()
    print("═══════════════════════════════════════════════════════════════════════════════════")
    print("|                                 F U N D G A T E                                 |")
    print("|                       Sistem Pengajuan & Manajemen Keuangan                     |")
    print("═══════════════════════════════════════════════════════════════════════════════════\n")
    print("──────────────────────────────── RIWAYAT PENGAJUAN ────────────────────────────────")

    data = baca_data("pengajuan")
    data = data[data["id_kepala_divisi"] == user["id"]]

    if data.empty:
        input("⚠️  Belum ada pengajuan. Tekan Enter...")
        return

    view = data.copy()
    view["total"] = view["total"].map(format_rupiah)

    tabel_rapih(
        view[["id_pengajuan", "tanggal", "jenis_pengajuan", "total", "status"]],
        "RIWAYAT PENGAJUAN"
    )

    input("\nTekan Enter untuk kembali...")