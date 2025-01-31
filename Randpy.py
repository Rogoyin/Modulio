import random
from typing import List

def Generar_Numeros_Aleatorios(Cantidad: int, Valor_Minimo: int, 
    Valor_Maximo: int) -> List[int]:

    """
    Genera una lista de números enteros aleatorios dentro de un rango 
    especificado.

    Esta función crea una lista de números enteros aleatorios, donde 
    cada número está dentro del rango definido por los valores mínimo 
    y máximo especificados.

    Parámetros:
    -----------
    Cantidad : int
        La cantidad de números aleatorios a generar.

    Valor_Minimo : int
        El valor mínimo para los números aleatorios.

    Valor_Maximo : int
        El valor máximo para los números aleatorios.

    Retorna:
    --------
    List[int]
        Una lista de números enteros aleatorios dentro del rango 
        especificado.

    Ejemplo:
    --------
    >>> Generar_Numeros_Aleatorios(5, 1, 10)
    [3, 7, 2, 10, 6]

    """

    return [random.randint(Valor_Minimo, Valor_Maximo) 
            for _ in range(Cantidad)]

def Generar_Letras_Aleatorias(Cantidad: int, 
    Incluir_Mayusculas: bool = True) -> List[str]:

    """
    Genera una lista de letras aleatorias del alfabeto.

    Esta función crea una lista de letras aleatorias, con la opción 
    de incluir tanto minúsculas como mayúsculas.

    Parámetros:
    -----------
    Cantidad : int
        La cantidad de letras aleatorias a generar.

    Incluir_Mayusculas : bool
        Indica si se deben incluir letras mayúsculas. Por defecto 
        es True.

    Retorna:
    --------
    List[str]
        Una lista de letras aleatorias del alfabeto.

    Ejemplo:
    --------
    >>> Generar_Letras_Aleatorias(5, Incluir_Mayusculas=True)
    ['A', 'b', 'Z', 'm', 'P']

    """

    Letras = "abcdefghijklmnopqrstuvwxyz"
    if Incluir_Mayusculas:
        Letras += Letras.upper()

    return [random.choice(Letras) for _ in range(Cantidad)]