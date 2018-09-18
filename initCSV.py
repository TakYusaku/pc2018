# read csv files and write csv file


import csv
import numpy as np

"""
with open('data.csv', 'r') as file:
    lst = list(csv.reader(file))

a = np.array(lst)
print(a)
"""
q_table = np.zeros((144, 9))

with open('q_table_QL.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(q_table)
