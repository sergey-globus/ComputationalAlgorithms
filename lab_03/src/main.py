from data import PointTable
from menu import menu

def main():
    table = PointTable()
    table.FromFile("data.txt")

    menu(table)

main()
