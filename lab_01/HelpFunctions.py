def NearRow(table, x):
    res = 0

    for i in range(1, len(table)):
        if table[i][0] > x:
            return res
        res += 1

    return res


def ResearchBorders(row, length, degree):
    top = int(degree / 2) - 1
    down = degree - top
    
    if row - top < 0:
        down += top - row
    elif row + down > length:
        top += (row + down) - length

    return top, down