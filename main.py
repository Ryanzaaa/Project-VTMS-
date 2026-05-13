from structures.linked_list import LinkedList
from structures.stack import Stack
from services.file_handler import simpan_csv, muat_csv, SEMUA_MAPEL
from models.student import Student
from structures.algorithm_engine import binary_search_nim, menu_ranking

ll    = LinkedList()
stack = Stack()

# Load data dari CSV saat program pertama kali dijalankan
muat_csv(ll)


# ──────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────
LABEL_MAPEL = {
    "matematika" : "Matematika",
    "fisika"     : "Fisika",
    "kimia"      : "Kimia",
    "informatika": "Informatika",
    "ekonomi"    : "Ekonomi",
    "sosiologi"  : "Sosiologi",
    "geografi"   : "Geografi",
    "sejarah"    : "Sejarah",
    "b_indonesia": "B. Indonesia",
    "b_inggris"  : "B. Inggris",
    "seni_budaya": "Seni Budaya",
    "prakarya"   : "Prakarya",
}

def input_nilai_mapel():
    # Minta input nilai semua mapel satu per satu
    nilai = {}
    print("  Masukkan nilai per mata pelajaran (0-100):")
    for mapel in SEMUA_MAPEL:
        while True:
            try:
                val = int(input(f"    {LABEL_MAPEL[mapel]:<15}: "))
                if 0 <= val <= 100:
                    nilai[mapel] = val
                    break
                else:
                    print("    [!] Nilai harus antara 0-100!")
            except ValueError:
                print("    [!] Input harus angka!")
    return nilai

def tampil_detail(node):
    # Tampilkan detail lengkap satu siswa beserta nilai per mapel
    skor  = node.skor_klaster()
    rek   = node.LABEL_KLASTER[node.rekomendasi()]
    print()
    print(f"  NIM  : {node.nim}")
    print(f"  Nama : {node.nama}")
    print()
    print(f"  {'─'*35}")
    print(f"  {'Mata Pelajaran':<20} {'Nilai':>6}")
    print(f"  {'─'*35}")
    for mapel in SEMUA_MAPEL:
        print(f"  {LABEL_MAPEL[mapel]:<20} {node.nilai_mapel.get(mapel, 0):>6}")
    print(f"  {'─'*35}")
    print(f"  Skor Sains    : {skor['sains']:.1f}")
    print(f"  Skor Sosial   : {skor['sosial']:.1f}")
    print(f"  Skor Kreatif  : {skor['kreatif']:.1f}")
    print(f"  {'─'*35}")
    print(f"  ★ Rekomendasi : {rek}")
    print()

def menu():
    print("\n" + "=" * 40)
    print("   VTMS - Vocational Talent Mapping")
    print("=" * 40)
    print("  1. Tambah Siswa")
    print("  2. Lihat Semua Siswa")
    print("  3. Cari Siswa")
    print("  4. Update Siswa")
    print("  5. Hapus Siswa")
    print("  6. Undo Aksi Terakhir")
    print("  7. Ranking per Klaster")
    print("  8. Keluar")
    print("=" * 40)


# ──────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────
print("\nSelamat datang di VTMS!")

