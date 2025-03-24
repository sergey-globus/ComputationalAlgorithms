from newton import Newton
from ermit import Ermit

def read_file(file_name):
    numbers = []
    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            line_numbers = [float(num) for num in line.split(',')]
            numbers.append(line_numbers)
    return numbers


def PrintResTask1(ResNewton, ResErmit, table, x, degree):
    print("По Ньютону:", ResNewton)
    print("По Эрмиту: ", ResErmit)

    print("|---------------------------------------------|")
    print("| Степень |      Ньютон     |      Эрмит      |")
    print("|---------------------------------------------|")
    for i in range(0, degree, 1):
        print(f"| {(i + 1): 7g} | {Newton(table, x, i + 1):15.7g} | {Ermit(table, x, i + 1):15.7g} |")
    print("|---------------------------------------------|")