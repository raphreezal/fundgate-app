from modules.utility import baca_data, simpan_data, clear_screen, format_rupiah, tabel_rapih

def menu_manajer(user_sedang_login):
    while True:
        clear_screen()
        print("======== KELOLA KEUANGAN ========")
        print("1. Cek & Proses Pengajuan Dana")
        print("2. Lihat Saldo & Limit")
        print("3. Set Limit Pengajuan")
        print("0. Kembali")

        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            proses_persetujuan_dana()
        elif pilihan == "2":
            lihat_saldo_dan_limit()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == "3":
            set_limit_pengajuan()
        elif pilihan == "0":
            return
        else:
            print("\n⚠️  Pilihan tidak valid! Silakan pilih menu yang tersedia.")
            input("Tekan Enter untuk input ulang...")

# 1. Fitur Persetujuan dan Penolakan Pengajuan Dana    /farah
def proses_persetujuan_dana():
    while True:
        clear_screen()
        tabel_pengajuan = baca_data("pengajuan")
        tabel_rincian = baca_data("rincian_pengajuan") # nambah rincian barang / najwa
        data_keuangan = baca_data("keuangan") # Baca data keuangan

        # ambil saldo saat ini /kei
        saldo_perusahaan = data_keuangan.loc[0, "saldo"]

        # Mencari data pengajuan dana   /farah
        data_pending = tabel_pengajuan[tabel_pengajuan["status"] == "Menunggu"].copy() # copy biar gak warning
    
        # Pengajuan kosong     /farah
        if data_pending.empty:
            print("\nTidak ada pengajuan yang perlu diproses.")
            input("Tekan Enter untuk kembali...")
            return
    
        # Pengajuan ada        /farah
        data_pending["total"] = data_pending["total"].map(format_rupiah) # format rupiah biar enak diliat /kei
        tabel_rapih(
            data_pending[["id_pengajuan", "divisi", "jenis_pengajuan", "total", "status"]],
            judul="DAFTAR PENGAJUAN" # judul tabel /kei
        )

        id_target = input("\nMasukkan ID Pengajuan yang ingin diproses (0 untuk kembali): ").strip()

        # ID pengajuan       /farah
        if id_target == "0":
            return
        if not id_target:
            print("\n⚠️  ID tidak boleh kosong!")
            input("Tekan Enter untuk input ulang...")
            continue
        if id_target not in data_pending["id_pengajuan"].astype(str).values:
            print("\n⚠️  ID tidak ditemukan atau tidak berstatus Menunggu!")
            input("Tekan Enter untuk input ulang...")
            continue

        # info detail pengajuan / najwa
        clear_screen()
        data_pilih = tabel_pengajuan.loc[
            tabel_pengajuan["id_pengajuan"] == id_target
        ].iloc[0]

        print("\n======== INFORMASI PENGAJUAN ========")
        print(f"ID Pengajuan    : {data_pilih['id_pengajuan']}")
        print(f"Divisi          : {data_pilih['divisi']}")
        print(f"Jenis Pengajuan : {data_pilih['jenis_pengajuan']}")
        print(f"Total           : {format_rupiah(data_pilih['total'])}")
    
        # nampilin rincian barang / najwa
        detail = tabel_rincian[tabel_rincian["id_pengajuan"] == id_target]

        print("\n======== RINCIAN BARANG / JASA ========")
        if detail.empty:
            print("Tidak ada rincian barang.")
        else:
            detail_view = detail.copy()
            detail_view["harga_satuan"] = detail_view["harga_satuan"].map(format_rupiah)
            detail_view["subtotal"] = detail_view["subtotal"].map(format_rupiah)
            tabel_rapih(detail_view[["nama_item", "jumlah", "harga_satuan", "subtotal"]])

        # print(
        #     detail_view[
        #         ["nama_item", "jumlah", "harga_satuan", "subtotal"]
        #     ].to_string(index=False)
        # )

        input("\nTekan Enter untuk lanjut ke keputusan...")

        # ambil info nominal pengajuan tersebut /kei
        # rev / najwa
        total_pengajuan = data_pilih["total"] # ambil nominal sebelum di format /kei
     
        print(f"Saldo perusahaan saat ini : {format_rupiah(saldo_perusahaan)}")
        print(f"Total pengajuan           : {format_rupiah(total_pengajuan)}") 

        print("\n1. Setujui")
        print("2. Tolak")
        print("0. Batal")

        while True:
            keputusan = input("Pilih tindakan: ").strip()
        
            if keputusan == "1":
                if saldo_perusahaan < total_pengajuan:
                    kurang = total_pengajuan - saldo_perusahaan
                    print(f"⚠️ Saldo tidak cukup (kurang {format_rupiah(kurang)})")
                    input("Tekan Enter untuk pilih tindakan lain...")
                    continue

                data_keuangan.loc[0, "saldo"] -= total_pengajuan
                simpan_data("keuangan", data_keuangan)
                status_baru = "Disetujui"
                catatan = ""
                break
        # rev nambah alasan penolakan / najwa
            elif keputusan == "2":
                status_baru = "Ditolak"
                catatan = input("Alasan penolakan: ")
                break
            elif keputusan == "0":
                print("===== Proses dibatalkan ====")
                return
            else:
                print("⚠️  Pilihan tidak valid! Silakan pilih menu yang tersedia.")

    # update status pengajuan   /najwa
    tabel_pengajuan.loc[
        tabel_pengajuan["id_pengajuan"] == id_target, "status"
    ] = status_baru

    tabel_pengajuan.loc[
        tabel_pengajuan["id_pengajuan"] == id_target, "catatan_manajer"
    ] = catatan

    simpan_data("pengajuan", tabel_pengajuan)

    print(f"\nSukses! Pengajuan {id_target} telah {status_baru}.")

