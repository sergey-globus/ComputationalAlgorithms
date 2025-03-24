from math import factorial
from HelpFunctions import NearRow, ResearchBorders

def SwapErmit(table):
    for i in range(len(table)):
        table[i][3] = -table[i][3] / table[i][2] ** 3
        table[i][2] = 1 / table[i][2]
        table[i][0], table[i][1] = table[i][1], table[i][0]

    table.sort(key=lambda x: x[0])

    return table


def SwitchStop(i, j, before, data, resj):
    if data[j - i][0] == data[j][0]:
        return data[j][i + 1] / factorial(i)
    else:
        return ((resj - before) / (data[j][0] - data[j - i][0]))


def ErmitCoef(data, n):
    # массив y(утроенные)
    result = [data[_][1] for _ in range(n)] 

    for i in range(1, n, 1):
        before = result[i - 1]
        for j in range (i, n, 1):
            before2 = result[j]
            result[j] = SwitchStop(i, j, before, data, result[j])
            before = before2

    return result


def PrepareDataErmit(data, x, degree):
    row = NearRow(data, x)
    top, down = ResearchBorders(row, len(data), degree)
    data = data[max(0, row - top) : min(len(data), row + down)]
    data = [elem for elem in data for _ in range(3)]

    return data


def YErmit(coef, table, x):
    result = coef[0]
    chlen = 1
    for i in range(1, len(table)):
        chlen *= (x - table[i - 1][0])
        result += coef[i] * chlen
    
    return result


def Ermit(table, x, degree):
    table = PrepareDataErmit(table, x, degree)
    coef = ErmitCoef(table, degree * 3)
    result = YErmit(coef, table, x)
    
    return result