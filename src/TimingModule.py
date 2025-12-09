# USED TO TIME HOW LONG SPECIFIC METHODS TAKE TO EXECUTE

import sys
import time 
from LRManager import LRManager
from HashIndex import HashIndex
from pympler import asizeof

def timeLR(filepath, indexColumn): 
    # CREATE MANAGER (NO NEED TO BE TIMED)
    manager = LRManager(filepath, indexColumn)

    # READS AND SORTS DATA, BUT DOES NOT CREATE/TRAIN MODEL
    # WILL BE TIMED SINCE OTHER INDEXING IMPLEMENTATION NEEDS TO READ IN DATA
    timeStart = time.time()
    manager.processInputFile()
    timeEnd = time.time()
    resultingTime = timeEnd - timeStart
    print("PROCESS INPUT TIME: " + str(resultingTime * 1000) + " ms.")

    # CREATES AND TRAINS MODEL
    timeStart = time.time()
    manager.initModel()
    timeEnd = time.time()
    resultingTime = timeEnd - timeStart
    print("CREATE AND TRAIN MODEL TIME: " + str(resultingTime * 1000) + " ms.")

    # GET THE MODEL
    # NO NEED TO BE TIMED(?)
    model = manager.getModel()

    # LOOKUP A KEY VALUE FROM THE CSV (1188 FOR TESTING)
    timeStart = time.time()
    model.getIndexPosition(1188)
    timeEnd = time.time()
    resultingTime1 = timeEnd - timeStart
    print("TIME TO LOOKUP KEY VALUE 1188: " + str(resultingTime1 * 1000) + " ms.")

    # REMOVE A KNOWN KEY VALUE (1188), THEN READJUST MODEL
    timeStart = time.time()
    model.removeIndex(1188)
    timeEnd = time.time()
    resultingTime2 = timeEnd - timeStart
    print("TIME TO REMOVE KEY VALUE 1188: " + str(resultingTime2 * 1000) + " ms.")

    # ADD BACK A KEY VALUE KNOWN TO NOT EXIST (1188), THEN READJUST MODEL
    timeStart = time.time()
    model.addIndex(1188)
    timeEnd = time.time()
    resultingTime3 = timeEnd - timeStart
    print("TIME TO INSERT KEY VALUE 1188: " + str(resultingTime3 * 1000) + " ms.")
    
    # PERFORM A RANGE QUERY TO COMPARE WITH HASH INDEX
    timeStart = time.time()
    model.getRange(500, 1000) # DO NOT USE FOR LOG
    timeEnd = time.time()
    resultingTime4 = timeEnd - timeStart
    print("TIME TO GET RANGE 500 - 1000: " + str(resultingTime4 * 1000) + " ms.")

    print("\n")

    modelSize = asizeof.asizeof(model)
    print("LR SPACE COMPLEXITY: MODEL USES:", modelSize, "bytes.")

    return [resultingTime1, resultingTime2, resultingTime3, resultingTime4]

