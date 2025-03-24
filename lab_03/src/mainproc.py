import numpy as np
from spline import Spline
from Newton import NewtonPolynom

def get_partition(base_idx, power, max_power):
    if base_idx >= max_power:
        return -1, -1

    if power > max_power:
        return -1, -1

    if base_idx + power // 2 < max_power:
        if base_idx - power + power // 2 + 1 >= 0:
            top_index = base_idx + power // 2
            bottom_index = top_index - (power - 1)
        else:
            bottom_index = 0
            top_index = power - 1
    else:
        top_index = max_power - 1
        bottom_index = top_index - (power - 1)

    return bottom_index, top_index

def Check3N(table, nx, ny, nz):
    if nx > table.data.shape[2]:
        print("nx power is too big")
        return -1
    if ny > table.data.shape[1]:
        print("ny power is too big")
        return -1
    if nz > table.data.shape[0]:
        print("nz power is too big")
        return -1
    return 0

def CheckExtrapol(table, nx, ny, nz, x, y, z):
    rc = 0

    bottom_z, top_z = get_partition(int(z), nz, table.data.shape[0])
    if bottom_z == -1 or top_z == -1:
        print("Ошибка! Экстраполяция по Z!!")
        rc = -1
    
    bottom_y, top_y = get_partition(int(y), ny, table.data.shape[1])
    if bottom_y == -1 or top_y == -1:
        print("Ошибка! Экстраполяция по Y!!")
        rc = -1

    bottom_x, top_x = get_partition(int(x), nx, table.data.shape[2])
    if bottom_x == -1 or top_x == -1:
        print("Ошибка! Экстраполяция по X!!")
        rc = -1
    
    return rc, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z

def MakeArr(n, bottom):
    arr = np.empty((2, n))
    for i in range(n):
        arr[0][i] = i + bottom
    
    return arr

def CheckExtrapolZZZ(table, z):
    z_idx = int(z)
    if z_idx > table.data.shape[0]:
        print("error: extrapolation by z coordinate")
        return -1
    
    return 0

def NewtonRun(table, x, y, z, nx, ny, nz):
    rc = Check3N(table, nx, ny, nz)
    if rc != 0:
        return
    rc = CheckExtrapolZZZ(table, z)
    if rc != 0:
        return
    rc, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z = CheckExtrapol(table, nx, ny, nz, x, y, z)
    if rc != 0:
        return
    
    tmpZ = MakeArr(nz, bottom_z)
    tmpX = MakeArr(nx, bottom_x)
    tmpY = MakeArr(ny, bottom_y)

    for i in range(nz):
        z_idx = bottom_z + i

        for j in range(ny):
            y_idx = bottom_y + j

            tmpX[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]
            polynom = NewtonPolynom(tmpX, 'f', 'x')
            polynom.calculate_table(x, nx - 1)
            interpolated_in_x = polynom.get_value(x)

            tmpY[1][j] = interpolated_in_x

        polynom = NewtonPolynom(tmpY, 'f', 'y')
        polynom.calculate_table(y, ny - 1)
        interpolated_in_y = polynom.get_value(y)
        tmpZ[1][i] = interpolated_in_y

    polynom = NewtonPolynom(tmpZ, 'f', 'z')
    polynom.calculate_table(z, nz - 1)

    return polynom.get_value(z)


def SplineRun(table, x, y, z):
    nx = table.data.shape[2]
    ny = table.data.shape[1]
    nz = table.data.shape[0]

    rc = CheckExtrapolZZZ(table, z)
    if rc != 0:
        return
    rc, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z = CheckExtrapol(table, nx, ny, nz, x, y, z)
    if rc != 0:
        return

    tmpZ = MakeArr(nz, bottom_z)
    tmpX = MakeArr(nx, bottom_x)
    tmpY = MakeArr(ny, bottom_y)

    for i in range(nz):
        z_idx = bottom_z + i

        for j in range(ny):
            y_idx = bottom_y + j

            tmpX[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]

            spline = Spline(tmpX, 0, 0)
            tmpY[1][j] = spline.get_value(x)

        spline = Spline(tmpY, 0, 0)
        interpolated_in_y = spline.get_value(y)
        tmpZ[1][i] = interpolated_in_y

    spline = Spline(tmpZ, 0, 0)

    return spline.get_value(z)

def MixedRun(table, x, y, z, nx, nz):
    ny = table.data.shape[1]

    rc = Check3N(table, nx, ny, nz)
    if rc != 0:
        return
    rc = CheckExtrapolZZZ(table, z)
    if rc != 0:
        return
    rc, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z = CheckExtrapol(table, nx, ny, nz, x, y, z)
    if rc != 0:
        return

    tmpZ = MakeArr(nz, bottom_z)
    tmpX = MakeArr(nx, bottom_x)
    tmpY = MakeArr(ny, bottom_y)

    for i in range(nz):
        z_idx = bottom_z + i

        for j in range(ny):
            y_idx = bottom_y + j

            tmpX[1] = table.data[z_idx, y_idx, bottom_x:top_x + 1]
            polynom = NewtonPolynom(tmpX, 'f', 'x')
            polynom.calculate_table(x, nx - 1)
            interpolated_in_x = polynom.get_value(x)

            tmpY[1][j] = interpolated_in_x

        spline = Spline(tmpY, 0, 0)
        interpolated_in_y = spline.get_value(y)
        tmpZ[1][i] = interpolated_in_y

    polynom = NewtonPolynom(tmpZ, 0, 0)
    polynom.calculate_table(z, nz - 1)

    return polynom.get_value(z)