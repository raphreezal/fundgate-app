from modules.utility import siapkan_folder_dan_file, clear_screen, header
from modules.auth import proses_login, cek_username  
from modules.staff_ops import menu_kepala_divisi
from modules.manager_ops import menu_manajer
from modules.admin_ops import menu_admin
from modules.report import menu_laporan
from modules.divisi_ops import menu_divisi

# funsi konfirmasi inputan / najwa
def konfirmasi_yn(pesan):
    while True:
        clear_screen()
        header()
        jawab = input(pesan).strip().lower()
        if jawab in ("y", "n"):
            return jawab
        print("\n⚠️  Input tidak valid! Harus y atau n.")
        input("Tekan Enter untuk input ulang...")

def main():
    # 1. pastiin database siap dulu sebelum aplikasi mulai /kei
    siapkan_folder_dan_file()
    while True:
        # login revisi (max 3 kali percobaan)   /najwa
        maks_login = 3
        percobaan = 0
        data_user = None
        username_terakhir = ""

        while percobaan < maks_login:
            clear_screen()
            header()
            print("    Selamat datang di Aplikasi FundGate !\n")
            print("────────────────── LOGIN ────────────────────\n")

            # username
            if username_terakhir:
                print(f"Username : {username_terakhir}")
                username = username_terakhir
            else:
                username = input("Username : ").strip()

            if not username:
                print("\n⚠️  Username tidak boleh kosong!")
                input("Tekan Enter untuk input ulang...")
                continue

            hasil_username = cek_username(username)
            if hasil_username == "USERNAME_TIDAK_ADA":
                print("\n⚠️  Username tidak terdaftar!")
                input("Tekan Enter untuk input ulang...")
                username_terakhir = ""
                continue

            username_terakhir = username

            # password
            password = input("Password : ").strip()
            if not password:
                print("\n⚠️  Password tidak boleh kosong!")
                input("Tekan Enter untuk input ulang...")
                continue

            hasil = proses_login(username_terakhir, password)

            if isinstance(hasil, dict):
                data_user = hasil
                break

            elif hasil == "PASSWORD_SALAH":
                percobaan += 1
                print("\n⚠️  Password salah!")
                print(f"Sisa percobaan: {maks_login - percobaan}")
                input("Tekan Enter untuk input ulang...")

        if data_user is None:
            print("\n⚠️  Login gagal. Program dihentikan.")
            break

        # login berhasil, cek role  /kei
        nama = data_user["username"]
        peran = data_user["role"]
        # arahin menu sesuai role   /kei
        if peran == "Kepala Divisi":
            menu_kepala_divisi(data_user)

        elif peran == "Manajer Keuangan":
            while True:
                clear_screen()
                header()
                print(f"Selamat datang, {nama}!")
                print(f"Anda masuk sebagai {peran}\n")  # nambah info usn sama role /najwa
                print("──────────── MENU UTAMA ────────────")   # menu manajer keuangan /farah
                print("1. 💰 Kelola Keuangan")
                print("2. 👤 Kelola User")
                print("3. 👥 Kelola Divisi")
                print("4. 📊 Lihat Laporan")
                print("0. 🔒 Logout")

                opsi = input("Pilih: ").strip()

                if opsi == "1":
                    menu_manajer(data_user)
                elif opsi == "2":
                    menu_admin(data_user)   # manajer punya akses spesial ke menu admin juga    /kei
                elif opsi == "3":
                    menu_divisi(data_user)
                elif opsi == "4":
                    menu_laporan(data_user)
                elif opsi == "0":
                    if konfirmasi_yn("\nYakin ingin logout? (y/n): ") == "y":
                        break
                else:
                    print("\n⚠️  Pilihan tidak valid!")
                    input("Tekan Enter untuk input ulang...")

        elif peran in ("Direktur", "Auditor"):
            menu_laporan(data_user)

        else:
            print("\n⚠️  Role tidak dikenali.")

        # loop menu selesai, tanya mau keluar aplikasi gak? /kei
        # updated  /najwa
        if konfirmasi_yn("\nApakah ada user lain yang mau login? (y/n): ") == "y":
            continue
        else:
            print("\nTerima kasih, sampai jumpa!")
            break


if __name__ == "__main__":
    main()