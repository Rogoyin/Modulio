import pandas as pd
from typing import Any, Dict, List, Set

def Agrupar_Diccionarios_Por_Elemento_Padre(
    Marco_De_Datos: pd.DataFrame, 
    Lista_De_Elementos: List[str], 
    Elemento_Padre: str, 
    Lista_De_Hijos: List[str]
) -> List[List[Dict[str, str]]]:

    """
    Agrupa diccionarios que contienen elementos hijos para cada elemento 
    padre.

    Parámetros:
        Marco_De_Datos: El DataFrame que contiene los datos.
        Lista_De_Elementos: Lista de valores de elementos padre para 
        agrupar.
        Elemento_Padre: El nombre de la columna a usar como elemento 
        padre.
        Lista_De_Hijos: Lista de nombres de elementos hijos a extraer.

    Retorna:
        Una lista de diccionarios agrupados para cada elemento padre.

    Ejemplo:
        >>> Elemento_Padre = 'Nombre'
        >>> Lista_De_Elementos = ['Jorge', 'Ramón']
        >>> Lista_De_Hijos = ['Edad', 'Ciudad']
        >>> Agrupar_Diccionarios_Por_Elemento_Padre(
        ...     Marco_De_Datos, Lista_De_Elementos, 
        ...     Elemento_Padre, Lista_De_Hijos
        ... )
        [['Jorge', {'Edad': 26}, {'Ciudad': 'Buenos Aires'}], 
         ['Ramón', {'Edad': 28}, {'Ciudad': 'Rio de Janeiro'}]]

    """

    Resultado = []

    for Padre in Lista_De_Elementos:
        Datos_Por_Elemento = [{Elemento_Padre: Padre}]

        for Indice, Fila in Marco_De_Datos.iterrows():
            if Padre == Fila[Elemento_Padre]:
                Diccionario = {
                    Hijo: Fila[Hijo] for Hijo in Lista_De_Hijos
                }
                Datos_Por_Elemento.append(Diccionario)
        
        Resultado.append(Datos_Por_Elemento)

    return Resultado

def Obtener_Claves_Por_Valor(
    Lista_De_Diccionarios: List[Dict[str, Any]], 
    Valor: Any
) -> List[str]:

    """
    Extrae las claves correspondientes a un valor específico de una 
    lista de diccionarios.

    Parámetros:
        Lista_De_Diccionarios (List[Dict[str, Any]]): Una lista de 
        diccionarios de donde extraer las claves.
        Valor (Any): El valor para el cual se deben extraer las claves.

    Retorna:
        List[str]: Una lista de claves correspondientes al valor 
        especificado.

    Ejemplo:
        >>> Obtener_Claves_Por_Valor([{'a': 1, 'b': 2}, {'c': 1}], 1)
        ['a', 'c']

    """

    Lista_De_Claves = []

    for Diccionario in Lista_De_Diccionarios:
        for Clave, Valor_Dict in Diccionario.items():
            # Agregar la clave si su valor coincide con el valor 
            # especificado.
            if Valor_Dict == Valor:
                Lista_De_Claves.append(Clave)

    return Lista_De_Claves

def Obtener_Valores_Por_Clave(
    Lista_De_Diccionarios: List[Dict[str, Any]], 
    Clave: str
) -> List[Any]:

    """
    Extrae los valores correspondientes a una clave específica de una 
    lista de diccionarios.

    Parámetros:
        Lista_De_Diccionarios (List[Dict[str, Any]]): Una lista de 
        diccionarios de donde extraer los valores.
        Clave (str): La clave para la cual se deben extraer los valores.

    Retorna:
        List[Any]: Una lista de valores correspondientes a la clave 
        especificada.

    Ejemplo:
        >>> Obtener_Valores_Por_Clave([{'a': 1, 'b': 2}, {'a': 3}], 'a')
        [1, 3]

    """

    Lista_De_Valores = []

    for Diccionario in Lista_De_Diccionarios:
        # Agregar el valor correspondiente a la clave a la lista de 
        # valores.
        Lista_De_Valores.append(Diccionario.get(Clave))

    return Lista_De_Valores

def Obtener_Clave_Por_Indice(
    Diccionario: Dict[str, Any], 
    Indice: int
) -> str:

    """
    Recupera una clave de un diccionario por su índice.

    Parámetros:
        Diccionario (Dict[str, Any]): El diccionario del cual recuperar 
        la clave.
        Indice (int): El índice de la clave a recuperar.

    Retorna:
        str: La clave en el índice especificado.

    Lanza:
        KeyError: Si el índice está fuera de rango.

    Ejemplo:
        >>> Obtener_Clave_Por_Indice({'a': 1, 'b': 2, 'c': 3}, 1)
        'b'

    """

    Contador = 0

    if Indice >= len(Diccionario):
        # Lanzar KeyError si el índice excede la longitud del 
        # diccionario.
        raise KeyError("El diccionario no tiene tantos índices.")
    
    for Clave in Diccionario.keys():
        if Contador == Indice:
            return str(Clave)
        Contador += 1

    # Esta línea asegura un retorno de string en caso de problemas 
    # inesperados.
    raise KeyError("Índice no encontrado en el diccionario.")

def Obtener_Valor_Por_Indice(
    Diccionario: Dict[str, Any], 
    Indice: int
) -> Any:

    """
    Recupera un valor de un diccionario por su índice.

    Parámetros:
        Diccionario (Dict[str, Any]): El diccionario del cual recuperar 
        el valor.
        Indice (int): El índice del valor a recuperar.

    Retorna:
        Any: El valor en el índice especificado.

    Lanza:
        IndexError: Si el índice está fuera de rango.

    Ejemplo:
        >>> Obtener_Valor_Por_Indice({'a': 1, 'b': 2, 'c': 3}, 1)
        2

    """

    Contador = 0

    if Indice >= len(Diccionario):
        # Lanzar IndexError si el índice excede la longitud del 
        # diccionario.
        raise IndexError("El diccionario no tiene tantos índices.")

    for Valor in Diccionario.values():
        if Contador == Indice:
            return Valor
        Contador += 1

    # Esta línea asegura un valor de retorno en caso de problemas 
    # inesperados.
    raise IndexError("Índice no encontrado en el diccionario.")

