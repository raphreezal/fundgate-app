import pandas as pd
from datetime import datetime
from modules.data_store import baca_data, simpan_data, tampilkan_interaktif

# ===============================
# MENU KEPALA DIVISI
# ===============================
def menu_kepala_divisi(user_sedang_login):
    while True:
        print(f"\n=== MENU KEPALA DIVISI: {user_sedang_login['divisi']} ===")
        print("1. Buat Pengajuan Dana")
        print("2. Riwayat Pengajuan Dana")
        print("0. Kembali")

        pilihan = input("Pilih menu (0-2): ")

        if pilihan == "1":
            buat_pengajuan_dana(user_sedang_login)
        elif pilihan == "2":
            riwayat_pengajuan(user_sedang_login)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak ada.")


# ===============================
# CREATE PENGAJUAN
# ===============================
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

    id_pengajuan = "REQ-" + datetime.now().strftime("%Y%m%d%H%M%S")
    tanggal = datetime.now().strftime("%Y-%m-%d")

    rincian_list = []
    total = 0

    while True:
        print("\nInput Rincian:")
        print("1. Barang")
        print("2. Jasa")
        tipe = "Barang" if input("Pilih: ") == "1" else "Jasa"

        nama = input("Nama: ")
        jumlah = int(input("Jumlah: "))
        harga = int(input("Harga satuan: "))
        subtotal = jumlah * harga

        total += subtotal

        rincian_list.append({
            "id_pengajuan": id_pengajuan,
            "tipe": tipe,
            "nama_item": nama,
            "jumlah": jumlah,
            "harga_satuan": harga,
            "subtotal": subtotal
        })

        if input("Tambah lagi? (y/n): ").lower() != "y":
            break

    print(f"\nTOTAL PENGAJUAN: Rp{total}")
    if input("Konfirmasi pengajuan? (y/n): ").lower() != "y":
        return

    data_pengajuan = {
        "id_pengajuan": id_pengajuan,
        "tanggal": tanggal,
        "id_kepala_divisi": user["id"],
        "nama_kepala_divisi": user["username"],
        "divisi": user["divisi"],
        "jenis_pengajuan": jenis_pengajuan,
        "status": "Menunggu",
        "total": total,
        "catatan_manajer": ""
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

    print("✅ Pengajuan berhasil dibuat.")


# ===============================
# RIWAYAT + MENU AKSI
# ===============================
def riwayat_pengajuan(user):
    pengajuan = baca_data("pengajuan")
    rincian = baca_data("rincian_pengajuan")

    data = pengajuan[pengajuan["id_kepala_divisi"] == user["id"]]

    if data.empty:
        print("Belum ada pengajuan.")
        return

    print("\n=== RIWAYAT PENGAJUAN ===")
    print(data[["id_pengajuan", "tanggal", "total", "status"]].to_string(index=False))

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


# ===============================
# VIEW DETAIL
# ===============================
def lihat_detail_pengajuan(rincian):
    idp = input("Masukkan ID Pengajuan: ")
    detail = rincian[rincian["id_pengajuan"] == idp]

    if detail.empty:
        print("Detail tidak ditemukan.")
    else:
        # Tampilkan kolom yang penting aja biar gak kepanjangan /mars
        tampilkan_interaktif(data_milik_saya, judul="RIWAYAT PENGAJUAN SAYA")
        print(detail[["tipe","nama_item","jumlah","harga_satuan","subtotal"]])


# ===============================
# EDIT (HANYA STATUS MENUNGGU)
# ===============================
def edit_pengajuan(user, pengajuan, rincian):
    idp = input("ID pengajuan yang diedit: ")

    data = pengajuan[pengajuan["id_pengajuan"] == idp]
    if data.empty:
        print("ID tidak ditemukan.")
        return

    if data.iloc[0]["status"] != "Menunggu":
        print("❌ Pengajuan sudah diproses.")
        return

    rincian = rincian[rincian["id_pengajuan"] != idp]

    total = 0
    rincian_baru = []

    while True:
        tipe = "Barang" if input("1. Barang | 2. Jasa: ") == "1" else "Jasa"
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

    print("✅ Pengajuan berhasil diedit.")


# ===============================
# DELETE
# ===============================
def hapus_pengajuan(user, pengajuan, rincian):
    idp = input("ID pengajuan yang dihapus: ")

    data = pengajuan[pengajuan["id_pengajuan"] == idp]
    if data.empty:
        print("ID tidak ditemukan.")
        return

    if data.iloc[0]["status"] != "Menunggu":
        print("❌ Tidak bisa dihapus.")
        return

    pengajuan = pengajuan[pengajuan["id_pengajuan"] != idp]
    rincian = rincian[rincian["id_pengajuan"] != idp]

    simpan_data("pengajuan", pengajuan)
    simpan_data("rincian_pengajuan", rincian)

    print("🗑️ Pengajuan berhasil dihapus.")
