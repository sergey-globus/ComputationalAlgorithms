import numpy as np


class Spline:
    def __init__(self, array, BeginProizw, StopProizw):
        self.array = array
        self.BeginProizw = BeginProizw
        self.StopProizw = StopProizw
        self.step_values = self.CalcStepVals()
        self.SweepCoeffs = self.calculate_SweepCoeffs()
        self.SplineCoeffs = self.get_SplineCoeffs()

    def GetValue(self, x):
        interval = self.get_spline_interval(x)
        h = x - self.array[0][interval]

        value = 0
        for i in range(4):
            value += self.SplineCoeffs[i][interval] * h ** i

        return value

    def CalcStepVals(self):
        length = self.array.shape[1]
        step_values = np.empty((length, ), dtype=float)

        for i in range(1, length):
            step = self.array[0][i] - self.array[0][i - 1]
            step_values[i] = step

        return step_values

    def calculate_SweepCoeffs(self):
        length = self.array.shape[1]
        SweepCoeffs = np.empty(self.array.shape, dtype=float)
        ksi_values = SweepCoeffs[0]
        eta_values = SweepCoeffs[1]

        ksi_values[0] = float("nan")
        eta_values[0] = float("nan")
        ksi_values[1] = 0
        eta_values[1] = self.BeginProizw / 2

        for i in range(2, length):
            h1 = self.step_values[i]
            h2 = self.step_values[i - 1]
            y_1 = self.array[1][i]
            y_2 = self.array[1][i - 1]
            y_3 = self.array[1][i - 2]

            divider = 2 * (h1 + h2) + h2 * ksi_values[i - 1]
            ksi_values[i] = - h2 / divider

            func = 3 * ((y_1 - y_2) / h1 - (y_2 - y_3) / h2)
            eta_values[i] = (func - h2 * eta_values[i - 1]) / divider

        return SweepCoeffs

    def fill_a_coefficients(self, a_coefficients):
        length = self.SweepCoeffs.shape[1]

        for i in range(length):
            a = self.array[1][i]
            a_coefficients[i] = a

    def fill_c_coefficients(self, c_coefficients):
        length = self.SweepCoeffs.shape[1]

        c_n_plus_1 = self.StopProizw / 2 

        ksi = self.SweepCoeffs[0][-1]
        eta = self.SweepCoeffs[1][-1]
        c = ksi * c_n_plus_1 + eta
        c_coefficients[-1] = c

        for i in range(length - 2, -1, -1):
            c_next = c_coefficients[i + 1]
            ksi = self.SweepCoeffs[0][i + 1]
            eta = self.SweepCoeffs[1][i + 1]

            c = ksi * c_next + eta
            c_coefficients[i] = c

    def fill_b_coefficients(self, b_coefficients, c_coefficients):
        length = self.SweepCoeffs.shape[1]

        for i in range(1, length):
            h1 = self.step_values[i]
            y_1 = self.array[1][i]
            y_2 = self.array[1][i - 1]
            c = c_coefficients[i]
            c_prev = c_coefficients[i - 1]

            b = (y_1 - y_2) / h1 - h1 * (c + 2 * c_prev) / 3
            b_coefficients[i - 1] = b

    def fill_d_coefficients(self, d_coefficients, c_coefficients):
        length = self.SweepCoeffs.shape[1]

        for i in range(1, length):
            h1 = self.step_values[i]
            c = c_coefficients[i]
            c_prev = c_coefficients[i - 1]

            d = (c - c_prev) / (3 * h1)
            d_coefficients[i - 1] = d

    def get_SplineCoeffs(self):
        length = self.SweepCoeffs.shape[1]
        SplineCoeffs = np.empty((4, length), dtype=float)

        self.fill_a_coefficients(SplineCoeffs[0])
        self.fill_c_coefficients(SplineCoeffs[2])
        self.fill_b_coefficients(SplineCoeffs[1], SplineCoeffs[2])
        self.fill_d_coefficients(SplineCoeffs[3], SplineCoeffs[2])

        return SplineCoeffs

    def get_spline_interval(self, x):
        length = self.array.shape[1]
        low = 0
        high = length - 1

        if x > self.array[0][length - 1]:
            return length - 1

        while low < high:
            index = (low + high) // 2
            if index == length - 1 or self.array[0][index + 1] < x:
                low = index + 1
            else:
                high = index
        return low 
