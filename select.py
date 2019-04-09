# hold
import os
import sys
import csv
import random
from datetime import date

# pipe in 'temp.csv'
temp_csv = sys.argv[1:4]
print(temp_csv)

"""
k = 5
#fpath = 'temp.csv'

def rng_sample(filename, k):
    sample = []
    with open(filename) as f:
        for n, line in enumerate(f):
            if n < k:
                sample.append(line.rstrip())
            else:
                r = random.randint(0, n)
                if r < k:
                    sample[r] = line.rstrip()
    return sample

rng_sample(temp_csv, 5)

with open(temp_csv, 'r') as csvinput:
    with open('stats.JC.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

f = open(temp_csv, 'r')

for line_num, line in enumerate(f):
    n = line_num + 1.0
    r = random.random()
    if n <= C:
        buffer.append(line.strip())
    elif r < C/n:
        loc = random.randint(0, C-1)
        buffer[loc] = line.strip()
return buffer

        all = []
        row = next(reader)
        row.append('Selected')
        all.append(row)

        for row in reader:
            row.append(row[0])
            all.append(row)

        writer.writerows(all)




dt = str(date.today())
append_dt = 'stats.JC_' + dt + '.csv'

os.rename('temp.csv', append_dt)"""

"""with open(FILE) as csvfile:
    reader = csv.reader(csvfile)
    chosen_row = random.choice(list(reader))
    print(chosen_row)

with open('stats.JC.csv') as csvfile:
    lines = [line for line in csvfile]
    line_number = random.randrange(lines)

with open('stats.JC.csv') as csvfile:
    reader = csv.reader(csvfile)
    chosen_row = next(row for row_number, row in enumerate(reader)
                      if row_number == line_number)
    print(chosen_row)"""
    # select 3-5, export to text or some sort of echo for discord
