import csv, os
DATA_PATH = "data/"

def baca_csv(nama_file):
    path = DATA_PATH + nama_file
    data = []
    if not os.path.exists(path):
        return data
    with open(path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def tulis_csv(nama_file, fieldnames, data):
    path = DATA_PATH + nama_file
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()
        writer.writerows(data)

def tambah_csv(nama_file, fieldnames, data_baru):
    path = DATA_PATH + nama_file
    file_ada = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames)
        if not file_ada:
            writer.writeheader()
        writer.writerow(data_baru)
