# LRManager.py
# PROCESSES THE CSV INTO INSTANCES OF MODELS FOR EACH COUNTRY

import sys
import csv
import LearnedIndexLR
from LearnedIndexLR import LearnedIndexLR

class LRManager:
    # CONSTRUCTOR
    def __init__(self, filepath: str, indexColumn: int):
        self.filepath = filepath
        self.indexColumn = int(indexColumn)
        self.keyList = [] # LIST STORING ALL INDEXES
        self.models = [] # LIST STORING ALL L.R. MODELS
        self.model = None # LIST STORING ALL L.R. MODELS

    # PROCESSES THE CSV INPUT FILE FOR THE COLUMN WITH THE KEYS
    def processInputFile(self):
        with open(self.filepath, "r") as inputFile:
            input = csv.reader(inputFile)

            # WILL HAVE TO MANUALLY CHANGE THIS VALUE IF NOT USING HEADER ROW
            checkHeaderRow = True

            # ONLY NEED THE COLUMN CONTAINING THE KEYS
            for row in input:
                # SKIP THE HEADER ROW
                if checkHeaderRow:
                    checkHeaderRow = False
                    continue

                # GET RECORD FROM SPECIFIED COLUMN
                inputKeyValue = row[self.indexColumn].strip()

                # IF inputKeyValue == "", THEN continue
                if inputKeyValue == "":
                    continue

                # PROCESS INTO CORRECT FORMAT
                # WILL ALLOW FLOATS FOR NOW, MAY WANT TO CHECK THIS LATER
                floatKeyValue = float(inputKeyValue)

                # ADD TO LIST
                self.keyList.append(floatKeyValue)

            # SORT LIST BY ASC AFTER FOR LOOP
            self.keyList.sort()
                
    # OUTPUT dataByCountry TO COMMAND LINE
    def printKeyList(self):
        print("printKeyList():")

        for keyEntry in self.keyList:
            print(keyEntry)
    
    # CREATE MODELS FOR ALL COUNTRIES
    # def initAllModels(self):
    #     for countryCode, countryData in self.dataByCountry.items():
    #         countryModel = LearnedIndexLR(countryCode, countryData)
    #         countryModel.trainModel()
    #         countryModel.calculateErrorRanges()
    #         self.models[countryCode] = countryModel

    #     print("[FROM LRManager.py] ALL MODELS INITIALISED") # TESTING

    # CREATE AND TRAIN MODEL FROM OUR KEY LIST
    def initModel(self):
        keyModel = LearnedIndexLR(self.keyList)
        keyModel.trainModel()
        keyModel.calculateErrorRanges()
        self.model = keyModel

    # RETURN THE MODEL OBJECT
    def getModel(self):
        return self.model
        

# MAIN
if __name__ == "__main__":
    # GET INPUT FILE FROM COMMAND LINE
    filepath = sys.argv[1]
    indexColumn = sys.argv[2]

    # CREATE MANAGER INSTANCE
    manager = LRManager(filepath, indexColumn)

    # TESTING THE MANAGER INSTANCE
    manager.processInputFile()
    manager.printKeyList()
    # manager.initAllModels()
    # manager.getModel("CA")


    # TESTING THE MODEL INSTANCE
    # canadaData = manager.getCountryData("CA")
    # printString = ""
    # for record in canadaData:
    #     printString += str(record)
    #     printString += ", "
    # print(printString)

    testIndexes = [2024, 2022, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000]

    canadaModel = LearnedIndexLR(testIndexes)
    canadaModel.trainModel()
    canadaModel.printSlopeIntercept()
    canadaModel.calculateErrorRanges()
    canadaModel.printErrorRanges()

 