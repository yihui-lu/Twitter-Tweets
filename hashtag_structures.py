'''
Task_2
Yihui Lu
20200412
'''

from T2_linked_list import *
from T2_bst import *
from T2_hash_table import *



#=========================================================================
class Tweet(object):
    def __init__(self, text, hashtags):
        self.__text = text
        self.__hashtags = hashtags
    def get_text(self):
        return self.__text
    def get_hashtags(self):
        return self.__hashtags
    def __str__(self):
        return "{}: {}".format(self.__text, self.__hashtags)




#=========================================================================
class Hashtag_Record(object):
    def __init__(self, tag):
        self.__tag = tag
        self.__tweets = []
    def get_tag(self):
        return self.__tag
    def get_tweets(self):
        return self.__tweets
    def add_tweet(self, tweet):
        self.__tweets.append(tweet)
    def __hash__(self):
        return hash(self.__tag)
    def __repr__(self):
        return "{} ({} tweets)".format(self.__tag, len(self.__tweets))
    def __eq__(self, other):
        return other != None and self.__tag == other.__tag
    def __lt__(self, other):
        return other != None and self.__tag < other.__tag
    def __gt__(self, other):
        return other != None and self.__tag > other.__tag


#=========================================================================
class Hashtag_List(list):

    def sorted_by_num_tweets(self):
        '''
        H.sorted_by_num_tweets() --> Hashtag_List
        Returns a copy of this Hashtag_List, in order from most Tweets to least.
        '''
        return Hashtag_List.__quick_sort(self)
    def __quick_sort(l):
        '''Hashtag_List.__quick_sort(list) --> Hashtag_List
        A helper method for sorted_by_num_tweets using quick sort.'''
        if len(l) <= 1:
            return l
        pivot = Hashtag_List()
        pivot.append(l[len(l)-1]) #pivot is the last item in the list
        lesser = Hashtag_List()
        greater = Hashtag_List()
        for i in range(len(l)-1): #for each index in the list (without the last position)
            if len(l[i].get_tweets()) < len(pivot[0].get_tweets()): 
            #num of Tweets at index < num of Tweets at pivot
                lesser.append(l[i])
            elif len(l[i].get_tweets()) > len(pivot[0].get_tweets()): 
            #num of Tweets at index > num of Tweets at pivot
                greater.append(l[i])
            else:
                pivot.append(l[i])
        htl = Hashtag_List() #extend in order from most->least
        htl.extend(Hashtag_List.__quick_sort(greater)) #sort the greater half
        htl.extend(pivot)
        htl.extend(Hashtag_List.__quick_sort(lesser)) #sort the lesser half
        return htl
        



#=========================================================================
class Hashtag_LinkedList(LinkedList):

    def as_list(self):
        '''
        H.as_list() --> Hashtag_List
        Return a Hashtag_List containing all items in this structure, 
        in increasing order of hashtag.
        '''
        l = Hashtag_List()
        temp = self.get_first()
        while temp != None: #while temp is a node
            l.append(temp.get_data()) #add the Hashtag_Record to the Hashtag_List
            temp = temp.get_next() #reset temp to the next node
        l.sort()
        return l


   
    def get_top_hashtag(self):
        '''
        H.get_top_hashtag() --> Hashtag_Record
        Return the Hashtag_Record (or one of) that has the most Tweets,
        or None if the structure is empty.
        '''        
        temp = self.get_first()
        if temp != None: #not empty
            top = temp
            while temp != None:
                if len(temp.get_data().get_tweets()) > len(top.get_data().get_tweets()): 
                #compare number of tweets of each Hashtag_Record
                    top = temp
                temp = temp.get_next() #reset temp to the next node
            return top.get_data()



    def reverse(self):
        '''
        H.reverse() --> None
        Reverse the order of all items in this Hashtag_LinkedList.
        '''
        temp = self.get_first()
        if temp != None: #if list is not empty
            nxt = temp.get_next()
            if nxt != None: #if list contains more than one element
                prev = temp 
                temp = nxt               
                nxt = temp.get_next() #total of three references: prev, temp, nxt
                prev.set_next(None) #the head becomes the tail, set its next to None
                while nxt != None:
                    temp.set_next(prev) #reverse the link, prev become the next of temp (instead of nxt)
                    prev = temp
                    temp = nxt
                    nxt = temp.get_next() #move the three references down the list
                #exit the while loop, temp is the tail of the original LinkedList
                temp.set_next(prev) #reverse the link
                self.set_first(temp) #set temp as the head
        


    def get_nth(self, n):
        '''
        H.get_nth(int) --> Hashtag_Record
        Return the Hashtag_Record in the n-th position in this list,
        or None if there is no n-th position.
        '''
        if n>=0: #negative position is not in list
            count = 0
            temp = self.get_first()
            while temp != None and count < n: #temp is a node and counted position < given position
                count += 1
                temp = temp.get_next()
            if count == n and temp != None: #node is not None at given position
                return temp.get_data()
            #else: return None


    def size(self):
        '''
        H.size() --> int
        Return the size of this Hashtag_LinkedList.
        Due to recursive implementation, may cause StackOverflowError on large lists.
        '''
        return Hashtag_LinkedList.__size_helper(self.get_first())
    def __size_helper(node):
        '''Recursive helper method of size.'''
        if node == None: #empty sublist
            return 0
        else:
            return 1+ Hashtag_LinkedList.__size_helper(node.get_next()) #1 (one node) + size of sublist starting from the next node




