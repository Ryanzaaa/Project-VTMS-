import csv
import os

FILE_PATH = "data/students.csv"

def muat_csv(linked_list):
    
    # Kalau file belum ada, skip (program baru pertama kali jalan)
    if not os.path.exists(FILE_PATH):
        return
 
    with open(FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nim  = row["NIM"]
            nama = row["Nama"]
            nilai = {
                "programming": int(row["Programming"]),
                "design"     : int(row["Design"]),
                "analisis"   : int(row["Analisis"]),
            }
            linked_list.tambah(nim, nama, nilai)

def simpan_csv(linked_list):
    
    # Pastikan folder data ada
    os.makedirs("data", exist_ok=True)

    with open(FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NIM", "Nama", "Programming", "Design", "Analisis"])

        current = linked_list.head
        while current:
            writer.writerow([
                current.nim,
                current.nama,
                current.nilai.get("programming", 0),
                current.nilai.get("design", 0),
                current.nilai.get("analisis", 0),
            ])
            current = current.next