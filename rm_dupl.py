# remove duplicates between csv
import sys
import csv

selected = sys.argv[1]
#print selected

with open('temp.csv', 'r') as file1:
    with open(selected, 'r') as file2:
        same = set(file1).difference(file2)

same.discard('\n')

with open('remaining.csv', 'w') as file_out:
    for line in same:
        file_out.write(line)
