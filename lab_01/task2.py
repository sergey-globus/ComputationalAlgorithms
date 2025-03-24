from ermit import Ermit, SwapErmit
from newton import Newton, SwapNewton

def Task2(table):
    print("\nЗадание 2")
    degree = int(input("Введите степень: "))
    print("По Ньютону:", Newton(SwapNewton(table.copy()), 0.4, degree))
    print("По Эрмиту:", Ermit(SwapErmit(table.copy()), 0.4, degree))