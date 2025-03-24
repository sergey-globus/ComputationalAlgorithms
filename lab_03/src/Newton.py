class PartialTable:
    def __init__(self, array):
        self.array = array
        self.bottom_index = 0

        max_amount = self.array.shape[1]
        max_index = max_amount - 1
        self.top_index = max_index

    def __len__(self):
        return max(self.top_index - self.bottom_index + 1, 0)

    def set_partition(self, value, amount):
        self.bottom_index = 0
        max_amount = self.array.shape[1]
        max_index = max_amount - 1
        top_index = max_index
        self.top_index = top_index

        for index in range(self.array.shape[1]):
            if self.array[0][index] > value:
                top_index = index
                break

        bottom_index = top_index

        while top_index - bottom_index < amount - 1:
            if bottom_index > 0:
                bottom_index -= 1
            if top_index - bottom_index == amount - 1:
                break
            if top_index < max_index:
                top_index += 1

        self.bottom_index = bottom_index
        self.top_index = top_index


class DiffsTable:
    def __init__(self, array, func_str, arg_str):
        self.func_str = func_str
        self.arg_str = arg_str
        self.array = array
        self.partial_table = PartialTable(self.array)

    def get_value(self, x):
        factor = 1
        approximated_value = self.diffs[1][0]

        for i in range(2, len(self.diffs)):
            if not self.diffs[i]:
                continue
            factor *= x - self.diffs[0][i - 2]
            approximated_value += factor * self.diffs[i][0]

        return approximated_value


class NewtonPolynom(DiffsTable):
    def calculate_table(self, x, power):
        self.power = power
        self.update_partial_table(x)
        self.calculate_diffs()
        self.x = x

    def get_value(self, x):
        return super().get_value(x)

    def update_partial_table(self, x):
        self.partial_table.set_partition(x, self.power + 1)

    def calculate_diffs(self):
        diffs = [self.array[0], self.array[1]]

        for i in range(1, self.partial_table.top_index - self.partial_table.bottom_index + 1):
            row = []
            for j in range(self.partial_table.top_index - self.partial_table.bottom_index - i + 1):
                partial_x_difference = diffs[0][j] - diffs[0][j + i]
                partial_y_difference = diffs[i][j] - diffs[i][j + 1]
                row.append(partial_y_difference / partial_x_difference)
            diffs.append(row)
        self.diffs = diffs
        self.points_used = len(self.diffs[0])