while True:
    menu()
    pilihan = input("  Pilih menu: ").strip()

    # ── 1. TAMBAH ──
    if pilihan == "1":
        print("\n  [ TAMBAH SISWA ]")
        nim  = input("  NIM  : ").strip()
        nama = input("  Nama : ").strip()

        if not nim or not nama:
            print("  [!] NIM dan Nama tidak boleh kosong!")
            continue

        nilai_mapel = input_nilai_mapel()

        berhasil = ll.tambah(nim, nama, nilai_mapel)
        if not berhasil:
            print(f"  [!] NIM {nim} sudah terdaftar!")
        else:
            stack.push(("tambah", nim))
            simpan_csv(ll)
            print(f"  [✓] Siswa {nama} berhasil ditambahkan!")
            # Langsung tampilkan rekomendasinya
            node = ll.cari(nim)
            rek  = node.LABEL_KLASTER[node.rekomendasi()]
            print(f"  ★ Rekomendasi klaster: {rek}")

    # ── 2. LIHAT ──
    elif pilihan == "2":
        print("\n  [ DAFTAR SISWA ]")
        ll.tampilkan()

    # ── 3. CARI ──
    elif pilihan == "3":
        print("\n  [ CARI SISWA ]")
        print("    a. Cari by NIM")
        print("    b. Cari by Nama")
        sub = input("  Pilih (a/b): ").strip().lower()

        if sub == "a":
            nim = input("  Masukkan NIM: ").strip()
            print("  Mencari dengan Binary Search...")
            node = binary_search_nim(ll, nim)
            if node:
                tampil_detail(node)
            else:
                print(f"  [!] NIM '{nim}' tidak ditemukan.")

        elif sub == "b":
            keyword = input("  Masukkan Nama: ").strip()
            hasil = ll.cari_nama(keyword)
            if hasil:
                print(f"\n  Ditemukan {len(hasil)} siswa:\n")
                for h in hasil:
                    tampil_detail(h)
            else:
                print(f"  [!] Tidak ada siswa dengan nama '{keyword}'")

        else:
            print("  [!] Pilihan tidak valid.")

    # ── 4. UPDATE ──
    elif pilihan == "4":
        print("\n  [ UPDATE SISWA ]")
        nim = input("  Masukkan NIM yang ingin diupdate: ").strip()

        node = ll.cari(nim)
        if not node:
            print(f"  [!] NIM {nim} tidak ditemukan!")
            continue

        tampil_detail(node)
        print("  Kosongkan (Enter) untuk tidak mengubah field tersebut.\n")

        nama_baru = input("  Nama baru (Enter = skip): ").strip()

        print("  Update nilai mapel (Enter = skip):")
        nilai_baru = {}
        for mapel in SEMUA_MAPEL:
            while True:
                raw = input(f"    {LABEL_MAPEL[mapel]:<15}: ").strip()
                if raw == "":
                    break
                try:
                    val = int(raw)
                    if 0 <= val <= 100:
                        nilai_baru[mapel] = val
                        break
                    else:
                        print("    [!] Nilai harus 0-100!")
                except ValueError:
                    print("    [!] Input harus angka!")

        # Simpan data lama untuk undo
        data_lama = {"nama": node.nama, "nilai_mapel": dict(node.nilai_mapel)}

        ll.update(
            nim,
            nama_baru=nama_baru if nama_baru else None,
            nilai_baru=nilai_baru if nilai_baru else None
        )

        stack.push(("update", nim, data_lama))
        simpan_csv(ll)
        print(f"  [✓] Data siswa {nim} berhasil diupdate!")

    # ── 5. HAPUS ──
    elif pilihan == "5":
        print("\n  [ HAPUS SISWA ]")
        nim = input("  Masukkan NIM yang ingin dihapus: ").strip()

        node = ll.cari(nim)
        if not node:
            print(f"  [!] NIM {nim} tidak ditemukan!")
            continue

        print(f"\n  Akan menghapus: {node.nama} ({node.nim})")
        konfirmasi = input("  Yakin? (y/n): ").strip().lower()

        if konfirmasi != "y":
            print("  Penghapusan dibatalkan.")
            continue

        deleted = ll.hapus(nim)
        stack.push(("hapus", deleted))
        simpan_csv(ll)
        print(f"  [✓] Siswa {deleted.nama} berhasil dihapus!")

    # ── 6. UNDO ──
    elif pilihan == "6":
        aksi = stack.pop()

        if aksi is None:
            print("\n  [!] Tidak ada aksi yang bisa di-undo.")
            continue

        tipe = aksi[0]

        if tipe == "tambah":
            nim = aksi[1]
            ll.hapus(nim)
            simpan_csv(ll)
            print(f"\n  [✓] Undo tambah: NIM {nim} berhasil dihapus.")

        elif tipe == "hapus":
            node = aksi[1]
            ll.tambah_node(node)
            simpan_csv(ll)
            print(f"\n  [✓] Undo hapus: {node.nama} berhasil dikembalikan.")

        elif tipe == "update":
            nim       = aksi[1]
            data_lama = aksi[2]
            ll.update(nim, nama_baru=data_lama["nama"], nilai_baru=data_lama["nilai_mapel"])
            simpan_csv(ll)
            print(f"\n  [✓] Undo update: Data NIM {nim} dikembalikan.")

    # ── 7. RANKING ──
    elif pilihan == "7":
        menu_ranking(ll)

    # ── 8. KELUAR ──
    elif pilihan == "8":
        print("\n  Sampai jumpa!\n")
        break

    else:
        print("  [!] Pilihan tidak valid, coba lagi.")
    
    # awaawaw=-