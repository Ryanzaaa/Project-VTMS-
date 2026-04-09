from structures.linked_list import LinkedList
from structures.stack import Stack
from services.file_handler import simpan_csv

ll = LinkedList()
stack = Stack()

def menu():
    print("\n=== VTMS MENU ===")
    print("1. Tambah")
    print("2. Lihat")
    print("3. Undo")
    print("4. Keluar")

while True:
    menu()
    pilihan = input("Pilih: ")

    if pilihan == "1":
        nim = input("NIM: ")
        nama = input("Nama: ")

        try:
            nilai_algoritma = int(input("Nilai Algoritma: "))
            nilai_uiux = int(input("Nilai UIUX: "))
        except ValueError:
            print("Input harus angka!")
            continue

        nilai = {
            "algoritma": nilai_algoritma,
            "uiux": nilai_uiux
        }

        ll.tambah(nim, nama, nilai)
        stack.push(("tambah", nim, nama, nilai))

        simpan_csv(ll)
        print("Data berhasil ditambah!")

    elif pilihan == "2":
        ll.tampilkan()

    elif pilihan == "3":
        aksi = stack.pop()

        if aksi is None:
            print("Tidak ada data untuk di-undo")
            continue

        tipe = aksi[0]

        if tipe == "tambah":
            nim = aksi[1]
            ll.hapus(nim)
            simpan_csv(ll)
            print("Undo tambah berhasil")

    elif pilihan == "4":
        break