from modules.utility import baca_data, simpan_data, clear_screen, format_rupiah, tabel_rapih, header

def menu_manajer(user_sedang_login):
    while True:
        clear_screen()
        header()
        print("────────────── KELOLA KEUANGAN ──────────────")
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
        data_pending["total"] = data_pending["total"].map(format_rupiah)
        print("════════════════════════════════════════════════════════════════════════════════════")
        print("|                                 F U N D G A T E                                  |")
        print("|                       Sistem Pengajuan & Manajemen Keuangan                      |")
        print("════════════════════════════════════════════════════════════════════════════════════\n")
        print("──────────────────────────────── DAFTAR PENGAJUAN ──────────────────────────────────")
        tabel_rapih(
            data_pending[["id_pengajuan", "divisi", "jenis_pengajuan", "total", "status"]])

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
        data_pilih = tabel_pengajuan.loc[
            tabel_pengajuan["id_pengajuan"] == id_target
        ].iloc[0]

        total_pengajuan = data_pilih["total"]
        diproses = False
        status_baru = ""
        catatan = ""

        while True:
            clear_screen()
            print("════════════════════════════════════════════════════════")
            print("|                    F U N D G A T E                   |")
            print("|          Sistem Pengajuan & Manajemen Keuangan       |")
            print("════════════════════════════════════════════════════════\n")
            print("────────────────── INFORMASI PENGAJUAN ─────────────────")
            print(f"ID Pengajuan    : {data_pilih['id_pengajuan']}")
            print(f"Divisi          : {data_pilih['divisi']}")
            print(f"Jenis Pengajuan : {data_pilih['jenis_pengajuan']}")
            print(f"Total           : {format_rupiah(data_pilih['total'])}")

            detail = tabel_rincian[tabel_rincian["id_pengajuan"] == id_target]
            # nampilin rincian barang / najwa
            if detail.empty:
                print("Tidak ada rincian barang.")
            else:
                view = detail.copy()
                view["harga_satuan"] = view["harga_satuan"].map(format_rupiah)
                view["subtotal"] = view["subtotal"].map(format_rupiah)
                tabel_rapih(view[["nama_item", "jumlah", "harga_satuan", "subtotal"]])

            print(f"\nSaldo perusahaan saat ini : {format_rupiah(saldo_perusahaan)}")
            print(f"Total pengajuan           : {format_rupiah(total_pengajuan)}") 

            print("1. Setujui")
            print("2. Tolak")
            print("0. Batal")

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
                diproses = True
                break
        # rev nambah alasan penolakan / najwa
            elif keputusan == "2":
                catatan = input("Alasan penolakan: ")
                status_baru = "Ditolak"
                diproses = True
                break
            elif keputusan == "0":
                break
            else:
                print("\n⚠️  Pilihan tidak valid! Silakan pilih tindakan yang tersedia.")
                input("Tekan Enter untuk input ulang...")
        
        if not diproses:
            continue

        # update status pengajuan   /najwa
        tabel_pengajuan.loc[
            tabel_pengajuan["id_pengajuan"] == id_target, "status"
        ] = status_baru

        tabel_pengajuan.loc[
            tabel_pengajuan["id_pengajuan"] == id_target, "catatan_manajer"
        ] = catatan

        simpan_data("pengajuan", tabel_pengajuan)

        # update status rincian
        tabel_rincian.loc[
            tabel_rincian["id_pengajuan"] == id_target, "status_item"
        ] = status_baru

        simpan_data("rincian_pengajuan", tabel_rincian)


        clear_screen()
        print("==== ✅ Pengajuan Berhasil Diproses! ====")
        print(f"ID Pengajuan : {id_target}")
        print(f"Status       : {status_baru}")

        if status_baru == "Ditolak":
            print(f"Catatan      : {catatan}")

        input("\nTekan Enter untuk kembali ke daftar...")

# 2. Fitur Lihat Saldo dan Limit    /farah
def lihat_saldo_dan_limit():
    clear_screen()
    data_keuangan = baca_data("keuangan")

    saldo = data_keuangan.loc[0, "saldo"]
    limit = data_keuangan.loc[0, "limit_pengajuan"]

    header()
    print("──────────── INFORMASI KEUANGAN ─────────────")
    print(f"Saldo perusahaan : {format_rupiah(saldo):>15}")
    print(f"Limit pengajuan  : {format_rupiah(limit):>15}")

# 3. Fitur Set Limit Pengajuan Dana    /farah
def set_limit_pengajuan():
    data_keuangan = baca_data("keuangan")
    
    while True:
        clear_screen()
        header()
        limit = data_keuangan.loc[0, "limit_pengajuan"]
        print("──────────── SET LIMIT PENGAJUAN ────────────")
        print(f"Limit saat ini : {format_rupiah(limit):>15}")
        print("\n1. Set nominal limit baru")
        print("0. Batal / Kembali")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            while True:
                clear_screen()  # clear tiap kali ulang input
                header()
                print("──────────── SET LIMIT PENGAJUAN ────────────")
                print(f"Limit saat ini : {format_rupiah(limit):>15}")
                print("\nMasukkan limit baru (0 untuk batal): ", end="")
                
                inp = input().strip()

                if inp == "0":
                    print("\n❌ Pengaturan limit dibatalkan.")
                    input("Tekan Enter untuk kembali...")
                    break  # kembali ke menu set_limit

                try:
                    limit_baru = int(inp)
                except ValueError:
                    print("\n⚠️  Input harus berupa angka!")
                    input("Tekan Enter untuk input ulang...")
                    continue  # balik ke input awal

                if limit_baru < 0:
                    print("\n⚠️  Limit harus lebih dari 0!")
                    input("Tekan Enter untuk input ulang...")
                    continue  # balik ke input awal

                # update limit
                data_keuangan.loc[0, "limit_pengajuan"] = limit_baru
                simpan_data("keuangan", data_keuangan)
                print(f"\n✅ Limit berhasil diperbarui menjadi {format_rupiah(limit_baru)}")
                input("Tekan Enter untuk kembali...")
                return  # selesai

        elif pilihan == "0":
            return  # kembali ke menu sebelumnya
        else:
            print("\n⚠️  Pilihan tidak valid! Silakan pilih menu yang tersedia.")
            input("Tekan Enter untuk input ulang...")
