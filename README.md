# 🎓 VTMS — Vocational Talent Mapping System

> Sistem berbasis CLI untuk memetakan bakat dan merekomendasikan jurusan vokasi bagi siswa berdasarkan nilai mata pelajaran, dibangun menggunakan struktur data Linked List, Stack, Merge Sort, dan Binary Search.

---

## 📋 Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Fitur Utama](#fitur-utama)
- [Arsitektur & Struktur Data](#arsitektur--struktur-data)
- [Prasyarat Instalasi](#prasyarat-instalasi)
- [Panduan Instalasi](#panduan-instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Direktori](#struktur-direktori)
- [Analisis Algoritma (Big O)](#analisis-algoritma-big-o)
- [Anggota Tim](#anggota-tim)

---

## Deskripsi Proyek

VTMS adalah aplikasi command-line yang membantu guru BK (Bimbingan Konseling) atau staf sekolah vokasi dalam **memetakan potensi siswa** ke tiga klaster jurusan:

| Klaster | Mata Pelajaran yang Dinilai |
|---|---|
| 🔬 Sains & Teknologi | Matematika, Fisika, Kimia, Informatika |
| 💼 Sosial & Bisnis | Ekonomi, Sosiologi, Geografi, Sejarah |
| 🎨 Kreatif & Bahasa | B. Indonesia, B. Inggris, Seni Budaya, Prakarya |

Sistem menghitung **rata-rata skor per klaster** dari 12 mata pelajaran, lalu merekomendasikan jurusan yang paling sesuai dengan profil nilai masing-masing siswa. Data disimpan secara persisten dalam file CSV.

---

## Fitur Utama

| No | Fitur | Keterangan |
|---|---|---|
| 1 | **Tambah Siswa** | Input NIS, nama, dan nilai 12 mata pelajaran dengan validasi input ketat |
| 2 | **Lihat Semua Siswa** | Tampilkan seluruh data dalam format tabel beserta skor per klaster |
| 3 | **Cari Siswa** | Pencarian by NIS (Binary Search) atau by nama (Linear Search partial match) |
| 4 | **Update Siswa** | Edit nama dan/atau nilai mapel tertentu saja (field lain tetap) |
| 5 | **Hapus Siswa** | Hapus data dengan konfirmasi terlebih dahulu |
| 6 | **Undo Aksi** | Batalkan aksi tambah / hapus / update terakhir menggunakan Stack |
| 7 | **Ranking per Klaster** | Peringkat siswa berdasarkan skor Sains, Sosial, atau Kreatif (Merge Sort) |

---

## Arsitektur & Struktur Data

Program dibangun dengan **4 struktur data / algoritma utama**:

### 1. Singly Linked List (`structures/linked_list.py`)
Menyimpan seluruh data siswa secara **dinamis** (tidak ada batas ukuran array). Setiap node adalah objek `Student` yang memiliki pointer `.next` ke siswa berikutnya.

```
HEAD → [S001|Rifqi|→] → [S002|Nadia|→] → [S003|Ryan|→] → None
```

Operasi yang didukung: `tambah()`, `cari()`, `cari_nama()`, `update()`, `hapus()`, `ke_list()`, `dari_list()`.

### 2. Stack (`structures/stack.py`)
Mengimplementasikan fitur **Undo** dengan prinsip LIFO (Last In, First Out). Setiap aksi CRUD yang berhasil di-`push` ke stack. Saat undo, aksi terakhir di-`pop` lalu dibalik.

```
Stack (LIFO):
TOP → ("update", "S001", data_lama)
      ("tambah", "S005")
      ("hapus",  node_S003)
```

### 3. Merge Sort (`structures/algorithm_engine.py`)
Digunakan untuk **mengurutkan siswa di fitur Ranking**. Kompleksitas O(n log n), jauh lebih efisien dari Bubble Sort untuk data yang besar.

Cara kerja (divide and conquer):
```
[Nadia, Ryan, Rifqi, Dinda]
   ↓ Bagi dua
[Nadia, Ryan]   [Rifqi, Dinda]
   ↓ Bagi lagi
[Nadia][Ryan]   [Rifqi][Dinda]
   ↓ Merge (bandingkan & gabung terurut)
[Nadia, Ryan]   [Dinda, Rifqi]
   ↓ Merge akhir
[Dinda, Nadia, Rifqi, Ryan]  ← Terurut!
```

### 4. Binary Search (`structures/algorithm_engine.py`)
Digunakan saat **cari siswa by NIS**. Lebih efisien dari linear search (O(log n) vs O(n)).

Alur:
1. Ambil semua node dari Linked List → ubah ke Python list
2. Sort berdasarkan NIS menggunakan Merge Sort (O(n log n))
3. Lakukan Binary Search: selalu periksa elemen tengah, buang setengah data yang tidak mungkin

---

## Prasyarat Instalasi

- **Python 3.10** atau lebih baru
- Tidak memerlukan library eksternal (hanya menggunakan `csv` dan `os` dari Python standard library)

Cek versi Python:
```bash
python --version
# atau
python3 --version
```

---

## Panduan Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/Ryanzaaa/Project-VTMS-.git
cd Project-VTMS-
```

### 2. (Opsional) Buat Virtual Environment

```bash
python -m venv venv

# Aktivasi di Windows:
venv\Scripts\activate

# Aktivasi di macOS/Linux:
source venv/bin/activate
```

### 3. Jalankan Program

```bash
python main.py
```

> **Catatan:** Program harus dijalankan dari root folder `Project-VTMS-/` agar path file `data/students.csv` terbaca dengan benar.

---

## Cara Penggunaan

Setelah program berjalan, muncul menu utama:

```
========================================
   VTMS - Vocational Talent Mapping
========================================
  1. Tambah Siswa
  2. Lihat Semua Siswa
  3. Cari Siswa
  4. Update Siswa
  5. Hapus Siswa
  6. Undo Aksi Terakhir
  7. Ranking per Klaster
  8. Keluar
========================================
```

### Menambah Siswa Baru
1. Pilih menu `1`
2. Masukkan NIS (harus unik) dan Nama
3. Input nilai 12 mata pelajaran (0–100). Program akan menolak input di luar rentang atau input bukan angka
4. Setelah tersimpan, rekomendasi klaster langsung ditampilkan

### Mencari Siswa
- Pilih menu `3`, lalu pilih:
  - **a (by NIS):** menggunakan Binary Search — lebih cepat, cocok jika NIS diketahui persis
  - **b (by Nama):** menggunakan Linear Search dengan partial match — bisa mencari nama sebagian (contoh: "Nad" akan menemukan "Nadia")

### Melihat Ranking
- Pilih menu `7`, lalu pilih klaster (Sains / Sosial / Kreatif)
- Sistem mengurutkan semua siswa dengan Merge Sort berdasarkan skor klaster yang dipilih

### Fitur Undo
- Pilih menu `6` untuk membatalkan aksi **tambah**, **hapus**, atau **update** terakhir
- Stack undo otomatis dikosongkan saat program ditutup (tidak persisten antar-sesi)

---

## Struktur Direktori

```
Project-VTMS-/
│
├── main.py                     # Entry point — menu utama & logika UI
│
├── models/
│   └── student.py              # Class Student (node Linked List) + logika klaster
│
├── structures/
│   ├── linked_list.py          # Implementasi Singly Linked List (CRUD)
│   ├── stack.py                # Implementasi Stack (untuk fitur Undo)
│   └── algorithm_engine.py     # Merge Sort + Binary Search + menu Ranking
│
├── services/
│   └── file_handler.py         # Persistensi data: baca/tulis CSV
│
├── data/
│   └── students.csv            # File penyimpanan data siswa (auto-generated)
│
└── README.md
```

---

## Analisis Algoritma (Big O)

| Operasi | Algoritma | Kompleksitas Waktu | Keterangan |
|---|---|---|---|
| Tambah siswa | Linked List traverse | O(n) | Sisipkan di akhir list |
| Cari by NIS | Binary Search | O(n log n) | Dominan di fase sort; search-nya O(log n) |
| Cari by Nama | Linear Search | O(n) | Partial match, harus scan semua node |
| Hapus siswa | Linked List traverse | O(n) | Cari node lalu putus pointer |
| Ranking | Merge Sort | O(n log n) | Lebih efisien dari Bubble Sort O(n²) |
| Undo | Stack pop | O(1) | Operasi konstan |

**Mengapa Merge Sort, bukan Bubble Sort?**
Bubble Sort memiliki kompleksitas O(n²) — pada 1000 siswa, ini berarti ~1.000.000 perbandingan. Merge Sort dengan O(n log n) hanya memerlukan ~10.000 perbandingan. Selisih ini sangat signifikan saat data bertumbuh.

---

## Anggota Tim

| Nama | NIM | Kontribusi Utama |
|---|---|---|
| Ryanza Faraz Mulia | J0403251064 | Stack, CSV File, Validasi Imput, Menu CLI |
| Valentino Agripina Pranaja De Ropa | J0403251154 | Algorithm Engine: Merge Sort, Searching by NIS, Ranking per Cluster|
| Rifqi Tazakka Putra | J0403251158 | Linked List, Class Student, Fungsi CRUD |


---

> Proyek ini dibuat untuk memenuhi tugas Project-Based Learning mata kuliah Algoritma & Struktur Data (TPL2106).

> Berikut link video presentasi projek kami : https://youtu.be/bM9pysVTCRM