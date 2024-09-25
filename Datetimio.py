def Sorting_Dates_For_Weeks(Dates: list):

    '''
    La función recibe una lista de fechas llamada Dates, donde cada elemento es una fecha con información de día, 
    mes, año, y posiblemente hora (dependiendo del formato que uses).

    Devuelve una lista de semanas ordenadas con los índices de los días.
    
    '''

    Weeks = []
    Index = 0

    while Index < len(Dates) - 2:
        if Dates[Index].weekday() == 0:
            Week = []
            while Index < len(Dates) - 2 and Dates[Index].weekday() <= Dates[Index + 1].weekday():
                Week.append(Index)
                Index += 1
            Week.append(Index)
            Weeks.append(Week)
        Index += 1

    if Dates[-1].weekday() == 0:
        Weeks[-1].append(len(Dates) - 1)
    else:
        Weeks.append([len(Dates) - 1])

    return Weeks