from T2_linked_list import *

class HashTable(object):

    def __init__(self, size):
        '''Construct an empty HashTable with the given number of buckets.'''        
        self.__num_records = 0
        self.__size = size
        self.__buckets = []
        for i in range(size):
            self.__buckets.append(LinkedList())

    def get_buckets(self):
        '''
        H.get_buckets() --> list
        Return a reference to the list of buckets.
        '''
        return self.__buckets

    def set_empty_buckets(self, buckets):
        '''
        H.set_empty_buckets(list) --> None
        Reset the list of buckets to the given list of empty buckets.
        '''
        self.__buckets = buckets
        self.__size = len(buckets)
        self.__num_records = 0
    
    def __str__(self):
        '''
        H.__str__() --> str
        Return a string representation of this hashtable.
        '''
        out = ""
        for i in range(self.__size):
            out += "[{:-^3}]:={}\n".format(i, self.__buckets[i])
        return out.strip()
          
    def insert(self, value):
        '''
        H.insert(object) --> None
        Insert the hashable object into this table.
        '''
        bucket = hash(value)%self.__size
        self.__buckets[bucket].insert(value)
        self.__num_records += 1
    
    
    def retrieve(self, value):
        '''
        H.retrieve(object) --> object
        Return a reference to the item in the table that is equivalent to
        the given hashable object.
        '''
        bucket = hash(value)%self.__size
        return self.__buckets[bucket].retrieve(value)
    
    def __contains__(self, value):
        '''
        H.contains(object) --> bool
        Return True if an item is in the table that is equivalent to the given
        hashable object, or False otherwise.
        '''
        bucket = hash(value)%self.__size
        return self.__buckets[bucket].contains(value)
 
        
    def load_factor(self):
        '''
        H.load_factor() --> float
        Return the load factor of this table.
        '''
        return self.__num_records/self.__size
