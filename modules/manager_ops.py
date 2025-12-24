from modules.data_store import baca_data, simpan_data


def menu_manajer(user_sedang_login):
    while True:
        print("\n======== MENU ========")
        print("1. Cek Pengajuan Dana")
        print("0. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            proses_persetujuan_dana()
        elif pilihan == "0":
            print("Log out berhasil. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid!")


def proses_persetujuan_dana():
    tabel_pengajuan = baca_data("pengajuan")

    # Mencari data pengajuan dana   /farah
    data_pending = tabel_pengajuan[tabel_pengajuan["status"] == "Menunggu"]
    # Pengajuan kosong     /farah
    if data_pending.empty:
        print("\nTidak ada pengajuan yang perlu diproses.")
        return
    # Pengajuan ada        /farah
    print("\n-------- DAFTAR PENGAJUAN --------")
    print(
        data_pending[
            ["id", "divisi", "nominal", "kategori"]
        ].to_string(index=False)
    )

    id_target = input("\nMasukkan Kode Pengajuan: ")

    # Kode pengajuan       /farah
    if id_target not in data_pending["id"].values:
        print("Kode tidak ditemukan di pengajuan atau sudah diproses.")
        return
    # Keputusan pengajuan  /farah
    while True:
        print("\n1. Setujui")
        print("2. Tolak")
        print("0. Batal")

        keputusan = input("Pilih: ")

        if keputusan == "1":
            status_baru = "Disetujui"
            break
        elif keputusan == "2":
            status_baru = "Ditolak"
            break
        elif keputusan == "0":
            print("Proses persetujuan dibatalkan.")
            return
        else:
            print("Input tidak valid. Silakan pilih 1, 2, atau 0.")

    # Update status pengajuan   /farah
    tabel_pengajuan.loc[
        tabel_pengajuan['id'] == id_target,
        'status'
    ] = status_baru

    simpan_data("pengajuan", tabel_pengajuan)

    print(f"\nPengajuan {id_target} berhasil diproses.")
    print(f"Status pengajuan terbaru: {status_baru}")
