"""
Doubly Linked List implementation in Python

References:
- https://www.geeksforgeeks.org/doubly-linked-list/
"""

class Node:
    def __init__(self, data):
        self.data = data
        
        self.next = None
        self.prev = None


class DoublyLinkedList: 
    def __init__(self): 
        self.head = None

    def push(self, new_data): 
        new_node = Node(new_data) 

        new_node.next = self.head 
  
        # 4. change prev of head node to new_node 
        if self.head is not None: 
            self.head.prev = new_node 

        self.head = new_node 
  
    # Given a node as prev_node, insert a new node after 
    # the given node 
    def insertAfter(self, prev_node, new_data): 
  
        # 1. Check if the given prev_node is None 
        if prev_node is None: 
            print("the given previous node cannot be NULL")
            return 
  
        # 2. allocate new node 
        # 3. put in the data 
        new_node = Node(new_data) 
  
        # 4. Make net of new node as next of prev node 
        new_node.next = prev_node.next
  
        # 5. Make prev_node as previous of new_node 
        prev_node.next = new_node 
  
        # 6. Make prev_node ass previous of new_node 
        new_node.prev = prev_node 
  
        # 7. Change previous of new_nodes's next node 
        if new_node.next is not None: 
            new_node.next.prev = new_node 
  
    # Given a reference to the head of DLL and integer, 
    # appends a new node at the end 
    def append(self, new_data): 
  
        # 1. Allocates node 
        # 2. Put in the data 
        new_node = Node(new_data) 
  
        # 3. This new node is going to be the last node, 
        # so make next of it as None 
        new_node.next = None
  
        # 4. If the Linked List is empty, then make the 
        # new node as head 
        if self.head is None: 
            new_node.prev = None
            self.head = new_node 
            return 
  
        # 5. Else traverse till the last node 
        last = self.head 
        while(last.next is not None): 
            last = last.next
  
        # 6. Change the next of last node 
        last.next = new_node 
  
        # 7. Make last node as previous of new node 
        new_node.prev = last 
  
        return
  
    # This function prints contents of linked list 
    # starting from the given node 
    def printList(self, node): 


        print("\nTraversal in forward direction")
        while(node is not None): 
            print(node.data) 
            last = node 
            node = node.next
  
        print("\nTraversal in reverse direction")
        while(last is not None): 
            print(last.data) 
            last = last.prev 

    def getNodeAtPos(self, pos):
        chosenNode = self.head
        for i in range(pos):
            chosenNode = chosenNode.next
        return chosenNode
    
    def getDataAtPos(self, pos):
        return self.getNodeAtPos(pos).data

if __name__ == '__main__':
    llist = DoublyLinkedList() 
    
    # Insert 6. So the list becomes 6->None 
    llist.append(6) 
    
    # Insert 7 at the beginning. 
    # So linked list becomes 7->6->None 
    llist.push(7) 
    
    # Insert 1 at the beginning. 
    # So linked list becomes 1->7->6->None 
    llist.push(1) 
    
    # Insert 4 at the end. 
    # So linked list becomes 1->7->6->4->None 
    llist.append(4) 
    
    # Insert 8, after 7. 
    # So linked list becomes 1->7->8->6->4->None 
    llist.insertAfter(llist.head.next, 8) 
    
    print("Created DLL is: ") 
    llist.printList(llist.head) 
    
    # This code is contributed by Nikhil Kumar Singh(nickzuck_007) 