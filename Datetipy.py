import datetime as dt

def Ordenar_Fechas_Por_Semanas(Fechas: list[dt.datetime]) -> list[list[int]]:
    
    """
    Ordena una lista de fechas por semanas y devuelve los índices de los días.

    Parámetros:
    - Fechas (list[datetime]): Una lista de fechas, donde cada elemento es un 
      objeto datetime que representa un día, mes, año y posiblemente hora.

    Retorna:
    - list[list[int]]: Una lista de semanas, donde cada semana contiene los 
      índices de los días dentro de esa semana.
    
    """

    Semanas = []
    Indice = 0

    while Indice < len(Fechas) - 2:
        # Verificar si es lunes.
        if Fechas[Indice].weekday() == 0:  
            Semana = []
            while (Indice < len(Fechas) - 2 and 
                   Fechas[Indice].weekday() <= Fechas[Indice + 1].weekday()):
                # Agregar el índice de la fecha.
                Semana.append(Indice)  
                Indice += 1
            # Agregar el último índice de la semana.
            Semana.append(Indice)  
            # Añadir la semana a la lista de semanas.
            Semanas.append(Semana)  
        Indice += 1

    # Si la última fecha es un lunes.
    if Fechas[-1].weekday() == 0:  
        # Agregar el último índice a la última semana.
        Semanas[-1].append(len(Fechas) - 1)  
    else:
        # Añadir la última fecha como una nueva semana.
        Semanas.append([len(Fechas) - 1])  

    return Semanas

def Agregar_Delta_Tiempo(Minutos: int = 0, Horas: int = 0, Dias: int = 0, 
                        Futuro: bool = True, Texto: bool = False):
    
    """
    Agrega o resta un delta de tiempo desde el datetime actual.

    Esta función calcula un nuevo datetime agregando o restando una cantidad 
    específica de tiempo (en minutos, horas y días) desde el datetime actual. 
    Puede devolver el resultado como una cadena formateada o como un objeto 
    datetime.

    Parámetros:
    Minutos (int): Número de minutos a agregar o restar. Por defecto es 0.
    Horas (int): Número de horas a agregar o restar. Por defecto es 0.
    Dias (int): Número de días a agregar o restar. Por defecto es 0.
    Futuro (bool): Si es True, suma el delta. Si es False, lo resta. 
                   Por defecto es True.
    Texto (bool): Si es True, retorna el resultado como cadena formateada. 
                  Si es False, retorna un objeto datetime. Por defecto es False.

    Retorna:
    datetime o str: Retorna el nuevo objeto datetime si Texto es False, 
                   o una cadena formateada si Texto es True.
    """

    Ahora = dt.datetime.now()
    Periodo = dt.timedelta(days=Dias, hours=Horas, minutes=Minutos)

    if Futuro:
        Momento = Ahora + Periodo
    else:
        Momento = Ahora - Periodo

    if Texto:
        return Momento.strftime('%Y-%m-%d %H:%M')
    else:
        return Momento