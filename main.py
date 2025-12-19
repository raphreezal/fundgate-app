
from modules.data_store import siapkan_folder_dan_file
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
        input_user = input("Username : ")
        input_pass = input("Password : ")
        
        # panggil fungsi buatan Najwa /kei
        # disini
        data_user = proses_login(input_user, input_pass)

        data_user = []
        if data_user is None:
            print("Gagal! Username atau Password salah.")
        else:
            # kalau berhasil login, cek rolenya siapa /kei
            nama = data_user['username']
            peran = data_user['role']
            print(f"Login Sukses! Halo, {nama} ({peran})")
            
            # 3. arahin ke menu sesuai peran (Role) /kei
            if peran == "kepala_divisi":
                # panggil fungsi buatan mars /kei
                # disini
                menu_kepala_divisi(data_user)
            
            elif peran == "manajer_keuangan":
                # manajer punya akses spesial ke menu admin juga /kei
                while True:
                    print("\n--- MENU UTAMA MANAJER ---")
                    print("1. Kelola Keuangan")
                    print("2. Kelola User (Admin)")
                    print("3. Lihat Laporan")
                    print("0. Logout")
                    opsi = input("Pilih: ")
                    
                    if opsi == "1": 
                        menu_manajer(data_user)
                    elif opsi == "2": 
                        menu_admin(data_user)
                    elif opsi == "3": 
                        menu_laporan(data_user)
                    elif opsi == "0": 
                        break
            
            elif peran == "direktur" or peran == "auditor":
                menu_laporan(data_user)
                
            else:
                print("Role tidak dikenali.")

            # kalau loop menu selesai (user pilih logout), tanya mau keluar aplikasi gak? /kei
            lagi = input("\nApakah ada user lain yang mau login? (y/n): ")
            if lagi.lower() != 'y':
                print("Terima kasih, sampai jumpa!")
                break

if __name__ == "__main__":
    main()