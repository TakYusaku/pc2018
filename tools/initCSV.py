# read csv files and write csv file


import csv
import numpy as np
import sys

"""
with open('data.csv', 'r') as file:
    lst = list(csv.reader(file))

a = np.array(lst)
print(a)
"""
q_table = np.zeros((144, 9))

fn = 'q_table_' + sys.argv[1] + '.csv'
with open(fn, 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(q_table)
