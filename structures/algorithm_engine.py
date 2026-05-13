# ══════════════════════════════════════════════════════════
#  ALGORITHM ENGINE — Sorting & Searching
#  Modul ini berisi implementasi:
#    1. Merge Sort  — mengurutkan siswa by skor klaster
#    2. Binary Search by NIM — mencari siswa secara efisien
#    3. Ranking per Cluster  — menampilkan peringkat tiap klaster
# ══════════════════════════════════════════════════════════


# ──────────────────────────────────────────
# 1. MERGE SORT
# ──────────────────────────────────────────

def merge_sort(arr, key_func, descending=True):
    """
    Implementasi Merge Sort rekursif pada list of Student nodes.

    Args:
        arr        (list)     : List of Student nodes
        key_func   (callable) : Fungsi pengambil nilai untuk diurutkan
                                Contoh: lambda s: s.skor_klaster()['sains']
        descending (bool)     : True = nilai besar di atas (default ranking)

    Return:
        List of Student nodes yang sudah diurutkan.

    Kompleksitas: O(n log n)
    """
    if len(arr) <= 1:
        return arr

    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key_func, descending)
    right = merge_sort(arr[mid:], key_func, descending)

    return _merge(left, right, key_func, descending)


def _merge(left, right, key_func, descending):
    """
    Proses penggabungan dua list terurut menjadi satu list terurut.
    (Fungsi internal)
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        lv = key_func(left[i])
        rv = key_func(right[j])

        if descending:
            ambil_kiri = lv >= rv
        else:
            ambil_kiri = lv <= rv

        if ambil_kiri:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ──────────────────────────────────────────
# 2. BINARY SEARCH BY NIM
# ──────────────────────────────────────────

def binary_search_nim(linked_list, target_nim):
    """
    Mencari siswa by NIM menggunakan Binary Search.

    Cara kerja:
      1. Ambil semua node dari linked list → ubah ke list
      2. Sort list berdasarkan NIM (ascending) pakai Merge Sort — O(n log n)
      3. Lakukan binary search — O(log n)

    Args:
        linked_list : LinkedList object
        target_nim  : NIM yang dicari (str)

    Return:
        Student node jika ditemukan, None jika tidak.
    """
    arr = linked_list.ke_list()

    if not arr:
        return None

    arr_sorted = merge_sort(arr, key_func=lambda s: s.nim, descending=False)

    lo, hi = 0, len(arr_sorted) - 1

    while lo <= hi:
        mid     = (lo + hi) // 2
        mid_nim = arr_sorted[mid].nim

        if mid_nim == target_nim:
            return arr_sorted[mid]
        elif mid_nim < target_nim:
            lo = mid + 1
        else:
            hi = mid - 1

    return None


# ──────────────────────────────────────────
# 3. RANKING PER CLUSTER
# ──────────────────────────────────────────

CLUSTERS = {
    "sains"   : "Sains & Teknologi",
    "sosial"  : "Sosial & Bisnis",
    "kreatif" : "Kreatif & Bahasa",
}


def tampilkan_ranking(linked_list, cluster="sains"):
    """
    Menampilkan peringkat siswa berdasarkan skor klaster tertentu.

    Args:
        linked_list : LinkedList object
        cluster     : Salah satu dari 'sains', 'sosial', 'kreatif'
    """
    arr = linked_list.ke_list()

    if not arr:
        print("  (Belum ada data siswa)")
        return

    key_func   = lambda s: s.skor_klaster()[cluster]
    sorted_arr = merge_sort(arr, key_func, descending=True)
    label      = CLUSTERS.get(cluster, cluster)

    print()
    print(f"  ╔{'═' * 68}╗")
    print(f"  ║  🏆  RANKING KLASTER: {label:<46}║")
    print(f"  ╠{'═' * 68}╣")
    print(f"  ║  {'Rank':<5} {'NIM':<12} {'Nama':<20} {'Skor':>7} {'Rekomendasi':<20}  ║")
    print(f"  ╠{'═' * 68}╣")

    for rank, student in enumerate(sorted_arr, start=1):
        skor  = student.skor_klaster()[cluster]
        rek   = student.LABEL_KLASTER[student.rekomendasi()]
        medal = ""
        if   rank == 1: medal = "🥇"
        elif rank == 2: medal = "🥈"
        elif rank == 3: medal = "🥉"
        else:           medal = f"  {rank}."

        print(
            f"  ║  {medal:<5} {student.nim:<12} {student.nama:<20} "
            f"{skor:>7.1f} {rek:<20}  ║"
        )

    print(f"  ╚{'═' * 68}╝")
    print(f"  Total: {len(sorted_arr)} siswa\n")


def menu_ranking(linked_list):
    """
    Sub-menu untuk memilih klaster ranking yang ingin ditampilkan.
    """
    print("\n  [ RANKING PER KLASTER ]")
    print("  Pilih klaster:")
    print("    a. Sains & Teknologi")
    print("    b. Sosial & Bisnis")
    print("    c. Kreatif & Bahasa")

    pilihan = input("  Pilih (a/b/c): ").strip().lower()

    cluster_map = {
        "a": "sains",
        "b": "sosial",
        "c": "kreatif",
    }

    cluster = cluster_map.get(pilihan)
    if cluster is None:
        print("  [!] Pilihan tidak valid.")
        return

    tampilkan_ranking(linked_list, cluster)
