import csv
import os

FILE_PATH = "data/students.csv"

# Daftar semua mapel sesuai urutan kolom di CSV
SEMUA_MAPEL = [
    "matematika", "fisika", "kimia", "informatika",
    "ekonomi", "sosiologi", "geografi", "sejarah",
    "b_indonesia", "b_inggris", "seni_budaya", "prakarya"
]


def muat_csv(linked_list):
    # Kalau file belum ada, skip (program baru pertama kali jalan)
    if not os.path.exists(FILE_PATH):
        return

    with open(FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nim  = row["NIM"]
            nama = row["Nama"]
            nilai_mapel = {mapel: int(row[mapel]) for mapel in SEMUA_MAPEL}
            linked_list.tambah(nim, nama, nilai_mapel)


def simpan_csv(linked_list):
    # Pastikan folder data ada
    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NIM", "Nama"] + SEMUA_MAPEL)

        current = linked_list.head
        while current:
            row = [current.nim, current.nama]
            for mapel in SEMUA_MAPEL:
                row.append(current.nilai_mapel.get(mapel, 0))
            writer.writerow(row)
            current = current.next