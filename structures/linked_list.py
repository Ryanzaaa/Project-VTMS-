from models.student import Student


class LinkedList:
    """
    Singly Linked List untuk menyimpan data mahasiswa secara dinamis.
    Setiap elemen adalah node Student yang terhubung via pointer .next
    """

    def __init__(self):
        self.head = None

    # ──────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────
    def tambah(self, nim, nama, nilai):
        """
        Menambah node baru di akhir linked list.
        Menolak jika NIM sudah terdaftar (duplikat).

        Return:
            True  — berhasil ditambah
            False — NIM sudah ada
        """
        # Cek duplikat NIM
        if self.cari(nim) is not None:
            return False

        new_node = Student(nim, nama, nilai)

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
        """ Menampilkan semua data mahasiswa dalam format tabel. """
        if self.head is None:
            print("  (Belum ada data mahasiswa)")
            return

        print()
        print("  " + "─" * 80)
        print(f"  {'No':<4} {'NIM':<12} {'Nama':<20} {'Prog':>6} {'Design':>7} {'Analisis':>9} {'Rata²':>7}")
        print("  " + "─" * 80)

        current = self.head
        no = 1
        while current:
            n = current.nilai
            print(
                f"  {no:<4} {current.nim:<12} {current.nama:<20} "
                f"{n.get('programming', 0):>6} "
                f"{n.get('design', 0):>7} "
                f"{n.get('analisis', 0):>9} "
                f"{current.rata_rata():>7.1f}"
            )
            current = current.next
            no += 1

        print("  " + "─" * 80)
        print(f"  Total: {no - 1} mahasiswa\n")

    def cari(self, nim):
        """
        Mencari node berdasarkan NIM.

        Return:
            Student node jika ditemukan, None jika tidak.
        """
        current = self.head
        while current:
            if current.nim == nim:
                return current
            current = current.next
        return None

    def cari_nama(self, keyword):
        """
        Mencari semua mahasiswa yang namanya mengandung keyword (case-insensitive).

        Return:
            List of Student nodes yang cocok.
        """
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
        """
        Memperbarui data mahasiswa berdasarkan NIM.
        Hanya field yang diisi (tidak None) yang akan diubah.

        Return:
            True, berhasil diupdate
            False, NIM tidak ditemukan
        """
        node = self.cari(nim)

        if node is None:
            return False

        if nama_baru:
            node.nama = nama_baru

        if nilai_baru:
            # Update hanya klaster yang diberikan, sisanya tetap
            for klaster, val in nilai_baru.items():
                node.nilai[klaster] = val

        return True

    # ──────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────
    def hapus(self, nim):
        """
        Menghapus node berdasarkan NIM.

        Return:
            Student node yang dihapus (untuk keperluan undo di Stack),
            atau None jika tidak ditemukan.
        """
        current = self.head
        prev = None

        while current:
            if current.nim == nim:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                current.next = None  # Putus pointer
                return current       # Kembalikan node yang dihapus

            prev = current
            current = current.next

        return None  # NIM tidak ditemukan

    # ──────────────────────────────────────────
    # UTILITY
    # ──────────────────────────────────────────
    def ke_list(self):
        """
        Mengubah seluruh linked list menjadi list Python biasa.
        Dipakai oleh sorting dan file_handler.

        Return:
            List of Student nodes.
        """
        hasil = []
        current = self.head
        while current:
            hasil.append(current)
            current = current.next
        return hasil

    def dari_list(self, list_node):
        """
        Membangun ulang linked list dari list Python (hasil sorting).
        Semua pointer .next akan di-reset dan disambung ulang.
        """
        self.head = None
        for node in list_node:
            node.next = None
            self.tambah_node(node)

    def tambah_node(self, node):
        """ Menambah node Student yang sudah ada langsung ke linked list. """
        node.next = None
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def kosong(self):
        """ Mengecek apakah linked list kosong. """
        return self.head is None