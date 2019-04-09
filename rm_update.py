# remove duplicates using past remaining
import sys
import csv

selected = sys.argv[1]
#print selected

with open('remaining.csv', 'r') as file1:
    with open(selected, 'r') as file2:
        same = set(file1).difference(file2)

same.discard('\n')

with open('updated.csv', 'w') as file_out:
    for line in same:
        file_out.write(line)
