from math import factorial
from HelpFunctions import NearRow, ResearchBorders

def SwapNewton(table):
    for i in range(len(table)):
        table[i] = table[i][:2][::-1]
    
    table.sort(key=lambda x: x[0])

    return table


def AddDividor(high_line, table):
    for i in range(1, len(high_line)):
        steps = 1
        for j in range(i):
            steps *= abs(table[j + 1][0] - table[j][0])
        high_line[i] *= 1 / (factorial(i) * steps)
    
    return high_line


def SearchNearRazn(table):
    for i in range(len(table) - 1):
        for j in range(len(table) - i - 1):
            table[j].append((table[j + 1][i + 1] - table[j][i + 1]))
    
    return table


def NewtonCoef(table):
    table = SearchNearRazn(table)
    high_line = AddDividor(table[0][1:], table)
    
    return high_line


def PrepareDataNewton(data, x, degree):
    data = [row[0:2] for row in data]
    row = NearRow(data, x)
    top, down = ResearchBorders(row, len(data), degree)
    data = data[max(0, row - top) : min(len(data), row + down)]

    return data


def YNewton(coef, table, x):
    result = coef[0]
    for i in range(1, len(coef)):
        chlen = 1
        for j in range(i):
            chlen *= (x - table[j][0])
        result += coef[i] * chlen
    
    return result


def Newton(table, x, degree):
    table = PrepareDataNewton(table, x, degree)
    coef = NewtonCoef(table)
    result = YNewton(coef, table, x)
    
    return result