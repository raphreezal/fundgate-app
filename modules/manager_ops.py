from modules.data_store import baca_data, simpan_data, clear_screen

def menu_manajer(user_sedang_login):
    while True:
        print("\n======== KELOLA KEUANGAN ========")
        print("1. Cek & Proses Pengajuan Dana")
        print("2. Lihat Saldo & Limit")
        print("3. Set Limit Pengajuan")
        print("0. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            proses_persetujuan_dana()
        elif pilihan == "2":
            lihat_saldo_dan_limit()
        elif pilihan == "3":
            set_limit_pengajuan()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang tersedia.")

# 1. Fitur Persetujuan dan Penolakan Pengajuan Dana    /farah
def proses_persetujuan_dana():
    tabel_pengajuan = baca_data("pengajuan")
    tabel_rincian = baca_data("rincian_pengajuan") # nambah rincian barang / najwa
    data_keuangan = baca_data("keuangan") # Baca data keuangan

    # ambil saldo saat ini /kei
    saldo_perusahaan = data_keuangan.loc[0, "saldo"]

    # Mencari data pengajuan dana   /farah
    data_pending = tabel_pengajuan[tabel_pengajuan["status"] == "Menunggu"]
    
    # Pengajuan kosong     /farah
    if data_pending.empty:
        print("\nTidak ada pengajuan yang perlu diproses.")
        return
    
    # Pengajuan ada        /farah
    print("\n======== DAFTAR PENGAJUAN ========")

    # tampilkan kolom ID, divisi, nominal biar jelas /kei
    print(data_pending[["id_pengajuan", "divisi", "jenis_pengajuan", "total", "status"]].to_string(index=False))

    id_target = input("\nMasukkan ID Pengajuan yang ingin diproses: ")

    # Kode pengajuan       /farah
    if id_target not in data_pending["id_pengajuan"].values:
        print("ID tidak ditemukan atau status bukan Menunggu.")
        return
    
    # info detail pengajuan / najwa
    data_pilih = tabel_pengajuan[
        tabel_pengajuan["id_pengajuan"] == id_target
    ].iloc[0]

    print("\n======== INFORMASI PENGAJUAN ========")
    print(f"ID Pengajuan    : {data_pilih['id_pengajuan']}")
    print(f"Divisi          : {data_pilih['divisi']}")
    print(f"Jenis Pengajuan : {data_pilih['jenis_pengajuan']}")
    print(f"Total           : Rp{data_pilih['total']}")
    
    # nampilin rincian barang / najwa
    detail = tabel_rincian[tabel_rincian["id_pengajuan"] == id_target]

    print("\n======== RINCIAN BARANG / JASA ========")
    if detail.empty:
        print("Tidak ada rincian barang.")
    else:
        print(
            detail[
                ["nama_item", "jumlah", "harga_satuan", "subtotal"]
            ].to_string(index=False)
        )

    input("\nTekan ENTER untuk lanjut ke persetujuan...")

    # Keputusan pengajuan  /farah
    # ambil info nominal pengajuan tersebut /kei
    # rev / najwa
    total_pengajuan = tabel_pengajuan.loc[
        tabel_pengajuan["id_pengajuan"] == id_target, "total"
    ].values[0]

    print(f"\nTotal Pengajuan : Rp{total_pengajuan}")
    print(f"Saldo Perusahaan Saat Ini  : Rp{saldo_perusahaan}")


    print("1. Setujui")
    print("2. Tolak")
    print("0. Batal")

    catatan = ""
    
    while True:
        keputusan = input("Pilih tindakan: ")
        
        if keputusan == "1":
            # --- LOGIKA POTONG SALDO ---
            if saldo_perusahaan >= total_pengajuan:
                status_baru = "Disetujui"
                # Kurangi saldo
                data_keuangan.loc[0, "saldo"] = saldo_perusahaan - total_pengajuan
                simpan_data("keuangan", data_keuangan) # Simpan saldo baru
                print("Saldo berhasil dikurangi.")
                break
            else:
                print(f"GAGAL: Saldo perusahaan tidak cukup! (Kurang Rp{total_pengajuan: - saldo_perusahaan})")
                return # Keluar fungsi
        
        # rev nambah alasan penolakan / najwa
        elif keputusan == "2":
            status_baru = "Ditolak"
            catatan = input("Alasan penolakan: ")
            break
        elif keputusan == "0":
            print("Proses dibatalkan.")
            return
        else:
            print("Pilihan salah.")

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

    print("\n======== INFORMASI KEUANGAN ========")
    print(f"Saldo perusahaan : Rp{saldo}")
    print(f"Limit pengajuan  : Rp{limit}")


# 3. Fitur Set Limit Pengajuan Dana    /farah
def set_limit_pengajuan():
    while True:
        data_keuangan = baca_data("keuangan")

        print("\n======== SET LIMIT PENGAJUAN ========")
        print(f"Limit saat ini :       Rp{data_keuangan.loc[0, 'limit_pengajuan']}")
        print("\n1. Set nominal limit baru")
        print("0. Batal / Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            while True:
                try:
                    limit_baru = int(input("\nMasukkan limit baru: "))
                except ValueError:
                    print("❌ Input harus berupa angka. Coba lagi! ")
                    continue

                if limit_baru <= 0:
                    print("❌ Limit harus lebih dari 0. Coba lagi!")
                    continue

                data_keuangan.loc[0, "limit_pengajuan"] = limit_baru
                simpan_data("keuangan", data_keuangan)

                print("\n✅ Limit pengajuan berhasil diperbarui.")
                return

        elif pilihan == "0":
            return

        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih menu yang tersedia.")
