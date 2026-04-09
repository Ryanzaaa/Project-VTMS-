from models.student import Student

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, nim, nama, nilai):
        new_node = Student(nim, nama, nilai)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def tampilkan(self):
        current = self.head
        while current:
            print(current.nim, current.nama, current.nilai)
            current = current.next

    def hapus(self, nim):
        current = self.head
        prev = None
        while current:
            if current.nim == nim:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next

        return False