# BPlusTree.py
# IMPLEMENT ONLY THE STRUCTURE OF B+ TREE,
# AS THIS FILE WILL BE CALLED FROM main.py  

class TreeNode:
    def __init__(self, nodeOrder: int):
        self.nodeOrder = nodeOrder
        self.isLeaf = False
        self.indexKeys = []
        self.parentNode = None

    def setOrder(self, nodeOrder):
        self.nodeOrder = nodeOrder

    def setIsLeafTrue(self):
        self.isLeaf = True
    def setIsLeafFalse(self):
        self.isLeaf = False

    def addIndexKey(self, keyValue):
        self.indexKeys.append(keyValue)

    def setParentNode(self, parentNode):
        self.parent = parentNode

