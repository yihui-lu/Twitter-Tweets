class BSTNode(object):
    
    def __init__(self, data):
        self.__data = data
        self.__left = None
        self.__right = None

    def get_data(self):
        return self.__data
    def set_data(self, data):
        self.__data = data
    def get_left(self):
        return self.__left
    def set_left(self, node):
        self.__left = node
    def get_right(self):
        return self.__right
    def set_right(self, node):
        self.__right = node


class BSTree(object):
    
    def __init__(self):
        '''Construct an empty binary search tree.'''        
        self.__root = None
        
    def get_root(self):
        '''T.get_root() --> BSTNode
        Return a reference to the root node in the tree (or None).
        '''
        return self.__root
        
    def empty(self):
        '''T.empty() --> None
        Reset this tree to be empty.
        '''
        self.__root = None

    def insert(self, val):
        '''T.insert(data) --> None
        Insert the data into tree.
        '''
        new_node = BSTNode(val)
        temp = self.__root
        
        #first insert
        if temp == None:
            self.__root = new_node

        #'standard' case
        else:
            inserted = False
            while temp != None:
                if val < temp.get_data():
                    #insert the new node if we have reached the 'leaves'
                    if temp.get_left() == None:
                        temp.set_left(new_node)
                        temp = None  #so that the loop will end now
                    else:
                        temp = temp.get_left()
                else:
                    if temp.get_right() == None:
                        temp.set_right(new_node)
                        temp = None  #so that the loop will end now
                    else:
                        temp = temp.get_right()


    def __contains__(self, data):
        '''T.__contains__(data) or data in T --> bool
        Return True if data is in the tree, or False otherwise.
        '''
        temp = self.__root
        while temp != None and data != temp.get_data():
            if data < temp.get_data():
                temp = temp.get_left()
            else:                
                temp = temp.get_right()
        return temp != None 
    
    
    def retrieve(self, data):
        '''T.retrieve(data) --> data
        Return a reference to the data in the tree, if one is equal to the
        datas passed as an argument.
        '''
        temp = self.__root
        while temp != None and data != temp.get_data():
            if data < temp.get_data():
                temp = temp.get_left()
            else:                
                temp = temp.get_right()
        if temp != None:
            return temp.get_data()


    def __str__(self):
        ''' T.__str__() or str(T) --> str
        Returns a string representation of this in a 'sideways' representation,
        with spaces to show depth.
        '''        
        return self.__str_helper(self.__root, 0)
    def __str_helper(self, node, depth):
        '''A helper method for the __str__() method.
        Takes the 'root' of a sub-part of the tree (just a BSTNode)
        and the current 'depth' of this sub-root in the tree (for formatting).
        Base case: sub-root is None, so we're done that branch
        Recursive case: re-call this helper method on each 'side' of this subroot,
                        inserting itself in-between.  Add 1 to depth for each call.
        '''        
        if node != None: #if I haven't gone off end of a branch
            #print right subtree, print me, print left subtree
            right = self.__str_helper(node.get_right(), depth+1)
            me = "{}[{}]\n".format("    "*depth, node.get_data())
            left = self.__str_helper(node.get_left(), depth+1)
            return right + me + left
        else:
            return ""


    def maximum(self):
        '''T.maximum() --> data
        Return the 'maximum' data in the tree.
        This is the data farthest to the 'right'.
        '''
        temp = self.__root
        while temp.get_right() != None:
            temp = temp.get_right()
        return temp.get_data()
    

    def minimum(self):
        '''T.minimum() --> data
        Return the 'minimum' data in the tree.
        This is the data farthest to the 'left'.
        '''
        temp = self.__root
        while temp.get_left() != None:
            temp = temp.get_left()
        return temp.get_data()
        
                    
    def size(self):
        '''T.size() --> int
        Return the number of nodes in this tree.
        '''
        return self.__size_helper(self.__root)
    def __size_helper(self, node):
        '''A helper method for the size() method.
        Takes the 'root' of a sub-part of the tree (just a BSTNode)
        and returns how many nodes are in that subtree, including that node
        '''
        if node == None:
            return 0
        else:
            return self.__size_helper(node.get_left()) + 1 + self.__size_helper(node.get_right())
    

    def depth(self):
        '''T.depth() --> int
        Return the depth of the largest 'branch' in this tree.
        '''
        return self.__depth_helper(self.__root) #replace this once implemented
    def __depth_helper(self, node):
        '''A helper method for the depth() method.
        Takes the 'root' of a sub-part of the tree (just a BSTNode)
        and returns the larger of the depth datas of the left and right
        subtrees of that node.
        '''
        if node == None:
            return 0
        left_size = 1 + self.__depth_helper(node.get_left())
        right_size = 1 + self.__depth_helper(node.get_right())
        return max(left_size, right_size)


    def average_depth(self):
        '''T.average_depth() --> float
        Return the average depth of all the leaves in this tree.
        '''        
        if self.__root == None:
            return 0
        else:
            leaf_depths = self.__avg_depth_helper(self.__root, 0)
            return sum(leaf_depths)/len(leaf_depths)
    def __avg_depth_helper(self, node, depth_so_far):
        '''A helper method for the average_depth() method.
        Takes the 'root' of a sub-part of the tree (just a BSTNode)
        and the depth of that node in the tree, and returns a list of all the
        depths of leaves in this sub-part of the tree.
        '''        
        depth_so_far += 1
        to_return = []
        if node == None:
            return to_return
        if node.get_left() == None and node.get_right() == None:
            #node is a leaf
            to_return.append(depth_so_far)
        
        to_return.extend(self.__avg_depth_helper(node.get_right(), depth_so_far))
        to_return.extend(self.__avg_depth_helper(node.get_left(), depth_so_far))
        return to_return