#=========================================================================
class Hashtag_BSTree(BSTree):

    def as_list(self):
        '''
        H.as_list() --> Hashtag_List
        Return a Hashtag_List containing all items in this structure, 
        in increasing order of hashtag.
        '''
        return Hashtag_BSTree.__as_list_helper(Hashtag_List(), self.get_root())
    def __as_list_helper(l,subroot):
        if subroot != None: #in-order traversal
            Hashtag_BSTree.__as_list_helper(l,subroot.get_left()) 
            #call the helper itself and append to the list starting from the left subtree
            l.append(subroot.get_data()) #append the subroot
            Hashtag_BSTree.__as_list_helper(l,subroot.get_right()) #call itself to append the right subtree
            return l
    
    

    def get_top_hashtag(self):
        '''
        H.get_top_hashtag() --> Hashtag_Record
        Return the Hashtag_Record (or one of) that has the most Tweets,
        or None if the structure is empty.
        '''
        l = self.as_list()
        if l != []: #not empty
            top = l[0]
            for i in l: #for each Hashtag_Record
                if len(i.get_tweets()) > len(top.get_tweets()):
                #compare num of tweets with the top, if greater, set top to current Hashtag_Record
                    top = i
            return top
            
    

    def balance(self):
        '''
        H.balance() --> None
        Balances the tree to minimize the depth, and make each level as full
        as possible.
        '''
        l = self.as_list() #create a list of all values
        self.empty() 
        self.__balance_helper(l)     
    def __balance_helper(self, l):
        if l != []: #not empty
            mid = len(l)//2
            self.insert(l[mid]) #insert the middle value
            self.__balance_helper(l[:mid]) #call to insert the left half
            self.__balance_helper(l[mid+1:]) #right half



    def get_leaves(self):
        '''
        H.get_leaves() --> Hashtag_List
        Returns a Hashtag_List of all the Hashtable_Records that are in the leaves.
        '''        
        return Hashtag_BSTree.__get_leaves_helper(self.get_root(),Hashtag_List())
    def __get_leaves_helper(subroot,l):
        if subroot != None:
            if subroot.get_left() == None and subroot.get_right() == None: #if leaf
                l.append(subroot.get_data()) #add Hashtag_Record to the HTList
            else: #if not leaf, check left and right children
                l.extend(Hashtag_BSTree.__get_leaves_helper(subroot.get_left(),Hashtag_List()))
                l.extend(Hashtag_BSTree.__get_leaves_helper(subroot.get_right(),Hashtag_List()))  
        return l
    
    

    def count_one_child(self):
        '''
        H.count_one_child() --> int
        Returns the number of nodes that have exactly one child.
        The larger this number is, the (potentially) more unbalanced it is.
        '''
        if self.get_root() == None: #if empty tree
            return 0
        return Hashtag_BSTree.__count_one_helper(self.get_root())
    def __count_one_helper(node):
        if node.get_left() == None:
            if node.get_right() == None: #no children
                return 0
            else: #one child on the right
                return 1 + Hashtag_BSTree.__count_one_helper(node.get_right()) #check right child
        elif node.get_right() == None: #one child on the left
            return 1 + Hashtag_BSTree.__count_one_helper(node.get_left()) #check left child
        else: #two children
            return Hashtag_BSTree.__count_one_helper(node.get_left())+ Hashtag_BSTree.__count_one_helper(node.get_right()) #check both children



