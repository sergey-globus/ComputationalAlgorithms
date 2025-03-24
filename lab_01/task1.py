from input import PrintResTask1
from ermit import Ermit
from newton import Newton

def Task1(table):
    print("\nЗадание 1")
    x = float(input("Введите x: "))
    degree = int(input("Введите степень: "))
    ResNewton = Newton(table, x, degree)
    ResErmit = Ermit(table, x, degree)

    PrintResTask1(ResNewton, ResErmit, table, x, degree)