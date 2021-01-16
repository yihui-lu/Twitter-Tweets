class ListNode(object):
    def __init__(self, data, link):
        self.__data = data
        self.__link = link
        
    def get_next(self):
        return self.__link
    
    def set_next(self, node):
        self.__link = node
        
    def get_data(self):
        return self.__data
    
    def set_data(self, data):
        self.__data = data
        
    def __str__(self):
        s = "[{}]".format(self.__data)
        if self.__link != None:
            s += "--->"
        return s


class LinkedList(object):
    def __init__(self):
        '''
        Construct an empty linked list.
        '''
        self.__first = None

    def get_first(self):
        '''
        LL.get_first() --> ListNode
        Returns a reference to the first nide in the list.
        '''
        return self.__first

    def set_first(self, node):
        '''
        LL.set_first(ListNode) --> None
        Set the first node in the list to the given node.
        '''
        self.__first = node
        
    def is_empty(self):
        '''
        LL.is_empty() --> bool
        Returns True if this LinkedList is empty, or False otherwise.
        '''
        return self.__first == None
    
    def insert(self, value):
        '''
        LL.insert(object) --> None
        Inserts the given value at the front of this linked list.
        '''
        self.__first = ListNode(value, self.__first)
    
    def size(self):
        '''
        LL.size() --> int
        Returns the number of items in this LinkedList.
        '''
        count = 0
        current = self.__first
        while current != None:
            count += 1
            current = current.get_next()
        return count
    
    def __str__(self):
        '''
        LL.__str__() or str(LL) --> str
        Returns a string representation of this LinkedList
        '''
        s = ""
        current = self.__first
        while current != None:
            s += str(current)
            current = current.get_next()
        return s

    def retrieve(self, value):
        '''
        LL.retrieve(object) --> object
        Returns a reference to the first value that is equal to the given
        argument, or None otherwise.
        '''
        current = self.__first
        while current != None and current.get_data() != value:
            current = current.get_next()
        if current != None:
            return current.get_data()
        

    def __contains__(self, value):
        '''
        LL.contains(object)  or  object in LL --> bool
        Returns True if this LinkedList contains the given object, or False otherwise.
        '''
        current = self.__first
        contains = False
        while current != None and current.get_data() != value:
            current = current.get_next()
        return current != None
    

    def remove(self, value):
        '''
        LL.remove(object) --> None
        Removes the specified object from the LinkedList, if present.
        '''
        current = self.__first
        if current == None:
            return
        elif current.get_data() == value:
            self.__first = current.get_next()
        else:
            while current.get_next() != None and current.get_next().get_data() != value:
                current = current.get_next()
            if current.get_next() == None:
                return
            else:
                current.set_next(current.get_next().get_next())
