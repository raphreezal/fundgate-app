import re
from modules.utility import baca_data

# login revisi / najwa
def proses_login(username, password):
    tabel = baca_data("users")

    user = tabel[tabel["username"].str.lower() == username.lower()]
    if user.empty:
        return "USERNAME_TIDAK_ADA"

    if user.iloc[0]["password"] != password:
        return "PASSWORD_SALAH"

    return user.iloc[0].to_dict()

def cek_username(username):
    tabel = baca_data("users")
    if tabel.empty:
        return "USERNAME_TIDAK_ADA"

    if username.lower() not in tabel["username"].str.lower().values:
        return "USERNAME_TIDAK_ADA"

    return "ADA"


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