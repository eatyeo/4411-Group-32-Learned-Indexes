# 4411-Group-32-Learned-Indexes

## About this README
This README is written for use on the github repo. If this is being read from the README.md file, refer to the following link for ease of viewing:
[GitHub Repo](https://github.com/leeandrew135/4411-Group-32-Learned-Indexes)

## Project Structure

### /data
There are 3 synthetic datasets, as well as 1 real dataset that is in the folder. The synthetic datasets were used in the timing module, are are the results that are available in the presentation and the report. 

These files represent synthetic data for a set of 1000 values that could be used as key values.

Note that the LRManager, takes in the input and processes it into a sorted array, that is then passed to the classes. More on this later.

### /src

This directory contains the following:

### TimingModule.py 
Used to measure and output the times that it takes to perform certain operations on the indexing models.

Note that in the main() section of this file, there is a variable 'interations' that controls over how many iterations the time is averaged out over. For example, if iterations == 10, then the operation will be run 10 times and averaged out over 10 times. 

Additionally, within the timeLR(), timeHI(), and timeBT() methods, the values that are used to test are hard coded for ease of development. It is possible that the value will have to be changed to another value that is known to be in the dataset, depending on which dataset is used. For example, '1188' will work for roughlyLinear and skewed, but will not work for logNormal. In the case of logNormal, the value '6.38256218189565' can be used instead, as it is a value known to be in the dataset.

For example, this file can be run with the following command:
```python
python3 TimingModule.py indexMethod filepath indexColumn
```
Where indexMethod is one of ["LR", "HI", "BT"] for Linear Regression, Hash Index, or B+ Tree.

Where filepath is the relative filepath.

Where indexColumn corresponds to the column of the input file that will be used (for synthetic datasets, this will be 0).

Again, note that depending on the input file that is used, the hardcoded values used for testing may not work, and may need to be adjusted to a value that is known to be in the dataset.

### LRManager.py
Can be run from the command line with the following command:
```python
python3 LRManager.py filepath indexColumn
```
Where filepath represents the relative filepath, and indexColumn represents an integer of the column that will be selected as the column of keys. For the synthetic datasets, this will always be 0, as there is only 1 column.

This file takes in the input, processes it into a sorted list, initialises the model, and returns the model object by it's function calls. There is already pre existing code in the 
```python
if __name__ == "__main__":
```
section of the file that was used for testing and debugging. 

### BPlusTree.py, HashIndex.py, LearnedIndexLR.py
These files represent the index structures of B+ tree, hash index, and linear regression learned index. These files are not meant to be run on their own, as they are called from LRManager.py

### NN.ipynb
The simple neural network implementation done using Jupyter Notebook.

