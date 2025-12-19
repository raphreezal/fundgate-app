import re
from file_handler import baca_csv, tambah_csv

# VALIDASI PASSWORD
def validasi_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[\W_]", password):
        return False
    return True

# LOGIN
def login(username, password):
    files = [
        "manajer_keuangan.csv",
        "kepala_divisi.csv",
        "direktur.csv",
        "auditor.csv"
    ]

    for file in files:
        users = baca_csv(file)
        for user in users:
            if user['username'].strip() == username.strip() and user['password'] == password:
                return user

    print("Username atau password salah")
    return None

# REGISTER USER (ADMIN)
def register_user(nama_file, data):
    if not validasi_password(data['password']):
        print("Password minimal 8 karakter, huruf besar, kecil, angka, dan simbol")
        return

    tambah_csv(nama_file, data.keys(), data)
    print("User berhasil ditambahkan")