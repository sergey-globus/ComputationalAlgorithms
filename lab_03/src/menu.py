from mainproc import *

def GetUserData():
    print("1. Полиномы Ньютона\n"
          "2. Сплайны\n"
          "3. Смешанная интерполяция\n"
          "0. Завершить программу")
    key = int(input("Введите номер действия: "))

    return key


def GetCordsUser():
    x = float(input("x: "))
    y = float(input("y: "))
    z = float(input("z: "))

    return x, y, z


def Get3NUser():
    nx = int(input("степень nx: "))
    ny = int(input("степень ny: "))
    nz = int(input("степень nz: "))

    return nx, ny, nz


def Get2NUser():
    nx = int(input("степень nx: "))
    nz = int(input("степень nz: "))

    return nx, nz


def PrintRes(result):
    print("Результат:", result)


def TaskNewton(table):
    x, y, z = GetCordsUser()
    nx, ny, nz = Get3NUser()

    result = NewtonRun(table, x, y, z, nx + 1, ny + 1, nz + 1)

    PrintRes(result)


def TaskSpline(table):
    x, y, z = GetCordsUser()

    result = SplineRun(table, x, y, z)

    PrintRes(result)


def TaskMixed(table):
    x, y, z = GetCordsUser()
    nx, nz = Get2NUser()

    result = MixedRun(table, x, y, z, nx + 1, nz + 1)

    PrintRes(result)


def menu(table):
    run_menu = True
    while run_menu:
        key = GetUserData()
        if key == 0:
            run_menu = False
        elif key == 1:
            TaskNewton(table)
        elif key == 2:
            TaskSpline(table)
        elif key == 3:
            TaskMixed(table)