from vyperlogix.trees import BinarySearchTree

if (__name__ == "__main__"):
    tree = BinarySearchTree.BinaryTree()
    tree.add(4, "test1")
    tree.add(10, "test2")
    tree.add(23, "test3")
    tree.add(1, "test4")
    tree.add(3, "test5")
    tree.add(2, "test6")
    tree.sort()
    print tree.search(3)
    print tree.deleteNode(10)
    print tree.deleteNode(23)
    print tree.deleteNode(4)
    print tree.search(3)
    tree.sort()
    
