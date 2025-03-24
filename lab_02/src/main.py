from spline import Spline
from tabs import NewtonTable
from print import Print
from input import Input

def main():
    table, x, err = Input()
    if err == -1:
        return
    
    NaturalSpline = Spline(table.to_nparray(), 0.0, 0.0) # естественные краевые условия для сплайна(вторые производные равные 0)
    
    NewtonTab = NewtonTable(table)
    NewtonTab.CalcTab(table.points[0][0], 3)
    Left2Proizw = NewtonTab.GetSecondProizw(table.points[0][0])
    NewtonTab.CalcTab(table.points[-1][0], 3)
    Right2Proizw = NewtonTab.GetSecondProizw(table.points[-1][0])

    NewtonSplineLeftProizw = Spline(table.to_nparray(), Left2Proizw, 0.0)
    NewtonSplineBothProizw = Spline(table.to_nparray(), Left2Proizw, Right2Proizw)
    NewtonTab.CalcTab(x, 3)

    Print(x, NewtonTab, NaturalSpline, NewtonSplineLeftProizw, NewtonSplineBothProizw)

main()
