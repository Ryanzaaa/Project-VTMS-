from structures.linked_list import LinkedList
from structures.stack import Stack
from services.file_handler import simpan_csv, muat_csv

ll = LinkedList()
stack = Stack()

# Load data dari CSV saat program dijalankan
muat_csv(ll)


# ──────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────
def input_nilai():
    
    # Minta input nilai 3 klaster, validasi harus angka 0-100
    while True:
        try:
            prog = int(input("    Nilai Programming (0-100): "))
            design = int(input("    Nilai Design     (0-100): "))
            analisis = int(input("    Nilai Analisis   (0-100): "))

            if not all(0 <= x <= 100 for x in [prog, design, analisis]):
                print("  [!] Nilai harus antara 0 sampai 100!\n")
                continue

            return {"programming": prog, "design": design, "analisis": analisis}

        except ValueError:
            print("  [!] Input harus berupa angka!\n")


def menu():
    print("\n" + "=" * 40)
    print("   VTMS - Vocational Talent Mapping")
    print("=" * 40)
    print("  1. Tambah Mahasiswa")
    print("  2. Lihat Semua Mahasiswa")
    print("  3. Cari Mahasiswa")
    print("  4. Update Mahasiswa")
    print("  5. Hapus Mahasiswa")
    print("  6. Undo Aksi Terakhir")
    print("  7. Keluar")
    print("=" * 40)


# ──────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────
print("\nSelamat datang di VTMS!")

while True:
    menu()
    pilihan = input("  Pilih menu: ").strip()

    # 1. TAMBAH
    if pilihan == "1":
        print("\n  [ TAMBAH MAHASISWA ]")
        nim  = input("  NIM  : ").strip()
        nama = input("  Nama : ").strip()

        if not nim or not nama:
            print("  [!] NIM dan Nama tidak boleh kosong!")
            continue

        print("  Masukkan nilai:")
        nilai = input_nilai()

        berhasil = ll.tambah(nim, nama, nilai)

        if not berhasil:
            print(f"  [!] NIM {nim} sudah terdaftar!")
        else:
            stack.push(("tambah", nim))
            simpan_csv(ll)
            print(f"  [✓] Mahasiswa {nama} berhasil ditambahkan!")

    # 2. LIHAT 
    elif pilihan == "2":
        print("\n  [ DAFTAR MAHASISWA ]")
        ll.tampilkan()

    # 3. CARI 
    elif pilihan == "3":
        print("\n  [ CARI MAHASISWA ]")
        keyword = input("  Masukkan NIM atau Nama: ").strip()

        # Coba cari by NIM dulu
        node = ll.cari(keyword)
        if node:
            print()
            print("  Ditemukan:")
            print(f"  {node}")
        else:
            # Kalau tidak ketemu by NIM, cari by nama
            hasil = ll.cari_nama(keyword)
            if hasil:
                print(f"\n  Ditemukan {len(hasil)} mahasiswa:\n")
                for h in hasil:
                    print(f"  {h}")
            else:
                print(f"  [!] Tidak ada mahasiswa dengan NIM/Nama '{keyword}'")

    # 4. UPDATE 
    elif pilihan == "4":
        print("\n  [ UPDATE MAHASISWA ]")
        nim = input("  Masukkan NIM yang ingin diupdate: ").strip()

        node = ll.cari(nim)
        if not node:
            print(f"  [!] NIM {nim} tidak ditemukan!")
            continue

        print(f"\n  Data sekarang: {node}")
        print("\n  Kosongkan (Enter) untuk tidak mengubah field tersebut.")

        nama_baru = input("  Nama baru    : ").strip()

        print("  Nilai baru (kosongkan jika tidak ingin diubah):")
        try:
            prog_input     = input("    Programming : ").strip()
            design_input   = input("    Design      : ").strip()
            analisis_input = input("    Analisis    : ").strip()
        except ValueError:
            print("  [!] Input nilai harus angka!")
            continue

        # Simpan data lama untuk undo
        data_lama = {
            "nama" : node.nama,
            "nilai": dict(node.nilai)
        }

        # Bangun nilai_baru hanya dari field yang diisi
        nilai_baru = {}
        try:
            if prog_input:
                nilai_baru["programming"] = int(prog_input)
            if design_input:
                nilai_baru["design"] = int(design_input)
            if analisis_input:
                nilai_baru["analisis"] = int(analisis_input)
        except ValueError:
            print("  [!] Input nilai harus angka!")
            continue

        ll.update(
            nim,
            nama_baru=nama_baru if nama_baru else None,
            nilai_baru=nilai_baru if nilai_baru else None
        )

        stack.push(("update", nim, data_lama))
        simpan_csv(ll)
        print(f"  [✓] Data mahasiswa {nim} berhasil diupdate!")

    # 5. HAPUS 
    elif pilihan == "5":
        print("\n  [ HAPUS MAHASISWA ]")
        nim = input("  Masukkan NIM yang ingin dihapus: ").strip()

        node = ll.cari(nim)
        if not node:
            print(f"  [!] NIM {nim} tidak ditemukan!")
            continue

        print(f"\n  Data yang akan dihapus: {node}")
        konfirmasi = input("  Yakin ingin menghapus? (y/n): ").strip().lower()

        if konfirmasi != "y":
            print("  Penghapusan dibatalkan.")
            continue

        deleted = ll.hapus(nim)
        stack.push(("hapus", deleted))
        simpan_csv(ll)
        print(f"  [✓] Mahasiswa {deleted.nama} berhasil dihapus!")

    # 6. UNDO 
    elif pilihan == "6":
        aksi = stack.pop()

        if aksi is None:
            print("\n  [!] Tidak ada aksi yang bisa di-undo.")
            continue

        tipe = aksi[0]

        if tipe == "tambah":
            
            # Undo tambah = hapus data yang baru ditambah
            nim = aksi[1]
            ll.hapus(nim)
            simpan_csv(ll)
            print(f"\n  [✓] Undo tambah: NIM {nim} berhasil dihapus.")

        elif tipe == "hapus":
            
            # Undo hapus = tambahkan kembali node yang tadi dihapus
            node = aksi[1]
            ll.tambah_node(node)
            simpan_csv(ll)
            print(f"\n  [✓] Undo hapus: {node.nama} berhasil dikembalikan.")

        elif tipe == "update":
            
            # Undo update = kembalikan data lama
            nim      = aksi[1]
            data_lama = aksi[2]
            ll.update(nim, nama_baru=data_lama["nama"], nilai_baru=data_lama["nilai"])
            simpan_csv(ll)
            print(f"\n  [✓] Undo update: Data NIM {nim} dikembalikan ke kondisi semula.")

    # 7. KELUAR 
    elif pilihan == "7":
        print("\n  Sampai jumpa!\n")
        break

    else:
        print("  [!] Pilihan tidak valid, coba lagi.")
    
    # awaawaw=-