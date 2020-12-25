class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        #initializes a dummy node and creates a self.head attribute
        self.head = Node(None)
        self.head.next = self.head
        self.head.prev = self.head
        

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        if self.head.next == self.head and self.head.prev == self.head: #if self.head.next == self.head then empty
            return True

        return False

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance'''
        node = Node(item) #creates a node item
        
        iteration_node = self.head.next
        while iteration_node != self.head: #traversing through the list for a bigger item
            if iteration_node.item == node.item: #if items are equal
                return False

            elif iteration_node.item < item: #if the item is the largest in list
                iteration_node = iteration_node.next

            else:
                y = 'y'
                break
        

        #runs when none of the above condidtions are true
        node.prev = iteration_node.prev
        node.next = iteration_node
        iteration_node.prev.next = node
        iteration_node.prev = node
        return True

        

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
          returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''

        iteration_node = self.head.next
        while iteration_node != self.head: #traversing through list
            if iteration_node.item == item: #if item in node is item being removed, remove it and return True
                prev_node = iteration_node.prev
                next_node = iteration_node.next
                prev_node.next = next_node
                next_node.prev = prev_node
                return True

            iteration_node = iteration_node.next

        return False #return false if item not found


    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        if item is None:
            return None

        iteration_node = self.head.next
        index_num = 0 #declares a variable for the possible index of item
        while iteration_node != self.head: #traverses through the list
            if iteration_node.item == item: #returns the index if found
                return index_num

            elif iteration_node.item > item:
                y = 'y'
                break

            iteration_node = iteration_node.next 
            index_num += 1

        return None #returns false if item is not found


    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0: #if input is invalid
            raise IndexError

        iteration_node = self.head.next
        for i in range(index+1): #for loop that makes sure that the input is not greater then the length of the list
            if iteration_node == self.head: #if input is invalid
                raise IndexError

            if i == index: #if index is found removes object from the list and returns item
                prev_node = iteration_node.prev
                next_node = iteration_node.next
                prev_node.next = next_node
                next_node.prev = prev_node
                return iteration_node.item #returns item from popped node

            iteration_node = iteration_node.next #increments the iteration node

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return False

        return self.search_helper(self.head.next, item)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''

        list_of_items = [] #creates variable for soon to be returned list
        iteration_node = self.head.next
        while iteration_node != self.head: #traverses through the OrderedList appending to the new python list
            list_of_items.append(iteration_node.item)
            iteration_node = iteration_node.next

        return list_of_items #returns python list


    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        if self.is_empty():
            return []

        return self.python_list_reversed_helper(self.head.next)

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head)




# Helper Funcs:
        
    def size_helper(self, node): #helper func for size
        if node.next == self.head: #base case
            return 0 

        return self.size_helper(node.next) + 1 #returns 1 plus the returned value of the recursive call

    def search_helper(self, node, item): #helper function for search
        if node.item == item: #base case
            return True

        if node.item > item:
            return False

        if node.next != self.head: #if next object in list is not self.head then call recursively
            return self.search_helper(node.next, item)

        return False #return false if not found 

    def python_list_reversed_helper(self, node):
        if node.next == self.head: #base case
            return [node.item]

        #concatinates a list of returned items(in reverse order) with the current item in also in reversed order
        return self.python_list_reversed_helper(node.next) + [node.item] 