from newton import Newton

def Task3(t1, t2):
    print("\nЗадание 3")

    # добавляем пары значений - x из первой таблицы, 
    # значение второй функции от x из первой таблицы по Ньютону минус y из первой
    FuncRes = [[t1[i][1], Newton(t2, t1[i][1], 3) - t1[i][0]] for i in range(len(t1))]   
    FuncRes = [[elem[1], elem[0]] for elem in FuncRes]
    FuncRes.sort(key=lambda x: x[0])

    result = Newton(FuncRes, 0.0, 3)
    print("Корень:", result)