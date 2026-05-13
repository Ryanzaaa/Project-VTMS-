class Student:
    # Daftar mapel per klaster
    KLASTER = {
        "sains"   : ["matematika", "fisika", "kimia", "informatika"],
        "sosial"  : ["ekonomi", "sosiologi", "geografi", "sejarah"],
        "kreatif" : ["b_indonesia", "b_inggris", "seni_budaya", "prakarya"],
    }

    LABEL_KLASTER = {
        "sains"  : "Sains & Teknologi",
        "sosial" : "Sosial & Bisnis",
        "kreatif": "Kreatif & Bahasa",
    }

    def __init__(self, nim, nama, nilai_mapel):
        # nim         : NIM siswa (unik)
        # nama        : Nama siswa
        # nilai_mapel : dict berisi nilai 12 mata pelajaran
        # next        : pointer ke node berikutnya
        self.nim         = nim
        self.nama        = nama
        self.nilai_mapel = nilai_mapel
        self.next        = None

    def skor_klaster(self):
        # Hitung rata-rata nilai per klaster dari nilai mapel
        hasil = {}
        for klaster, mapel_list in self.KLASTER.items():
            nilai_list = [self.nilai_mapel.get(m, 0) for m in mapel_list]
            hasil[klaster] = sum(nilai_list) / len(nilai_list)
        return hasil

    def rekomendasi(self):
        # Klaster dengan skor tertinggi = rekomendasi jurusan
        skor = self.skor_klaster()
        return max(skor, key=skor.get)

    def __str__(self):
        skor  = self.skor_klaster()
        rek   = self.rekomendasi()
        label = self.LABEL_KLASTER[rek]
        return (
            f"NIM: {self.nim} | Nama: {self.nama} | "
            f"Sains: {skor['sains']:.1f} | "
            f"Sosial: {skor['sosial']:.1f} | "
            f"Kreatif: {skor['kreatif']:.1f} | "
            f"Rekomendasi: {label}"
        )