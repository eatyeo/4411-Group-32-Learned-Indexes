# BPlusTree.py
# IMPLEMENT ONLY THE STRUCTURE OF B+ TREE,
# AS THIS FILE WILL BE CALLED FROM main.py  

class TreeNode:
    def __init__(self, isLeaf = False):
        self.isLeaf = isLeaf
        self.keys = []

        # INTERNAL NODE, POINTS TO CHILDREN NODES
        self.childrenNodes = []

        # LEAD NODE, POINTS TO NEXT LEAF
        self.nextLeaf = None 

        # Will be set by the tree
        self.parent = None
        self.nodeOrder = None

    def getIfFull(self, maxKeys: int):
        return len(self.keys) >= maxKeys
        
    def getKeyCount(self):
        return len(self.keys)

    def getIsInternal(self):
        return not self.isLeaf

    """
    Insert the key and value into a leaf node making sure the keys are sorted.
    If key already exists, append value to the list
    Else, Insert key with the new value as a list
    """
    def addIndexKey(self, key, value):
        if self.getIsInternal():
            raise ValueError("Can't add index keys to non leaf nodes")
    
        # No keys exist in this node. Append a key to keys and append value as a list to childrenodes
        if not self.keys:
            self.keys.append(key)
            self.childrenNodes.append([value])
            return
        
        #For sort, find the correct insertion position
        sorted_position=0
        while sorted_position<len(self.keys)and self.keys[sorted_position] < key:
            sorted_position+=1

        #If the key is already there, append value to the list at the correct position
        if sorted_position < len(self.keys) and self.keys[sorted_position] == key:
            self.childrenNodes[sorted_position].append(value)
        #Key not there, insert the key and value at sorted positions
        else:
            self.keys.insert(sorted_position, key)
            self.childrenNodes.insert(sorted_position, [value])

    def setOrder(self, nodeOrder):
        self.nodeOrder = nodeOrder

    def setIsLeafTrue(self):
        self.isLeaf = True
    def setIsLeafFalse(self):
        self.isLeaf = False
    def setParentNode(self, parentNode):
        self.parent = parentNode

"""
 Simple B+-tree index.
- Keys are values from the dataset (e.g., 1188).
- Leaf nodes store lists of positions where each key appears in the original data.
"""
class BPlusTree:
    def __init__(self, order=4):
        self.order = order # order = max number of children per internal node
        self.maxKeys = order - 1 # Max keys per node
        self.root = TreeNode(isLeaf=True) # Starting with one empty leaf
        self.root.setOrder(order)

    def buildIndex(self, dataList):
        #Build the B+Tree index from dataset values
        for position, key in enumerate(dataList):
            self.addIndex(key, position)

    def getIndexPosition(self, key):
        #Return list of positions the key is, or None if not found
        leaf = self.find_leaf(self.root, key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return list(leaf.childrenNodes[i])
        return None
    
    def addIndex(self, key, position):
        #Insert a new (key, position) pair into the position
        leaf = self.find_leaf(self.root, key)
        leaf.addIndexKey(key, position)

        # SPlit the leaf since it would violate max keys rule
        if leaf.getIfFull(self.maxKeys):
            self.split_leaf(leaf)

    """
    Remove key and all of its positions from the index (if it exists).
    Deleting from the leaf and only shrinking the root if it becomes empty.
    """
    def removeIndex(self, key):
        leaf = self.find_leaf(self.root, key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                leaf.keys.pop(i)
                leaf.childrenNodes.pop(i)
                break

        # If Root empty an empty leaf, return
        if leaf is self.root and leaf.getKeyCount() == 0 and not leaf.getIsInternal():
            return
        
    def getRange(self, keyStart, keyEnd):
    #Return list of positions for all keys k where key1 <= k <= key2

        resultPositions = []
        leaf = self.find_leaf(self.root, keyStart)

        while leaf is not None:
            # merging the 2 lists with zip than iterating over the keys and positions for that key
            for k, positions in zip(leaf.keys, leaf.childrenNodes):

                # if the key is inside the range specified, add positions
                if keyStart <= k <= keyEnd:
                    resultPositions.extend(positions)

                # key end is passed, return back
                elif k > keyEnd:
                    return resultPositions
            leaf = leaf.nextLeaf

        return resultPositions
    
    #Traverse down from node to the leaf that contains the key
    def find_leaf(self, node, key):

        # Keep going down while we are at an internal node.
        while node.getIsInternal():
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.childrenNodes[i]
        return node

    """
    Split a full leaf node into two leaves and push up the first key
    """
    def split_leaf(self, leaf):
        #New leaf that will become the right sibling
        new_leaf = TreeNode(isLeaf=True)
        new_leaf.setOrder(self.order)
        new_leaf.nextLeaf = leaf.nextLeaf
        leaf.nextLeaf = new_leaf

        total_keys = leaf.getKeyCount()
        split_index = total_keys // 2

        # Move second half of keys and values into new_leaf
        new_leaf.keys = leaf.keys[split_index:]
        new_leaf.childrenNodes = leaf.childrenNodes[split_index:]
        # First half stays in the original leaf
        leaf.keys = leaf.keys[:split_index]
        leaf.childrenNodes = leaf.childrenNodes[:split_index]

        new_leaf.parent = leaf.parent

        # First key of the new leaf will be the parent
        new_parent_key = new_leaf.keys[0]

        # Case 1: Leaf was root.
        if leaf.parent is None:
            # Give it a new root
            new_root = TreeNode(isLeaf=False)
            new_root.setOrder(self.order)
            new_root.keys = [new_parent_key]
            new_root.childrenNodes = [leaf, new_leaf]
            leaf.parent = new_root
            new_leaf.parent = new_root
            self.root = new_root
        # Case 2: Leaf has a parent
        else:
            #Insert new parent key into the parent node
            self.insert_into_internal(leaf.parent, new_parent_key, new_leaf)

    """
    Insert key and a pointer to right child into an internal node.
    If full, split
    """
    def insert_into_internal(self, node, key, right_child):
        # Find position for key to maintain the sorted order
        sorted_position = 0
        while sorted_position < len(node.keys) and node.keys[sorted_position] < key:
            sorted_position += 1

        node.keys.insert(sorted_position, key)
        node.childrenNodes.insert(sorted_position + 1, right_child)
        right_child.parent = node

        if node.getIfFull(self.maxKeys):
            self.split_internal(node)

    """
    Split a full internal node into two nodes and make the middle key
    a parent node
    """
    def split_internal(self, node):

        new_internal = TreeNode(isLeaf=False)
        new_internal.setOrder(self.order)

        total_keys = node.getKeyCount()
        mid_index = total_keys // 2

        new_parent_key = node.keys[mid_index]

        new_internal.keys = node.keys[mid_index + 1:]
        new_internal.childrenNodes = node.childrenNodes[mid_index + 1:]

        for child in new_internal.childrenNodes:
            child.parent = new_internal

        # Left side stays in 'node'
        node.keys = node.keys[:mid_index]
        node.childrenNodes = node.childrenNodes[:mid_index + 1]

        new_internal.parent = node.parent

        # Case 1: Node was the root
        if node.parent is None:
            # Create new root and make node and the new internal into its children
            new_root = TreeNode(isLeaf=False)
            new_root.setOrder(self.order)
            new_root.keys = [new_parent_key]
            new_root.childrenNodes = [node, new_internal]
            node.parent = new_root
            new_internal.parent = new_root
            self.root = new_root

        # Case 2: Node has a parent
        else:
            self.insert_into_internal(node.parent, new_parent_key, new_internal)