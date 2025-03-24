def Print(x, NewtonTab, NaturalSpline, NewtonSplineLeftProizw, NewtonSplineBothProizw):
    print("\nNewton's polynom:\ninterpolated value: {}\n".format(NewtonTab.GetValue(x)))

    print("Splines:")
    print("begin proizw: {}\n".format(NaturalSpline.BeginProizw),
          "stop proizw: {}\n".format(NaturalSpline.StopProizw),
          "interpolated value: {}\n".format(NaturalSpline.GetValue(x)),
          sep='')

    print("begin proizw: {}\n".format(NewtonSplineLeftProizw.BeginProizw),
          "stop proizw: {}\n".format(NewtonSplineLeftProizw.StopProizw),
          "interpolated value: {}\n".format(NewtonSplineLeftProizw.GetValue(x)),
          sep='')

    print("begin proizw: {}\n".format(NewtonSplineBothProizw.BeginProizw),
          "stop proizw: {}\n".format(NewtonSplineBothProizw.StopProizw),
          "interpolated value: {}\n".format(NewtonSplineBothProizw.GetValue(x)),
          sep='')