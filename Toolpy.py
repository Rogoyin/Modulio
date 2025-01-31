
from typing import Callable, Any, NoReturn

def Imprimir_Docstring(Funcion: Callable[..., Any]) -> None:

    """
    Imprime el docstring de una función dada con formato mejorado.

    Esta función toma como entrada otra función y muestra su docstring 
    con un formato especial que incluye líneas decorativas para mejor 
    visualización.

    Parámetros:
    -----------
    Funcion : Callable[..., Any]
        La función cuyo docstring se va a imprimir.

    Retorna:
    --------
    None
        La función imprime el docstring de la función proporcionada.

    Lanza:
    ------
    ValueError
        Si el argumento proporcionado no es una función.

    """
    
    if not callable(Funcion):
        raise ValueError("El argumento proporcionado no es una función.")

    # Captura el docstring.
    Docstring_Capturado = Funcion.__doc__ or "No hay docstring disponible."
    # Se usa valor alternativo si no hay docstring.

    # Imprime el docstring capturado con formato.
    print("===" * 10)  # Línea decorativa.
    print(Docstring_Capturado)
    print("===" * 10)  # Línea decorativa.

