# HashIndex.py
# IMPLEMENTATION OF A HASH INDEX STRUCTURE
# Uses a standard Python dictionary

class HashIndex:
    def __init__(self):
        # Key = The value from the dataset
        # Value = List of positions (rows) where this value appears in the original file
        self.hashTable = {}

    # POPULATES THE HASH TABLE FROM A GIVEN LIST OF DATA
    def buildIndex(self, dataList: list):
        self.hashTable.clear()
        for position, value in enumerate(dataList):
            if value not in self.hashTable:
                self.hashTable[value] = [position]
            else:
                self.hashTable[value].append(position)

    # RETURNS THE LIST OF POSITIONS FOR A GIVEN KEY (OR NONE IF NOT FOUND)
    def getIndexPosition(self, key):
        return self.hashTable.get(key, None)

    # ADDS A NEW KEY-POSITION PAIR TO THE INDEX
    def addIndex(self, key, position):
        if key not in self.hashTable:
            self.hashTable[key] = [position]
        else:
            self.hashTable[key].append(position)

    # REMOVES THE KEY AND ALL ITS POSITIONS FROM THE INDEX
    def removeIndex(self, key):
        if key in self.hashTable:
            del self.hashTable[key]