def timeHI(filepath, indexColumn):
    manager = LRManager(filepath, indexColumn)
    
    # READS AND SORTS DATA (TIMED)
    timeStart = time.time()
    manager.processInputFile()
    timeEnd = time.time()
    print("PROCESS INPUT TIME: " + str((timeEnd - timeStart) * 1000) + " ms.")

    # CREATE AND POPULATE THE HASH INDEX
    timeStart = time.time()
    hash_idx = HashIndex()
    hash_idx.buildIndex(manager.keyList)
    timeEnd = time.time()
    print("BUILD INDEX TIME: " + str((timeEnd - timeStart) * 1000) + " ms.")

    # LOOKUP A KNOWN KEY VALUE (1188)
    timeStart = time.time()
    positions = hash_idx.getIndexPosition(1188) 
    timeEnd = time.time()
    resultingTime1 = timeEnd - timeStart
    print("TIME TO LOOKUP KEY 1188: " + str(resultingTime1 * 1000) + " ms.")
    
    # VERIFY SEARCH RESULTS
    if positions:
        print(f"   > Found matches at indices: {positions[:5]}...")
    else:
        print("   > Key not found.")
    
    # REMOVE THE KEY (1188) FROM THE INDEX
    timeStart = time.time()
    hash_idx.removeIndex(1188)
    timeEnd = time.time()
    resultingTime2 = timeEnd - timeStart
    print("TIME TO REMOVE KEY 1188: " + str(resultingTime2 * 1000) + " ms.")

    # ADD BACK A KEY VALUE KNOWN TO NOT EXIST (1188)
    timeStart = time.time()
    hash_idx.addIndex(1188, positions[0])
    timeEnd = time.time()
    resultingTime3 = timeEnd - timeStart
    print("TIME TO INSERT KEY VALUE 1188: " + str(resultingTime3 * 1000) + " ms.")

    # PERFORM A RANGE QUERY TO COMPARE WITH HASH INDEX
    timeStart = time.time()
    hash_idx.getRange(500, 1000) # DO NOT USE FOR LOG
    timeEnd = time.time()
    resultingTime4 = timeEnd - timeStart
    print("TIME TO GET RANGE 500 - 1000: " + str(resultingTime4 * 1000) + " ms.")

    print("\n")
    
    modelSize = asizeof.asizeof(hash_idx)
    print("HI SPACE COMPLEXITY: MODEL USES:", modelSize, "bytes.")

    return [resultingTime1, resultingTime2, resultingTime3, resultingTime4]

def main():
    # GET PARAMS FROM COMMAND LINE
    indexMethod = sys.argv[1]
    filepath = sys.argv[2]
    indexColumn = int(sys.argv[3])

    print("\nTIMING MODULE START")

    # LINEAR REGRESSION
    if indexMethod == "LR":
        counter = 0
        iterations = 500
        totalLookup = 0
        totalRemove = 0
        totalInsert = 0
        totalRange = 0

        while counter < iterations:
            result = timeLR(filepath, indexColumn)
            totalLookup += result[0]
            totalRemove += result[1]
            totalInsert += result[2]
            totalRange += result[3]
            counter += 1

        avgLookup = totalLookup / iterations
        avgRemove = totalRemove / iterations
        avgInsert = totalInsert / iterations
        avgRange = totalRange / iterations

        print("AVG. LR LOOKUP OVER " + str(iterations) + ": " + str(avgLookup * 1000) + " ms.")
        print("AVG. LR REMOVE OVER " + str(iterations) + ": " + str(avgRemove * 1000) + " ms.")
        print("AVG. LR INSERT OVER " + str(iterations) + ": " + str(avgInsert * 1000) + " ms.")
        print("AVG. LR  RANGE OVER " + str(iterations) + ": " + str( avgRange * 1000) + " ms.")
        print("\n")
    # B+ TREE
    elif indexMethod == "BT":
        pass
    # HASH INDEX
    elif indexMethod == "HI":
        counter = 0
        iterations = 500
        totalLookup = 0
        totalRemove = 0
        totalInsert = 0
        totalRange = 0

        while counter < iterations:
            result = timeHI(filepath, indexColumn)
            totalLookup += result[0]
            totalRemove += result[1]
            totalInsert += result[2]
            totalRange += result[3]
            counter += 1

        avgLookup = totalLookup / iterations
        avgRemove = totalRemove / iterations
        avgInsert = totalInsert / iterations
        avgRange = totalRange / iterations

        print("AVG. HI LOOKUP OVER " + str(iterations) + ": " + str(avgLookup * 1000) + " ms.")
        print("AVG. HI REMOVE OVER " + str(iterations) + ": " + str(avgRemove * 1000) + " ms.")
        print("AVG. HI INSERT OVER " + str(iterations) + ": " + str(avgInsert * 1000) + " ms.")
        print("AVG. HI RANGE OVER " + str(iterations) + ": " + str(avgRange * 1000) + " ms.")
        print("\n")
    # NEURAL NETWORK
    elif indexMethod == "NN":
        pass
    else:
        print("UNKNOWN indexMethod: " + str(indexMethod))

if __name__ == "__main__":
    main()
