import numpy as np


class PointTable:
    def __len__(self):
        return len(self.points)

    @staticmethod
    def GetRazm(file_name):
        x_size = -1
        y_size = -1
        x_indices = set()
        y_indices = set()
        z_indices = set()

        with open(file_name, 'r') as file:
            for i, line in enumerate(file):
                i += 1
                line = line.strip()

                if "z=" in line:
                    str_idx = line.find("z=")
                    current_index = int(line[str_idx + 2])

                    z_indices.add(current_index)

                    if not x_indices or not y_indices:
                        continue

                    if x_size == -1:
                        x_size = len(x_indices)
                        y_size = len(y_indices)

                    x_indices.clear()
                    y_indices.clear()

                elif "y\\x" in line:
                    line = line.lstrip("y\\x")
                    items = line.split()
                    indices = list(map(int, items))
                    for current_index in indices:
                        x_indices.add(current_index)

                elif not line:
                    continue

                else:
                    items = line.split()
                    values = list(map(int, items))
                    current_index = values[0]
                    y_indices.add(current_index)

        return len(z_indices), y_size, x_size

    def FromFile(self, file_name):
        shape = self.GetRazm("data.txt")
        self.data = np.empty((shape))

        z_index = 0
        with open(file_name, 'r') as file:
            for _, line in enumerate(file):
                line = line.strip()

                if "z=" in line:
                    str_idx = line.find("z=")
                    z_index = int(line[str_idx + 2])

                elif "y\\x" in line:
                    line = line.lstrip("y\\x")
                    items = line.split()
                    x_indices = list(map(int, items))

                elif not line:
                    continue

                else:
                    items = line.split()
                    values = list(map(int, items))
                    y_index = values[0]

                    for index in range(1, len(values)):
                        x_index = x_indices[index - 1]
                        self.data[z_index][y_index][x_index] = values[index]
