import re
from modules.utility import baca_data

# validasi password / najwa
def validasi_password(password):
    if len(password) < 8:
        return False, "Password minimal 8 karakter!"
    if not re.search(r"[A-Z]", password):
        return False, "Password harus mengandung huruf kapital!"
    if not re.search(r"[a-z]", password):
        return False, "Password harus mengandung huruf kecil!"
    if not re.search(r"[0-9]", password):
        return False, "Password harus mengandung angka!"
    
    simbol = "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|"
    punya_simbol = False
    for char in password:
        if char in simbol:
            punya_simbol = True
            break
    
    if not punya_simbol:
        return False, "Password harus mengandung simbol!"
    
    return True, "Valid"

# login revisi / najwa
def proses_login(username_input, password_input):
    tabel_users = baca_data("users")
    list_user = tabel_users.to_dict("records")

    for user in list_user:
        if user["username"] == username_input:
            if user["password"] == password_input:
                return user
            else:
                print("❌ Password salah!")
                return None

    print("❌ Username tidak terdaftar!")
    return None



# def proses_login(username_input, password_input):
#     # Ambil data dari CSV / najwa
#     tabel_users = baca_data("users")
#     username_input = username_input.lower()
#     list_user = tabel_users.to_dict('records') 
    
#     user_ditemukan = None
    
#     # Linear Search untuk cari username / najwa
#     for user in list_user:
#         if str(user['username']).lower() == username_input:
#             user_ditemukan = user
#             break 

#     if user_ditemukan is None:
#         print("Username salah atau tidak terdaftar!")
#         return None
#     else:
#         if str(user_ditemukan['password']) == password_input:
#             return user_ditemukan 
#         else:
#             print("Password salah!")
#             return None