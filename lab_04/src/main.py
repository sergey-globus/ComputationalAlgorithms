from tab import Table
import algho_runner as ca

def inputTableData(dim: int):
    amountX = int(input("\nAmount of nodes: "))
    xStart = int(input("Start X: "))
    xEnd = int(input("End X: "))

    if dim == 1:
        return [amountX], xStart, xEnd
    else:
        amountY = int(input("\nAmount of nodes: "))
        yStart = int(input("Start Y: "))
        yEnd = int(input("End Y: "))

        return [amountX, amountY], xStart, xEnd, yStart, yEnd

def changeWeights(myTable: Table):  
    print("\n1. All ones\n2. By number\n")
    opt = int(input("Enter option: "))

    num = None
    weight = None

    if opt == 2:
        num = int(input("Enter number: "))
        weight = float(input("Enter weight: "))
    
    myTable.editWeight(opt, num, weight)

opts = "\n Одномерная аппроксимация\n" \
        "1. Создать таблицу\n" \
        "2. Вывести таблицу\n" \
        "3. Изменить значения весов\n" \
        "4. Вывести графики\n" \
        "\n\ Двумерная аппроксимация\n" \
        "5. Создать таблицу\n" \
        "6. Вывести таблицу\n" \
        "7. Изменить значения весов\n" \
        "8. Вывести графики\n" \
        "\n# Решение уравнения\n" \
        "9. Решить\n" \
        "\n0. Выход\n" \
    

def main():
    oneDimTable = Table()
    twoDimTable = Table()

    while True:
        print(opts) 
        opt = int(input("введите номер меню: "))

        if opt == 0:
            return
        elif opt == 1:
            amount, xStart, xEnd = inputTableData(1)
            oneDimTable.generateTable(amount, [xStart, xEnd])
        elif opt == 2:
            oneDimTable.printTable()
        elif opt == 3:
            changeWeights(oneDimTable)
        elif opt == 4:
            power = int(input("\nВведите степень полинома: "))
            koefsN = ca.solveSystemOne(oneDimTable, power)
            oneDimTable.drawGraphics(koefsN)
        elif opt == 5:
            amount, xStart, xEnd, yStart, yEnd = inputTableData(2)
            twoDimTable.generateTable(amount, [xStart, xEnd, yStart, yEnd])
        elif opt == 6:
            twoDimTable.printTable()
        elif opt == 7:
            changeWeights(twoDimTable)
        elif opt == 8:
            power = int(input("\nВведите степень полинома: "))
            if power != 1 and power != 2:
                print("Неправильная степень полинома")
            else:
                koefs = ca.solveSystemTwo(twoDimTable, power)
                twoDimTable.drawGraphics(koefs)
        elif opt == 9:
            ca.solveODE()

main()