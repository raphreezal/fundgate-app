from modules.utility import siapkan_folder_dan_file, clear_screen
from modules.auth import proses_login
from modules.staff_ops import menu_kepala_divisi
from modules.manager_ops import menu_manajer
from modules.admin_ops import menu_admin
from modules.report import menu_laporan

def main():
    # 1. pastiin database siap dulu sebelum aplikasi mulai /kei
    siapkan_folder_dan_file()

    print("\n========================================")
    print(" SELAMAT DATANG DI APLIKASI FUNDGATE ")
    print("========================================")
    
    while True:
        # 2. minta login /kei
        print("\nSilakan Login Terlebih Dahulu")
        
        # validasi username / najwa 
        while True:
            input_user = input("Username : ").strip()
            if not input_user:
                print("Username tidak boleh kosong!")
            else:
                break
        
        # validasi password / najwa
        while True:
            input_pass = input("Password : ").strip()
            if not input_pass:
                print("Password tidak boleh kosong!")
            else:
                break
        
        # panggil fungsi buatan Najwa /kei
        # disini
        data_user = proses_login(input_user, input_pass)

        if data_user is None:
            print("Gagal! Username atau Password salah.")
        else:
            # kalau berhasil login, cek rolenya siapa /kei
            nama = data_user['username']
            peran = data_user['role']
            print(f"\nLogin Sukses! Halo, {nama} ({peran})")
            
            # 3. arahin ke menu sesuai peran (Role) /kei
            if peran == "kepala_divisi":
                # panggil fungsi buatan mars /kei
                # disini
                menu_kepala_divisi(data_user)
            
            elif peran == "manajer_keuangan":
                while True:
                    clear_screen()
                # manajer punya akses spesial ke menu admin juga /kei
                    print("==== MENU UTAMA MANAJER ====")
                    print("1. Kelola Keuangan")
                    print("2. Kelola User")
                    print("3. Lihat Laporan")
                    print("0. Logout")

                    opsi = input("Pilih: ").strip()

                    if opsi == "1":
                        menu_manajer(data_user)

                    elif opsi == "2":
                        menu_admin(data_user)

                    elif opsi == "3":
                        menu_laporan(data_user)

                    elif opsi == "0":
                        break

                    else:
                        print("\n⚠️  Pilihan tidak valid!")
                        input("Tekan Enter untuk input ulang...")

            elif peran in ("direktur", "auditor"):
                menu_laporan(data_user)

            else:
                print("⚠️ Role tidak dikenali.")
        
            # kalau loop menu selesai (user pilih logout), tanya mau keluar aplikasi gak? /kei
            lagi = input("\nApakah ada user lain yang mau login? (y/n): ")
            if lagi.lower() != 'y':
                print("Terima kasih, sampai jumpa!")
                break

if __name__ == "__main__":
    main()