#=========================================================================
class Hashtag_HashTable(HashTable):
    
    def __init__(self, size, scalable=False):
        '''
        __init__(int, bool)
        Construct a custom HashTable, with 'size' buckets.
        When scalable is True, this table will double in size when the
        load factor exceeds 1.0 from an insert.
        '''           
        HashTable.__init__(self, size)  #construct parent
        buckets = []                    #temporary holder
        for i in range(size):
            #these buckets are Hashtag_LinkedLists
            buckets.append(Hashtag_LinkedList())
        self.set_empty_buckets(buckets)       #update parent property
        self.__scalable = scalable


    def as_list(self):
        '''
        H.as_list() --> Hashtag_List
        Return a Hashtag_List containing all items in this structure, 
        in increasing order of hashtag.
        '''
        l = Hashtag_List()
        for i in self.get_buckets():
            l.extend(i.as_list()) #create a list for each bucket and combine the lists
        l.sort()
        return l

    
    
    def get_top_hashtag(self):
        '''
        H.get_top_hashtag() --> Hashtag_Record
        Return the Hashtag_Record (or one of) that has the most Tweets,
        or None if the structure is empty.
        ''' 
        l = Hashtag_List()
        for i in self.get_buckets():
            l.extend(i.as_list()) #create a list containing all items
        if l != []: #if not empty
            top = l[0] #set the first item as top
            num_tweets = len(top.get_tweets()) #number of tweets of the current top
            for i in l:
                if len(i.get_tweets()) > num_tweets: #compare num of tweets
                    top = i #reset top if Hashtag_Record at index has more tweets
                    num_tweets = len(top.get_tweets())
            return top

    
    
    def get_largest_bucket(self):
        '''
        H.get_largest_bucket() --> Hashtag_LinkedList
        Return the largest bucket in this table, or None if the structure is empty.
        ''' 
        buckets = self.get_buckets()
        if buckets != []: #not empty
            lg = buckets[0]
            size = lg.size()
            for i in buckets[1:]: #for each bucket in the rest of buckets
                if i.size() > size: #if the bucket is larger
                    lg = i #set the largest to current bucket
                    size = lg.size()
            return lg

    

    def get_percent_above_load_factor(self):
        '''
        H.get_percent_above_load_factor() --> float
        Return the decimal percentage of buckets whose size is more
        than the load factor (in other words, more than the average).
        ''' 
        buckets = self.get_buckets()
        if buckets != []: #load factor will crash if there aren't any buckets
            load = self.load_factor()
            count = 0
            for i in buckets: #for each bucket
                if i.size() > load: #if the size of the bucket exceeds the load factor
                    count += 1 
            return count/len(buckets) #percentage in decimal



    def insert(self, ht_record):
        '''
        H.insert(Hashtag_Record) --> None
        Insert the given record in this table.  Scale the table size if necessary.
        ''' 
        HashTable.insert(self, ht_record)
        if self.__scalable == True and self.load_factor() >= 1: 
        #only scale the table if it's set to scalable when the load factor exceeds 1.0
            l = self.as_list() #store all items in a list
            empty = [] #create an empty set of buckets (2 times the size)
            for i in range(2*len(self.get_buckets())):
                empty.append(Hashtag_LinkedList())         
            self.set_empty_buckets(empty) #empty out the hashtable
            for i in l:
                HashTable.insert(self, i) #insert all items 
        
