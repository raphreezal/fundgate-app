import re
from modules.utility import baca_data

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
