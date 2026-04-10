class Student:
    def __init__(self, nim, nama, nilai):
        """
        Node untuk Linked List.
        
        Atribut:
            nim   (str)  : Nomor Induk Mahasiswa (unik, dipakai sebagai key)
            nama  (str)  : Nama mahasiswa
            nilai (dict) : Nilai per klaster {
                               'programming' : int,
                               'design'      : int,
                               'analisis'    : int
                           }
            next         : Pointer ke node berikutnya
        """
        self.nim   = nim
        self.nama  = nama
        self.nilai = nilai   # dict dengan key: programming, design, analisis
        self.next  = None

    def rata_rata(self):
        """ Menghitung rata-rata nilai dari semua klaster. """
        if not self.nilai:
            return 0
        return sum(self.nilai.values()) / len(self.nilai)

    def __str__(self):
        return (
            f"NIM: {self.nim} | Nama: {self.nama} | "
            f"Programming: {self.nilai.get('programming', 0)} | "
            f"Design: {self.nilai.get('design', 0)} | "
            f"Analisis: {self.nilai.get('analisis', 0)} | "
            f"Rata-rata: {self.rata_rata():.1f}"
        )