def Obtener_Claves_Unicas_Anidadas(Diccionario: Dict[str, Any]) -> Set[str]:

    """
    Recopila todas las claves únicas de un diccionario anidado de 
    forma recursiva.

    Parámetros:
        Diccionario (Dict[str, Any]): Diccionario de entrada, 
        potencialmente anidado.

    Retorna:
        Set[str]: Conjunto de todas las claves únicas encontradas en el 
        diccionario.

    Ejemplo:
        >>> Obtener_Claves_Unicas_Anidadas(
        ...     {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        ... )
        {'a', 'b', 'c', 'd', 'e'}

    """

    Claves = set(Diccionario.keys())

    for Valor in Diccionario.values():
        if isinstance(Valor, dict):
            Claves.update(Obtener_Claves_Unicas_Anidadas(Valor))

    return Claves

def Obtener_Valores_Unicos_Anidados(Diccionario: Dict[str, Any]) -> Set[Any]:

    """
    Recopila todos los valores únicos de un diccionario anidado de 
    forma recursiva.

    Parámetros:
        Diccionario (Dict[str, Any]): Diccionario de entrada, 
        potencialmente anidado.

    Retorna:
        Set[Any]: Conjunto de todos los valores únicos encontrados en el 
        diccionario.

    Ejemplo:
        >>> Obtener_Valores_Unicos_Anidados(
        ...     {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        ... )
        {1, 2, 3}

    """

    Valores = set()

    for Valor in Diccionario.values():
        if isinstance(Valor, dict):
            # Recopilar recursivamente valores de diccionarios anidados.
            Valores.update(Obtener_Valores_Unicos_Anidados(Valor))
        else:
            Valores.add(Valor)

    return Valores

def Obtener_Claves_Unicas_De_Diccionarios(
    Lista_De_Diccionarios: List[Dict[str, Any]]
) -> List[str]:

    """
    Extrae todas las claves únicas de una lista de diccionarios.

    Parámetros:
        Lista_De_Diccionarios (List[Dict[str, Any]]): Una lista de 
        diccionarios de donde extraer las claves.

    Retorna:
        List[str]: Una lista de claves únicas encontradas en todos los 
        diccionarios.

    Ejemplo:
        >>> Obtener_Claves_De_Diccionarios(
        ...     [{'a': 1, 'b': 2}, {'c': 3}]
        ... )
        ['a', 'b', 'c']

    """

    Conjunto_De_Claves: Set[str] = set()

    for Diccionario in Lista_De_Diccionarios:
        # Agregar todas las claves del diccionario al conjunto.
        Conjunto_De_Claves.update(Diccionario.keys())

    return list(Conjunto_De_Claves)

def Renombrar_Claves_Repetidas(
    Diccionario_Anidado: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Renombra recursivamente las claves en un diccionario anidado si 
    están repetidas a través de los niveles. Las claves repetidas se 
    renombran en el formato "Clave_Padre_Clave_Hijo".

    Parámetros:
        Diccionario_Anidado (Dict[str, Any]): Un diccionario que puede 
        contener diccionarios anidados.

    Retorna:
        Dict[str, Any]: Un nuevo diccionario con las claves renombradas 
        según sea necesario.

    Ejemplo:
        >>> Renombrar_Claves_Repetidas({"a": 1, "b": {"a": 2}})
        {'a': 1, 'b': {'b_a': 2}}

    """

    Claves_Vistas: Set[str] = set()

    def Renombrar_Claves(
        Diccionario: Dict[str, Any], 
        Clave_Padre: str
    ) -> Dict[str, Any]:
        Diccionario_Actualizado = {}

        for Clave, Valor in Diccionario.items():
            Nueva_Clave = (
                Clave if Clave not in Claves_Vistas 
                else f"{Clave_Padre}_{Clave}"
            )
            Claves_Vistas.add(Nueva_Clave)

            if isinstance(Valor, dict):
                # Renombrar recursivamente las claves en diccionarios 
                # anidados.
                Diccionario_Actualizado[Nueva_Clave] = Renombrar_Claves(
                    Valor, 
                    Nueva_Clave
                )
            else:
                Diccionario_Actualizado[Nueva_Clave] = Valor

        return Diccionario_Actualizado

    return Renombrar_Claves(Diccionario_Anidado, Clave_Padre = "Raiz")

def Contar_Diccionarios_Con_Clave(
    Lista_De_Diccionarios: List[Dict[str, Any]], 
    Clave: str
) -> int:

    """
    Cuenta cuántos diccionarios contienen una clave específica.

    Parámetros:
        Lista_De_Diccionarios (List[Dict[str, Any]]): La lista de 
        diccionarios a buscar.
        Clave (str): La clave cuyas ocurrencias se deben contar.

    Retorna:
        int: La cantidad de diccionarios que contienen la clave 
        especificada.

    Ejemplo:
        >>> Contar_Diccionarios_Con_Clave(
        ...     [{'a': 1, 'b': 2}, {'b': 3}, {'c': 4}], 
        ...     'b'
        ... )
        2

    """

    Contador = 0

    for Diccionario in Lista_De_Diccionarios:
        if Clave in Diccionario:
            # Incrementar el contador si la clave existe en el 
            # diccionario.
            Contador += 1

    return Contador
