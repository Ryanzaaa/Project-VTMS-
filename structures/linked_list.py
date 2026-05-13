from models.student import Student


class LinkedList:
    # Singly Linked List untuk menyimpan data siswa secara dinamis.
    # Setiap elemen adalah node Student yang terhubung via pointer .next

    def __init__(self):
        self.head = None

    # ──────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────
    def tambah(self, nim, nama, nilai_mapel):
        # Menambah node baru di akhir linked list.
        # Menolak jika NIM sudah terdaftar (duplikat).
        # Return True jika berhasil, False jika NIM sudah ada.
        if self.cari(nim) is not None:
            return False

        new_node = Student(nim, nama, nilai_mapel)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        return True

    # ──────────────────────────────────────────
    # READ
    # ──────────────────────────────────────────
    def tampilkan(self):
        # Menampilkan semua data siswa dalam format tabel per klaster
        if self.head is None:
            print("  (Belum ada data siswa)")
            return

        print()
        print("  " + "─" * 75)
        print(f"  {'No':<4} {'NIM':<12} {'Nama':<20} {'Sains':>7} {'Sosial':>7} {'Kreatif':>8} {'Rekomendasi':<20}")
        print("  " + "─" * 75)

        current = self.head
        no = 1
        while current:
            skor = current.skor_klaster()
            rek  = current.LABEL_KLASTER[current.rekomendasi()]
            print(
                f"  {no:<4} {current.nim:<12} {current.nama:<20} "
                f"{skor['sains']:>7.1f} "
                f"{skor['sosial']:>7.1f} "
                f"{skor['kreatif']:>8.1f} "
                f"{rek:<20}"
            )
            current = current.next
            no += 1

        print("  " + "─" * 75)
        print(f"  Total: {no - 1} siswa\n")

    def cari(self, nim):
        # Mencari node berdasarkan NIM.
        # Return Student node jika ditemukan, None jika tidak.
        current = self.head
        while current:
            if current.nim == nim:
                return current
            current = current.next
        return None

    def cari_nama(self, keyword):
        # Mencari semua siswa yang namanya mengandung keyword (case-insensitive).
        # Return list of Student nodes yang cocok.
        hasil = []
        current = self.head
        while current:
            if keyword.lower() in current.nama.lower():
                hasil.append(current)
            current = current.next
        return hasil

    # ──────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────
    def update(self, nim, nama_baru=None, nilai_baru=None):
        # Memperbarui data siswa berdasarkan NIM.
        # Hanya field yang diisi (tidak None) yang akan diubah.
        # Return True jika berhasil, False jika NIM tidak ditemukan.
        node = self.cari(nim)

        if node is None:
            return False

        if nama_baru:
            node.nama = nama_baru

        if nilai_baru:
            # Update hanya mapel yang diberikan, sisanya tetap
            for mapel, val in nilai_baru.items():
                node.nilai_mapel[mapel] = val

        return True

    # ──────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────
    def hapus(self, nim):
        # Menghapus node berdasarkan NIM.
        # Return node yang dihapus (untuk keperluan undo di Stack),
        # atau None jika NIM tidak ditemukan.
        current = self.head
        prev = None

        while current:
            if current.nim == nim:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                current.next = None
                return current

            prev = current
            current = current.next

        return None

    # ──────────────────────────────────────────
    # UTILITY
    # ──────────────────────────────────────────
    def ke_list(self):
        # Mengubah seluruh linked list menjadi list Python biasa.
        # Dipakai oleh sorting dan file_handler.
        hasil = []
        current = self.head
        while current:
            hasil.append(current)
            current = current.next
        return hasil

    def dari_list(self, list_node):
        # Membangun ulang linked list dari list Python (hasil sorting).
        self.head = None
        for node in list_node:
            node.next = None
            self.tambah_node(node)

    def tambah_node(self, node):
        # Menambah node Student yang sudah ada langsung ke linked list.
        node.next = None
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def kosong(self):
        # Mengecek apakah linked list kosong.
        return self.head is None