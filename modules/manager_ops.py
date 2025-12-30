from modules.data_store import baca_data, simpan_data


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
            print("Log out berhasil. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid!")

# 1. Fitur Persetujuan dan Penolakan Pengajuan Dana    /farah
def proses_persetujuan_dana():
    tabel_pengajuan = baca_data("pengajuan")
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
    print("\n-------- DAFTAR PENGAJUAN --------")

    # tampilkan kolom ID, divisi, nominal biar jelas /kei
    print(data_pending[["id", "divisi", "kategori", "nominal"]].to_string(index=False))

    id_target = input("\nMasukkan ID Pengajuan yang ingin diproses: ")

    # Kode pengajuan       /farah
    if id_target not in data_pending["id"].values:
        print("ID tidak ditemukan atau status bukan Menunggu.")
        return

    # Keputusan pengajuan  /farah
    # ambil info nominal pengajuan tersebut /kei
    nominal_pengajuan = tabel_pengajuan.loc[tabel_pengajuan["id"] == id_target, "nominal"].values[0]

    print(f"\nPengajuan: {id_target} | Nominal: Rp{nominal_pengajuan}")
    print(f"Saldo Perusahaan Saat Ini: Rp{saldo_perusahaan}")

    print("1. Setujui")
    print("2. Tolak")
    print("0. Batal")
    
    while True:
        keputusan = input("Pilih tindakan: ")
        
        if keputusan == "1":
            status_baru = "Disetujui"
            break
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
    tabel_pengajuan.loc[tabel_pengajuan["id"] == id_target, "status"] = status_baru
    tabel_pengajuan.loc[tabel_pengajuan["id"] == id_target, "catatan_manajer"] = catatan

    simpan_data("pengajuan", tabel_pengajuan)

    print(f"\nSukses! Pengajuan {id_target} telah {status_baru}.")

# 2. Fitur Lihat Saldo dan Limit    /farah
def lihat_saldo_dan_limit():
    data_keuangan = baca_data("keuangan")

    saldo = data_keuangan.loc[0, "saldo"]
    limit = data_keuangan.loc[0, "limit_pengajuan"]

    print("\n===== INFORMASI KEUANGAN =====")
    print(f"Saldo perusahaan : Rp{saldo}")
    print(f"Limit pengajuan  : Rp{limit}")


# 3. Fitur Set Limit Pengajuan Dana    /farah
def set_limit_pengajuan():
    data_keuangan = baca_data("keuangan")

    print("\n===== SET LIMIT PENGAJUAN =====")
    print(f"Limit saat ini : Rp{data_keuangan.loc[0, 'limit_pengajuan']}")

    try:
        limit_baru = int(input("Masukkan limit baru: "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    if limit_baru <= 0:

        print("Limit harus lebih dari 0.")
        return

    data_keuangan.loc[0, "limit_pengajuan"] = limit_baru
    simpan_data("keuangan", data_keuangan)

    print("Limit pengajuan berhasil diperbarui.")