# 2. Fitur Lihat Saldo dan Limit    /farah
def lihat_saldo_dan_limit():
    clear_screen()
    data_keuangan = baca_data("keuangan")

    saldo = data_keuangan.loc[0, "saldo"]
    limit = data_keuangan.loc[0, "limit_pengajuan"]

    print("======== INFORMASI KEUANGAN ========")
    print(f"Saldo perusahaan : {format_rupiah(saldo):>15}")
    print(f"Limit pengajuan  : {format_rupiah(limit):>15}")

# 3. Fitur Set Limit Pengajuan Dana    /farah
def set_limit_pengajuan():
    while True:
        clear_screen()
        data_keuangan = baca_data("keuangan")
        limit = data_keuangan.loc[0, "limit_pengajuan"]

        print("======== SET LIMIT PENGAJUAN ========")
        print(f"Limit saat ini : {format_rupiah(limit):>15}")
        print("\n1. Set nominal limit baru")
        print("0. Batal / Kembali")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            while True:
                clear_screen()
                print("======== SET LIMIT PENGAJUAN ========")
                print(f"Limit saat ini : {format_rupiah(limit):>15}")
                print("\nMasukkan limit baru (0 untuk batal) :")

                try:
                    limit_baru = int(input("Limit baru: ").strip())
                except ValueError:
                    print("\n⚠️  Input harus berupa angka.")
                    input("Enter untuk coba lagi...")
                    continue

                if limit_baru == 0:
                    break

                if limit_baru < 0:
                    print("\n⚠️  Limit harus lebih dari 0.")
                    input("Enter untuk coba lagi...")
                    continue

                data_keuangan.loc[0, "limit_pengajuan"] = limit_baru
                simpan_data("keuangan", data_keuangan)

                print("\n✅ Limit pengajuan berhasil diperbarui.")
                input("Tekan Enter untuk kembali...")
                return

        elif pilihan == "0":
            return

        else:
            print("\n⚠️  Pilihan tidak valid!")
            input("Tekan Enter untuk pilih ulang...")