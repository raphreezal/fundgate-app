from modules.utility import siapkan_folder_dan_file, clear_screen, header
from modules.auth import proses_login, cek_username
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
        
        # login revisi (max 3 kali percobaan) / najwa
        maks_login = 3
        percobaan = 0
        data_user = None

        while percobaan < maks_login:
            clear_screen()
            header()
            
            while True:
                print("────────────────── LOGIN ────────────────────\n")
                username = input("Username : ").strip()
                if not username:
                    print("⚠️   Username tidak boleh kosong!")
                    input("Tekan Enter untuk input ulang...\n")
                    clear_screen()
                    header()
                    continue

                hasil_username = cek_username(username)
                if hasil_username == "USERNAME_TIDAK_ADA":
                    print("⚠️   Username tidak terdaftar!")
                    input("Tekan Enter untuk input ulang...\n")
                    clear_screen()
                    header()
                    continue
                else:
                    print("✅ Username terdaftar")
                    input("Tekan Enter untuk melanjutkan...\n")
                    break 

            while True:
                password = input("Password : ").strip()
                if not password:
                    print("⚠️   Password tidak boleh kosong!")
                    input("Tekan Enter untuk input ulang...\n")
                    continue 

                hasil = proses_login(username, password)
                if isinstance(hasil, dict):
                    data_user = hasil
                    break  
                elif hasil == "PASSWORD_SALAH":
                    percobaan += 1

                    if percobaan >= maks_login:
                        print("❌ Login Gagal! Percobaan login sudah habis (3 kali).")
                        print("Program dihentikan.")
                        exit()

                    print("⚠️   Password salah!")
                    print(f"Sisa percobaan: {maks_login - percobaan}")
                    input("Tekan Enter untuk input ulang...\n")

            if data_user is not None:
                break 

        if data_user is None:
            print("Gagal! Username atau Password salah.")
        else:
            # kalau berhasil login, cek rolenya siapa /kei
            nama = data_user['username']
            peran = data_user['role']
            # print(f"\n===== ✅  Login Sukses! Halo, {nama} ({peran}) =====")
            
            # 3. arahin ke menu sesuai peran (Role) /kei
            if peran == "Kepala Divisi":
                # panggil fungsi buatan mars /kei
                menu_kepala_divisi(data_user)
            
            elif peran == "Manajer Keuangan":
                while True:
                    clear_screen()
                    # manajer punya akses spesial ke menu admin juga /kei

                    header()
                    print(f"Selamat datang, {nama}! \nAnda masuk sebagai {peran}.\n") # nambah info usn sama role / najwa
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
                        print("\n⚠️    Pilihan tidak valid!")
                        input("Tekan Enter untuk input ulang...\n")

            elif peran in ("Direktur", "Auditor"):
                menu_laporan(data_user)

            else:
                print("⚠️    Role tidak dikenali.")
        
            # kalau loop menu selesai (user pilih logout), tanya mau keluar aplikasi gak? /kei
            lagi = input("\nApakah ada user lain yang mau login? (y/n): ")
            if lagi.lower() != 'y':
                print("Terima kasih, sampai jumpa!")
                break

if __name__ == "__main__":
    main()