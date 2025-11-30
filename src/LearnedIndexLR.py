# LearnedIndexLR.py
# THIS LEARNED INDEX IMPLEMENTS SIMPLE LINEAR REGRESSION
# a * x * b

class LearnedIndexLR:
    def __init__(self):
        self.keys = []
        self.values = []

        self.a = 0
        self.b = 0
        self.maxError = 0

    # LOAD THEN SORT INTO KEYS AND VALUES
    def loadDataFromFile(self, filepath):
        pass

