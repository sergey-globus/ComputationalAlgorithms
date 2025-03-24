import numpy as np

class Spline:
    def __init__(self, array, start_derivative, end_derivative):
        self.array = array

        self.start_derivative = start_derivative
        self.end_derivative = end_derivative

        self.step_values = self.calculate_step_values()
        self.sweep_coefficients = self.calculate_sweep_coefficients()
        self.spline_coefficients = self.get_spline_coefficients()

    def get_value(self, x):
        interval = self.get_spline_interval(x)
        h = x - self.array[0][interval]

        value = 0
        for i in range(4):
            value += self.spline_coefficients[i][interval] * h ** i

        return value

    def calculate_step_values(self):
        length = self.array.shape[1]
        step_values = np.empty((length, ), dtype=float)

        for i in range(1, length):
            step = self.array[0][i] - self.array[0][i - 1]
            step_values[i] = step

        return step_values

    def calculate_sweep_coefficients(self):
        length = self.array.shape[1]
        sweep_coefficients = np.empty(self.array.shape, dtype=float)
        ksi_values = sweep_coefficients[0]
        eta_values = sweep_coefficients[1]

        ksi_values[0] = float("nan")
        eta_values[0] = float("nan")
        ksi_values[1] = 0
        eta_values[1] = self.start_derivative / 2

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

        return sweep_coefficients

    def fill_a_coefficients(self, a_coefficients):
        length = self.sweep_coefficients.shape[1]

        for i in range(length):
            a = self.array[1][i]
            a_coefficients[i] = a

    def fill_c_coefficients(self, c_coefficients):
        length = self.sweep_coefficients.shape[1]

        c_n_plus_1 = self.end_derivative / 2 

        ksi = self.sweep_coefficients[0][-1]
        eta = self.sweep_coefficients[1][-1]
        c = ksi * c_n_plus_1 + eta
        c_coefficients[-1] = c  

        for i in range(length - 2, -1, -1):
            c_next = c_coefficients[i + 1]
            ksi = self.sweep_coefficients[0][i + 1]
            eta = self.sweep_coefficients[1][i + 1]

            c = ksi * c_next + eta
            c_coefficients[i] = c

    def fill_b_coefficients(self, b_coefficients, c_coefficients):
        length = self.sweep_coefficients.shape[1]

        for i in range(1, length):
            h1 = self.step_values[i]
            y_1 = self.array[1][i]
            y_2 = self.array[1][i - 1]
            c = c_coefficients[i]
            c_prev = c_coefficients[i - 1]

            b = (y_1 - y_2) / h1 - h1 * (c + 2 * c_prev) / 3
            b_coefficients[i - 1] = b

    def fill_d_coefficients(self, d_coefficients, c_coefficients):
        length = self.sweep_coefficients.shape[1]

        for i in range(1, length):
            h1 = self.step_values[i]
            c = c_coefficients[i]
            c_prev = c_coefficients[i - 1]

            d = (c - c_prev) / (3 * h1)
            d_coefficients[i - 1] = d

    def get_spline_coefficients(self):
        length = self.sweep_coefficients.shape[1]
        spline_coefficients = np.empty((4, length), dtype=float)

        self.fill_a_coefficients(spline_coefficients[0])
        self.fill_c_coefficients(spline_coefficients[2])
        self.fill_b_coefficients(spline_coefficients[1], spline_coefficients[2])
        self.fill_d_coefficients(spline_coefficients[3], spline_coefficients[2])

        return spline_coefficients

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
