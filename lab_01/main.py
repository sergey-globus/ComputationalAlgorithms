from input import read_file
from task1 import Task1
from task2 import Task2
from task3 import Task3

table = read_file('table.csv')
Task1(table.copy())
Task2(table.copy())
table1 = read_file('table1.csv')
table2 = read_file('table2.csv')
Task3(table1, table2)