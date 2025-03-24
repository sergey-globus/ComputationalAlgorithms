from tabs import PointTable

def Input():
    err = 0

    table = PointTable()
    table.ReadFile("data.txt")
    x = float(input("Input x: "))

    if not (table.points[0][0] <= x <= table.points[-1][0]):
        print("Error: extrapolation!!")
        err = -1
    
    return table, x, err