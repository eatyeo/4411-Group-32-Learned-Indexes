# USED TO TIME HOW LONG SPECIFIC METHODS TAKE TO EXECUTE

import sys
import time 
from LRManager import LRManager

def main():
    # GET PARAMS FROM COMMAND LINE
    indexMethod = sys.argv[1]
    filepath = sys.argv[2]
    indexColumn = int(sys.argv[3])

    print("\nTIMING MODULE START")

    # LINEAR REGRESSION
    if indexMethod == "LR":
        # CREATE MANAGER (NO NEED TO BE TIMED)
        manager = LRManager(filepath, indexColumn)

        # READS AND SORTS DATA, BUT DOES NOT CREATE/TRAIN MODEL
        # WILL BE TIMED SINCE OTHER INDEXING IMPLEMENTATION NEEDS TO READ IN DATA
        timeStart = time.time()
        manager.processInputFile()
        timeEnd = time.time()
        resultingTime = timeEnd - timeStart
        # print("PROCESS INPUT TIME: " + str(resultingTime) + " SECONDS.")
        print("PROCESS INPUT TIME: " + str(resultingTime * 1000) + " ms.")

        # CREATES AND TRAINS MODEL
        timeStart = time.time()
        manager.initModel()
        timeEnd = time.time()
        resultingTime = timeEnd - timeStart
        # print("CREATE AND TRAIN MODEL TIME: " + str(resultingTime) + " SECONDS.")
        print("CREATE AND TRAIN MODEL TIME: " + str(resultingTime * 1000) + " ms.")

        # GET THE MODEL
        # NO NEED TO BE TIMED(?)
        model = manager.getModel()

        # LOOKUP A KEY VALUE FROM THE CSV (1188 FOR TESTING)
        timeStart = time.time()
        model.getIndexPosition(1188)
        timeEnd = time.time()
        resultingTime = timeEnd - timeStart
        # print("TIME TO LOOKUP KEY VALUE 1188: " + str(resultingTime) + " SECONDS.")
        print("TIME TO LOOKUP KEY VALUE 1188: " + str(resultingTime * 1000) + " ms.")

        # REMOVE A KNOWN KEY VALUE (1188), THEN READJUST MODEL
        timeStart = time.time()
        model.removeIndex(1188)
        timeEnd = time.time()
        resultingTime = timeEnd - timeStart
        # print("TIME TO LOOKUP KEY VALUE 1188: " + str(resultingTime) + " SECONDS.")
        print("TIME TO REMOVE KEY VALUE 1188: " + str(resultingTime * 1000) + " ms.")

        # ADD BACK A KEY VALUE KNOWN TO NOT EXIST (1188), THEN READJUST MODEL
        timeStart = time.time()
        model.addIndex(1188)
        timeEnd = time.time()
        resultingTime = timeEnd - timeStart
        # print("TIME TO LOOKUP KEY VALUE 1188: " + str(resultingTime) + " SECONDS.")
        print("TIME TO INSERT KEY VALUE 1188: " + str(resultingTime * 1000) + " ms.")
        
        print("\n")
    # B+ TREE
    elif indexMethod == "BT":
        pass
    # HASH INDEX
    elif indexMethod == "HI":
        pass
    # NEURAL NETWORK
    elif indexMethod == "NN":
        pass
    else:
        print("UNKNOWN indexMethod: " + str(indexMethod))

if __name__ == "__main__":
    main()
