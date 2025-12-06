# LearnedIndexLR.py
# IMPLEMENTS LINEAR REGRESSION FOR A SINGLE COUNTRY
# https://www.geeksforgeeks.org/machine-learning/ml-linear-regression/
# https://www.w3schools.com/python/python_ml_linear_regression.asp

import math

class LearnedIndexLR:
    def __init__(self, indexList: list):
        self.indexList = indexList # CONSIDER SORTING IN ASC. ORDER
        self.indexPositions = []

        # CREATE INDEX OF INTS len(indexList)
        positionsAppend = 0
        for index in indexList:
            self.indexPositions.append(positionsAppend)
            positionsAppend += 1

        # THESE WILL BE USE FOR OUR [mx + b] LINEAR REGRESSION
        self.m = 0
        self.b = 0

        self.maxError = 0.0
        self.minError = 9999999999.9 # ANY HIGH VALUE
        self.maxPositiveError = 0.0
        self.maxNegativeError = 0.0

    # LOAD THEN SORT INTO KEYS AND VALUES
    def trainModel(self):

        # CALCULATE AVERAGES FOR LINEAR REGRESSION FORMULA
        numberOfPoints = len(self.indexList)
        # x, y => indexList, indexPositions
        avgIndex = sum(self.indexList) / numberOfPoints
        avgPosition = sum(self.indexPositions) / numberOfPoints

        # CALCULATE THE SLOPE
        numeratorSum = 0
        denominatorSum = 0
        for position in self.indexPositions:
            xCalc = self.indexList[position] - avgIndex
            # FORMULA FOR SLOPE IN DOCUMENT
            numeratorSum += xCalc * (position - avgPosition)
            denominatorSum += xCalc * xCalc
        self.m = numeratorSum / denominatorSum

        # CALCULATE THE INTERCEPT 
        self.b = avgPosition - self.m * avgIndex

    # OUTPUTS SLOPE AND INTERCEPT VALUES TO TERMINAL
    def printSlopeIntercept(self):
        print("\tself.m:\t" + str(self.m))
        print("\tself.b:\t" + str(self.b))

    # GETS THE MAX POSSIBLE ERROR RANGES
    def calculateErrorRanges(self):
        for position in self.indexPositions:
            predictedValue = self.predict(self.indexList[position])
            error = predictedValue - position

            # GET THE MAX ERROR IN POSITIVE AND NEGATIVE
            self.maxError = max(self.maxError, abs(error))
            self.minError = min(self.minError, abs(error))


            # NOW THE MAX ERROR IN POSITIVE OR NEGATIVE
            if error > 0:
                self.maxPositiveError = max(self.maxPositiveError, error)
            else:
                self.maxNegativeError = min(self.maxNegativeError, error)

    # OUTPUT ALL CALCULATED ERROR RANGES TO COMMAND LINE
    def printErrorRanges(self):
        print("MAX ABSOLUTE ERROR: " + str(self.maxError))
        print("MIN ABSOLUTE ERROR: " + str(self.minError))
        print("MAX POSITIVE ERROR: " + str(self.maxPositiveError))
        print("MAX NEGATIVE ERROR: " + str(self.maxNegativeError))

    # USE [year] TO PREDICT POSITION BY [mx + b]
    def predict(self, year: int):
        returnValue = self.m * year + self.b
        return returnValue
    
    # CALCULATES THE EXACT RANGES, THEN PERFORMS BINARY SEARCH
    def getIndexPosition(self, key):
        # GET THE PREDICTION
        prediction = self.predict(key)

        # COMPUTE POSSIBLE RANGE
        # ADDED MIN/MAX TO ENSURE CORRECT BOUNDS
        left = max(0, prediction + self.maxNegativeError)
        right = min(prediction + self.maxPositiveError, len(self.indexPositions) - 1)

        # ROUND MAX UPWARDS, ROUND MIN DOWNWARDS
        left = math.floor(left)
        right = math.ceil(right)

        # NOW DO BINARY SEARCH
        while left <= right:
            middle = (left + right) // 2
            if self.indexList[middle] == key:
                return middle
            elif self.indexList[middle] < key:
                left = middle + 1
            else:
                right = middle - 1

        # IF THIS IS REACHED, THEN INDEX WAS NOT FOUND
        return None

    # ADDS THE GIVEN KEY TO THE INDEX LIST
    def addIndex(self, key):
        # GET THE PREDICTION 
        prediction = self.predict(key)

        # COMPUTE POSSIBLE RANGE
        left = max(0, prediction + self.maxNegativeError)
        right = min(prediction + self.maxPositiveError, len(self.indexPositions) - 1)

        # ROUND MAX UPWARDS, ROUND MIN DOWNWARDS
        left = math.floor(left)
        right = math.ceil(right)

        # DO BINARY SEARCH, WHILE CHECKING EACH TIME WE MOVE LEFT/RIGHT
        # THIS SAME MODIFIED BINARY SEARCH WILL BE USED IN REMOVE
        keyFound = False
        while left <= right:
            middle = (left + right) // 2
            if self.indexList[middle] == key:
                keyFound = True
                break
            elif self.indexList[middle] < key:
                left = middle + 1
            else:
                right = middle - 1

        if keyFound:
            return None
        else:
            # KEY HAS BEEN FOUND
            # print("INDEX INSERTION POSITION: " + str(left))
            self.indexList.insert(left, key)
            # APPEND +1 TO indexPositions
            self.indexPositions.append(len(self.indexPositions))

    # REMOVES THE GIVEN KEY FROM THE INDEX (IF POSSIBLE)
    def removeIndex(self, key):
                # GET THE PREDICTION 
        prediction = self.predict(key)

        # COMPUTE POSSIBLE RANGE
        left = prediction + self.maxNegativeError
        right = prediction + self.maxPositiveError

        # ROUND MAX UPWARDS, ROUND MIN DOWNWARDS
        left = math.floor(left)
        right = math.ceil(right)

        # USE MODIFIED BINARY SEARCH TO DELETE THE GIVEN INDEX
        # IF GIVEN KEY IS FOUND, THEN DELETE, IF NOT FOUND, THEN DO NOTHING
        keyFound = None
        while left <= right:
            middle = (left + right) // 2
            if self.indexList[middle] == key:
                keyFound = True
                break
            elif self.indexList[middle] < key:
                left = middle + 1
            else:
                right = middle - 1

        if keyFound:
            print("INDEX DELETION POSITION: " + str(middle))
            self.indexList.pop(middle)
            # REMOVE LAST ELEM FROM indexPositions
            self.indexPositions.pop()
        else:
            # KEY WAS NOT FOUND
            return None