from modules.utility import siapkan_folder_dan_file, clear_screen, header
from modules.auth import proses_login
from modules.staff_ops import menu_kepala_divisi
from modules.manager_ops import menu_manajer
from modules.admin_ops import menu_admin
from modules.report import menu_laporan
from modules.divisi_ops import menu_divisi


def main():
    # 1. pastiin database siap dulu sebelum aplikasi mulai /kei
    siapkan_folder_dan_file()
    clear_screen()
    header()
    print("     Selamat Datang di Aplikasi FundGate!")
    
    while True:
        print("\n────────────────── LOGIN ────────────────────")
        
        # validasi username / najwa 
        # while True:
        #     input_user = input("Username : ").strip()
        #     if not input_user:
        #         print("Username tidak boleh kosong!")
        #     else:
        #         break
        
        # # validasi password / najwa
        # while True:
        #     input_pass = input("Password : ").strip()
        #     if not input_pass:
        #         print("Password tidak boleh kosong!")
        #     else:
        #         break
        
        # login revisi (max 3 kali percobaan) / najwa
        maks_login = 3
        percobaan = 0

        while percobaan < maks_login:
            clear_screen()
            header()
            print("────────────────── LOGIN ────────────────────")

            # input usn / najwa
            username = input("Username : ").strip()
            if not username:
                print("❌ Username tidak boleh kosong!")
                input("Enter...")
                continue

            # cek usn / najwa
            hasil_username = proses_login(username, None)

            if hasil_username == "USERNAME_TIDAK_ADA":
                print("❌ Username tidak terdaftar!")
                percobaan += 1
                print(f"Sisa percobaan: {maks_login - percobaan}")
                input("Enter...")
                continue

            # input pw / najwa
            password = input("Password : ").strip()
            if not password:
                print("❌ Password tidak boleh kosong!")
                input("Enter...")
                continue

            # cek pw / najwa
            hasil = proses_login(username, password)

            if isinstance(hasil, dict):
                data_user = hasil
                break
            elif hasil == "PASSWORD_SALAH":
                print("❌ Password salah!")
                percobaan += 1
                print(f"Sisa percobaan: {maks_login - percobaan}")
                input("Enter...")



        if percobaan == maks_login:
            print("❌ Login gagal 3 kali. Program dihentikan.")
            exit()


        if data_user is None:
            print("Gagal! Username atau Password salah.")
        else:
            # kalau berhasil login, cek rolenya siapa /kei
            nama = data_user['username']
            peran = data_user['role']
            print(f"\n===== ✅  Login Sukses! Halo, {nama} ({peran}) =====")
            
            # 3. arahin ke menu sesuai peran (Role) /kei
            if peran == "kepala_divisi":
                # panggil fungsi buatan mars /kei
                # disini
                menu_kepala_divisi(data_user)
            
            elif peran == "manajer_keuangan":
                while True:
                    clear_screen()
                # manajer punya akses spesial ke menu admin juga /kei

                    header()
                    print("──────────────── MENU UTAMA ─────────────────") # punya manajer keuangan /farah
                    print("1. 💰 Kelola Keuangan")
                    print("2. 👤 Kelola User")
                    print("3. 👥 Kelola Divisi")
                    print("4. 📊 Lihat Laporan")
                    print("0. 🔒 Logout")

                    opsi = input("Pilih: ").strip()

                    if opsi == "1":
                        menu_manajer(data_user)

                    elif opsi == "2":
                        menu_admin(data_user)
                    
                    #nambah menu kelola divisi / najwa
                    elif opsi == "3":
                        menu_divisi(data_user)

                    elif opsi == "4":
                        menu_laporan(data_user)

                    elif opsi == "0":
                        break

                    else:
                        print("\n⚠️  Pilihan tidak valid!")
                        input("Tekan Enter untuk input ulang...")

            elif peran in ("direktur", "auditor"):
                menu_laporan(data_user)

            else:
                print("⚠️  Role tidak dikenali.")
        
            # kalau loop menu selesai (user pilih logout), tanya mau keluar aplikasi gak? /kei
            lagi = input("\nApakah ada user lain yang mau login? (y/n): ")
            if lagi.lower() != 'y':
                print("Terima kasih, sampai jumpa!")
                break

if __name__ == "__main__":
    main()