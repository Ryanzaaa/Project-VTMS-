import csv

def simpan_csv(linked_list):
    with open("data/students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["NIM", "Nama", "Algoritma", "UIUX"])

        current = linked_list.head
        while current:
            writer.writerow([
                current.nim,
                current.nama,
                current.nilai["algoritma"],
                current.nilai["uiux"]
            ])
            current = current.next

