"""

Author: Dang Quang Minh (minh.dq176823@sis.hust.edu.vn)
"""

from ddl import DoublyLinkedList

# Define constants
QUAN_VALUE = 5
DEPTH = None 

class Table:
    """
    "O an quan" table.
    """
    def __init__(self, quanValue=QUAN_VALUE):
        self.quan_value = quanValue
        self.borrow = 0

        self.llist = DoublyLinkedList()
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([0, 1])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([5, 0])
        self.llist.push([0, 1])

        # self.llist.printList(self.llist.head)

    def print_table(self):
        """
        Print table in CLI
        """
        a = []

        a.append(self.llist.head.data[0] if self.llist.head.data[0] != 0 else ' ')

        n0_has_quan = '*' if self.llist.head.data[1] == 1 else ' '
        n6_has_quan = ' '

        i = self.llist.head.next
        k = 1
        while i is not None:
            a.append(i.data[0] if i.data[0] > 0 else ' ')

            if k == 6:
                n6_has_quan = '*' if i.data[1] == 1 else ' '
            k += 1
            i = i.next

        print("    11 10  9  8  7  6 ")
        print("+--+--------------+--+")
        print(f"|{n0_has_quan:2}|{a[11]:2}|{a[10]:2}|{a[9]:2}|{a[8]:2}|{a[7]:2}|{n6_has_quan:2}|")
        print(f"|{a[0]:2}|--------------|{a[6]:2}|")
        print(f"|  |{a[1]:2}|{a[2]:2}|{a[3]:2}|{a[4]:2}|{a[5]:2}|  |")
        print("+--+--------------+--+")
        print("  0  1  2  3  4  5")

    def get_state(self):
        """
        Output:
            state:  array of length 12. 
                    From 0->11 include the value of n0->n11. 
                    From 12->13 include the nodeType of n0 and n6.
        """
        state = []

        cur = self.llist.head
        
        for i in range(12):
            state.append(cur.data[0])
            cur = cur.next

        state.append(self.llist.head.data[1])
        state.append(self.llist.head.next.next.next.next.next.next.data[1])

        return state

    def load_state(self, state):
        # TODO
        return

class Player:
    def __init__(self, points=0):
        self.points = points

    
    def play(self, table, move):
        # TODO
        return
