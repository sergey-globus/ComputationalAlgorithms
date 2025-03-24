import numpy as np

class PointTable:
    def __len__(self):
        return len(self.points)

    def from_points(self, points):
        self.points = points

    def ReadFile(self, file_name):
        self.points = []
        with open(file_name, 'r') as file:
            for line in enumerate(file):
                item = line[1].rstrip().split(" ")

                x, y = map(float, item[:2])
                self.points.append([x, y])

    def to_nparray(self):
        return np.array([[point[0] for point in self.points], [point[1] for point in self.points]])


class PartialTable:
    def __init__(self, point_table):
        self.point_table = point_table
        self.bottom_index = 0
        max_amount = len(self.point_table)
        self.top_index = max_amount - 1
        self.set_coordinates()

    def SetPartition(self, value, amount):
        self.bottom_index = 0
        max_amount = len(self.point_table)
        top_index = max_amount - 1
        self.top_index = top_index
        self.set_coordinates()

        for index in range(len(self.point_table)):
            if self.coordinates[0][index] > value:
                top_index = index
                break

        bottom_index = top_index

        while top_index - bottom_index < amount - 1:
            if bottom_index > 0:
                bottom_index -= 1
            if top_index - bottom_index == amount - 1:
                break
            if top_index < max_amount - 1:
                top_index += 1

        self.point_table = self.point_table
        self.bottom_index = bottom_index
        self.top_index = top_index
        self.set_coordinates()

    def set_coordinates(self):
        self.coordinates = [[], []]
        for i in range(self.bottom_index, self.top_index + 1):
            self.coordinates[0].append(self.point_table.points[i][0])
            self.coordinates[1].append(self.point_table.points[i][1])


class DiffsTable:
    def __init__(self, point_table):
        self.point_table = point_table
        self.PartialTab = PartialTable(self.point_table)

    def GetValue(self, x):
        factor = 1
        approximated_value = self.diffs[1][0]

        for i in range(2, len(self.diffs)):
            if not self.diffs[i]:
                continue
            factor *= x - self.diffs[0][i - 2]
            approximated_value += factor * self.diffs[i][0]

        return approximated_value

    def GetSecondProizw(self, x):
        x0 = self.diffs[0][0]
        x1 = self.diffs[0][1]
        x2 = self.diffs[0][2]
        return 2 * (self.diffs[3][0] + self.diffs[4][0] * (3 * x - x0 - x1 - x2))


class NewtonTable(DiffsTable):
    def CalcTab(self, x, degree):
        self.degree = degree
        self.UpdatePartialTab(x)
        self.calculate_diffs()
        self.x = x

    def GetValue(self, x):
        return super().GetValue(x)

    def GetSecondProizw(self, x):
        return super().GetSecondProizw(x)

    def UpdatePartialTab(self, x):
        self.PartialTab.SetPartition(x, self.degree + 1)

    def calculate_diffs(self):
        coordinates = self.PartialTab.coordinates
        diffs = [coordinates[0], coordinates[1]]

        for i in range(1, self.PartialTab.top_index - self.PartialTab.bottom_index + 1):
            row = []
            for j in range(self.PartialTab.top_index - self.PartialTab.bottom_index - i + 1):
                partial_x_difference = diffs[0][j] - diffs[0][j + i]
                partial_y_difference = diffs[i][j] - diffs[i][j + 1]
                row.append(partial_y_difference / partial_x_difference)
            diffs.append(row)
        self.diffs = diffs
        self.points_used = len(self.diffs[0])