'''
Task_2
Yihui Lu
20200412
'''

from hashtag_structures import *
import unittest

class Test_Hashtag_LinkedList_Size(unittest.TestCase):
    def test_size_empty(self):
        l = Hashtag_LinkedList()
        return self.assertEqual(0, l.size(), "Size: empty LinkedList")
    def test_size_single(self):
        l = Hashtag_LinkedList()
        l.insert('1')
        return self.assertEqual(1, l.size(), "Size: LinkedList with one item")
    def test_size_many(self):
        l = Hashtag_LinkedList()
        for i in ['1','2','3','4', '5']:
            l.insert(i)
        return self.assertEqual(5, l.size(), "Size: LinkedList with many items")

class Test_Hashtag_BSTree_CountOneChild(unittest.TestCase):
    def test_count_one_child_empty(self): 
        t = Hashtag_BSTree()
        return self.assertEqual(0, t.count_one_child(), "Count one child: empty BSTree")
    def test_count_one_child_root(self): #BSTree with only one item (root)
        t = Hashtag_BSTree()
        t.insert('root')
        return self.assertEqual(0, t.count_one_child(), "Count one child: BSTree with one item")
    def test_count_one_child_all(self): #all items in the tree has one child
        t = Hashtag_BSTree()
        for i in [5,2,3,4]:
            t.insert(i)
        return self.assertEqual(3,t.count_one_child(), "Count one child: all items in the BSTree has one child")
    def test_count_one_child_none(self): #no items in the BSTree have one child
        t = Hashtag_BSTree()
        for i in [5,3,7,2,4]:
            t.insert(i)
        return self.assertEqual(0, t.count_one_child(), "Count one child: no item in the BSTree has only one child")
    def test_count_one_child_normal(self): #all three cases (no children, one child, two children) occur in the tree
        t = Hashtag_BSTree()
        for i in [5,3,7,2]:
            t.insert(i)
        return self.assertEqual(1, t.count_one_child(), "Count one child: normal BSTree")

unittest.main()