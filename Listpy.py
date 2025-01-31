import numpy as np
import re
import itertools

def Verificar_Elementos_Iterables_De_Lista(Lista: list):

    """
    Verifica si todos los elementos en una lista son tipos iterables 
    (lista, tupla, diccionario).

    Esta función revisa cada elemento en la lista proporcionada para asegurar 
    que sea una instancia de un tipo iterable. Si todos los elementos son 
    iterables, la función devuelve True; en caso contrario, devuelve False.

    Parámetros:
    -----------
    Lista : list
        Una lista de elementos para verificar.

    Retorna:
    --------
    bool
        True si todos los elementos son iterables, False en caso contrario.

    Ejemplo:
    ---------
    >>> Resultado = Verificar_Elementos_Iterables_De_Lista([[1, 2], (3, 4), {}])
    >>> print(Resultado)
    True

    """

    for Elemento in Lista:
        if not isinstance(Elemento, (list, tuple, dict)):
            return False
    return True

def Convertir_Lista_De_Tuplas_A_Lista_De_Listas(Lista_De_Tuplas: list):

    """
    Convierte una lista de tuplas a una lista de listas.

    Esta función toma una lista de tuplas como entrada y convierte cada 
    tupla en una lista. Si la entrada contiene elementos no iterables, 
    devuelve la lista original como una lista.

    Parámetros:
    -----------
    Lista_De_Tuplas : list
        Una lista de tuplas para convertir.

    Retorna:
    --------
    list
        Una lista de listas si todos los elementos son tuplas; en caso 
        contrario, devuelve la lista original.

    Ejemplo:
    ---------
    >>> Resultado = Convertir_Lista_De_Tuplas_A_Lista_De_Listas([(1, 2), (3, 4)])
    >>> print(Resultado)
    [[1, 2], [3, 4]]

    """

    if Verificar_Elementos_Iterables_De_Lista(Lista_De_Tuplas):
        Lista_De_Listas = []
        for Tupla in Lista_De_Tuplas:
            Lista_De_Listas.append(list(Tupla))
        return Lista_De_Listas
    else:
        return list(Lista_De_Tuplas)

def Encontrar_Posicion_Maxima_En_Segmento(Lista: list, Indice_Inicio: int, 
    Indice_Fin: int) -> int:

    """
    Encuentra la posición del valor máximo dentro de un segmento 
    específico de una lista.

    Esta función determina el índice del valor máximo en un segmento 
    de la lista proporcionada, definido por los índices de inicio y fin.

    Parámetros:
    -----------
    Lista : list
        La lista donde se buscará la posición del valor máximo.

    Indice_Inicio : int
        El índice de inicio del segmento.

    Indice_Fin : int
        El índice final del segmento.

    Retorna:
    --------
    int
        El índice del valor máximo dentro del segmento especificado.

    Ejemplo:
    ---------
    >>> Resultado = Encontrar_Posicion_Maxima_En_Segmento([1, 3, 2, 5, 4], 1, 3)
    >>> print(Resultado)
    3

    """

    Segmento = Lista[Indice_Inicio:Indice_Fin + 1]
    return Segmento.index(max(Segmento))

def Ordenar_Listas_Por_Referencia(Lista_Referencia: list, 
    *Listas_A_Ordenar: list) -> tuple:

    """
    Ordena una lista de referencia y otras listas asociadas basándose 
    en el orden de la lista de referencia.

    Esta función ordena la lista de referencia proporcionada en orden 
    ascendente y reorganiza las otras listas de acuerdo con el nuevo 
    orden de la lista de referencia.

    Parámetros:
    -----------
    Lista_Referencia : list
        La lista a ordenar, que dicta el orden de ordenamiento para 
        las otras listas.

    *Listas_A_Ordenar : list
        Listas adicionales que serán ordenadas en el mismo orden que 
        la lista de referencia.

    Retorna:
    --------
    tuple
        Una tupla que contiene la lista de referencia ordenada y las 
        listas asociadas ordenadas.

    Ejemplo:
    ---------
    >>> lista_ref, listas_ordenadas = Ordenar_Listas_Por_Referencia(
            [3, 1, 2], [30, 10, 20])
    >>> print(lista_ref, listas_ordenadas)
    [1, 2, 3], ([10, 20, 30],)

    """

    Indice_Actual = len(Lista_Referencia) - 1

    while Indice_Actual > 0:
        Posicion_Maxima = Encontrar_Posicion_Maxima_En_Segmento(
            Lista_Referencia, 0, Indice_Actual)
            
        Lista_Referencia[Posicion_Maxima], Lista_Referencia[Indice_Actual] = \
            Lista_Referencia[Indice_Actual], Lista_Referencia[Posicion_Maxima]
        
        for Lista in Listas_A_Ordenar:
            Lista[Posicion_Maxima], Lista[Indice_Actual] = \
                Lista[Indice_Actual], Lista[Posicion_Maxima]
        
        Indice_Actual -= 1
        
    return Lista_Referencia, tuple(Listas_A_Ordenar)

def Calcular_Promedio_De_Listas(Lista_De_Listas: list) -> list:

    """
    Calcula el promedio de cada lista dentro de una lista de listas.

    Esta función computa el valor promedio de cada sublista en la lista 
    de listas proporcionada.

    Parámetros:
    -----------
    Lista_De_Listas : list
        Una lista que contiene múltiples listas para las cuales se 
        calcularán los promedios.

    Retorna:
    --------
    list
        Una lista de valores promedio correspondientes a cada sublista.

    Ejemplo:
    ---------
    >>> Promedios = Calcular_Promedio_De_Listas([[1, 2, 3], [4, 5, 6]])
    >>> print(Promedios)
    [2.0, 5.0]

    """

    Promedios = [np.mean(Lista) for Lista in Lista_De_Listas]
    return Promedios

def Transponer_Lista_De_Listas(Lista_De_Listas: list) -> list:

    """
    Transpone una lista de listas, convirtiendo filas en columnas y 
    viceversa.

    Esta función reorganiza la lista de listas proporcionada de manera 
    que la primera sublista se convierte en la primera columna, la 
    segunda sublista en la segunda columna, y así sucesivamente.

    Parámetros:
    -----------
    Lista_De_Listas : list
        Una lista de listas para ser transpuesta.

    Retorna:
    --------
    list
        Una nueva lista de listas que representa la versión transpuesta 
        de la lista de entrada.

    Ejemplo:
    ---------
    >>> Transpuesta = Transponer_Lista_De_Listas([[1, 2, 3], [4, 5, 6]])
    >>> print(Transpuesta)
    [[1, 4], [2, 5], [3, 6]]

    """

    Lista_Transpuesta = list(map(list, zip(*Lista_De_Listas)))
    return Lista_Transpuesta

def Cortar_Iterable_Por_Referencia(Iterable, Elemento_Base, Remover = 'Antes', 
    Incluir = True, Apariciones = 1):

    """
    Corta un iterable basado en la posición de un elemento base 
    especificado.

    Esta función modifica el iterable proporcionado cortándolo según 
    la primera ocurrencia de un elemento especificado. El corte puede 
    eliminar elementos antes o después del elemento base.

    Parámetros:
    -----------
    Iterable : iterable
        El iterable a ser cortado.

    Elemento_Base : object
        El elemento que sirve como punto de referencia para el corte.

    Remover : str
        Indica si se deben remover elementos 'Antes' o 'Despues' del 
        elemento base. Por defecto es 'Antes'.

    Incluir : bool
        Indica si se debe incluir el elemento base en el resultado. 
        Por defecto es True.

    Apariciones : int
        La ocurrencia del elemento base a usar para el corte. 
        Por defecto es 1.

    Retorna:
    --------
    iterable
        El iterable cortado.

    Lanza:
    -------
    KeyError
        Si el elemento base no se encuentra en el iterable.

    Ejemplo:
    ---------
    >>> Resultado = Cortar_Iterable_Por_Referencia([1, 2, 3, 4], 3)
    >>> print(Resultado)
    [4]

    """

    if Elemento_Base not in Iterable:
        raise KeyError('El elemento debe estar en el iterable.')
    
    Contador = 0
    for Indice, Elemento in enumerate(Iterable):
        if Elemento == Elemento_Base:
            Contador += 1
            if Contador == Apariciones:
                if Remover == 'Antes':
                    if Incluir == False:
                        Indice += 1
                    Iterable = Iterable[Indice:]
                else:
                    if Incluir:
                        Indice += 1
                    Iterable = Iterable[:Indice]
    return Iterable

def Obtener_Indices_De_Todas_Las_Ocurrencias(Iterable, 
    Elemento_Objetivo) -> list:

    """
    Recupera los índices de todas las ocurrencias de un elemento 
    específico en un iterable.

    Esta función itera a través del iterable proporcionado y recopila 
    los índices donde aparece el elemento objetivo.

    Parámetros:
    -----------
    Iterable : iterable
        El iterable en el cual buscar el elemento objetivo.

    Elemento_Objetivo : object
        El elemento cuyos índices se deben encontrar.

    Retorna:
    --------
    list
        Una lista de índices donde ocurre el elemento objetivo.

    Ejemplo:
    ---------
    >>> Indices = Obtener_Indices_De_Todas_Las_Ocurrencias([1, 2, 3, 2, 4], 2)
    >>> print(Indices)
    [1, 3]

    """

    Contador = 1
    Ocurrencias = []

    for Indice, Elemento in enumerate(Iterable):
        if Elemento == Elemento_Objetivo:
            Ocurrencias.append(Indice)
            Contador += 1
    
    return Ocurrencias

def Encontrar_Y_Reemplazar(Iterable, Elemento_Objetivo, Nuevo_Valor, 
    Ocurrencia = 1):

    """
    Encuentra y reemplaza una ocurrencia específica de un elemento en 
    un iterable.

    Esta función busca el elemento objetivo dentro del iterable y 
    reemplaza la ocurrencia especificada con un nuevo valor.

    Parámetros:
    -----------
    Iterable : iterable
        El iterable en el cual encontrar y reemplazar el elemento 
        objetivo.

    Elemento_Objetivo : object
        El elemento a ser reemplazado.

    Nuevo_Valor : object
        El valor que reemplazará al elemento objetivo.

    Ocurrencia : int
        La ocurrencia específica del elemento objetivo a reemplazar. 
        Por defecto es 1.

    Retorna:
    --------
    iterable
        El iterable modificado después del reemplazo.

    Lanza:
    -------
    KeyError
        Si el elemento objetivo no aparece el número especificado 
        de veces.

    Ejemplo:
    ---------
    >>> Modificado = Encontrar_Y_Reemplazar([1, 2, 2, 3], 2, 5, 1)
    >>> print(Modificado)
    [1, 5, 2, 3]

    """

    Indices_Ocurrencias = Obtener_Indices_De_Todas_Las_Ocurrencias(
        Iterable, Elemento_Objetivo)
    if Ocurrencia > len(Indices_Ocurrencias):
        raise KeyError(
            f"El elemento objetivo {Elemento_Objetivo} no aparece "
            f"{Ocurrencia} veces: aparece menos."
        )
    
    Indice_A_Cambiar = Indices_Ocurrencias[Ocurrencia - 1]
    Iterable[Indice_A_Cambiar] = Nuevo_Valor
    return Iterable

def Obtener_Indices_Sublista(Lista, Sublista):

    """
    Recupera los índices de todas las ocurrencias de una sublista 
    específica dentro de una lista.

    Esta función busca la sublista proporcionada en la lista principal 
    y devuelve los índices iniciales de cada ocurrencia.

    Parámetros:
    -----------
    Lista : list
        La lista en la cual buscar la sublista.

    Sublista : list
        La sublista a encontrar dentro de la lista principal.

    Retorna:
    --------
    list
        Una lista de índices iniciales donde ocurre la sublista.

    Ejemplo:
    ---------
    >>> Indices = Obtener_Indices_Sublista([1, 2, 3, 2, 4], [2])
    >>> print(Indices)
    [1, 3]

    """

    Lista_De_Indices = []
    for Indice, Elemento in enumerate(Lista):
        if Elemento == Sublista[0]:
            if Lista[Indice:Indice+len(Sublista)] == Sublista:
                Lista_De_Indices.append(Indice)
    return Lista_De_Indices

def Filtrar_Lista_Por_Criterio(Lista: list, Criterio: str = "=", 
    Valor = None, Valor2 = None):

    """
    Filtra una lista basada en criterios específicos.

    Esta función itera a través de la lista de entrada y aplica el 
    criterio dado para filtrar los elementos. Los elementos filtrados 
    se devuelven en una nueva lista.

    Parámetros:
    -----------
    Lista : list
        La lista a ser filtrada.

    Criterio : str
        El criterio a aplicar para el filtrado. Puede ser uno de:
        =, !=, >, <, <=, >=, 
        Contiene, No_Contiene, Empieza_Con, Termina_Con, En, No_En,
        Es_Instancia, Entre, Longitud, Es_Nulo, No_Es_Nulo, Modulo,
        Regex, Todos_Verdaderos, Alguno_Verdadero, Funcion_Personal,
        Tipo_Igual, En_Rango. Por defecto es "=".

    Valor : object
        El valor contra el cual comparar según el criterio especificado.

    Valor2 : object
        Un segundo valor a usar para ciertos criterios, como 'Entre' 
        o 'Longitud'.

    Retorna:
    --------
    list
        Una nueva lista que contiene los elementos que cumplen el 
        criterio especificado.

    Lanza:
    -------
    KeyError
        Si se especifica un criterio no soportado.

    Ejemplo:
    ---------
    >>> Filtrado = Filtrar_Lista_Por_Criterio([1, 2, 3, 4], Criterio = '>', 
            Valor = 2)
    >>> print(Filtrado)
    [3, 4]

    """

    Lista_Final = []
    
    for Elemento in Lista:
        if Criterio == "=":
            if Elemento == Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "!=":
            if Elemento != Valor:
                Lista_Final.append(Elemento)
        elif Criterio == ">":
            if Elemento > Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "<":
            if Elemento < Valor:
                Lista_Final.append(Elemento)
        elif Criterio == ">=":
            if Elemento >= Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "<=":
            if Elemento <= Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "Contiene":
            if isinstance(Elemento, str) and isinstance(Valor, str) and \
                Valor in Elemento:
                Lista_Final.append(Elemento)
        elif Criterio == "No_Contiene":
            if isinstance(Elemento, str) and isinstance(Valor, str) and \
                Valor not in Elemento:
                Lista_Final.append(Elemento)
        elif Criterio == "Empieza_Con":
            if isinstance(Elemento, str) and isinstance(Valor, str) and \
                Elemento.startswith(Valor):
                Lista_Final.append(Elemento)
        elif Criterio == "Termina_Con":
            if isinstance(Elemento, str) and isinstance(Valor, (str, tuple)) and \
                Elemento.endswith(Valor):
                Lista_Final.append(Elemento)
        elif Criterio == "En":
            if Elemento in Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "No_En":
            if Elemento not in Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "Es_Instancia":
            if Valor is not None and isinstance(Valor, type) and \
                isinstance(Elemento, Valor):
                Lista_Final.append(Elemento)
        elif Criterio == "Entre":
            if Valor <= Elemento <= Valor2:
                Lista_Final.append(Elemento)
        elif Criterio == "Longitud":
            if hasattr(Elemento, '__len__') and len(Elemento) == Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "Es_Nulo":
            if Elemento is None:
                Lista_Final.append(Elemento)
        elif Criterio == "No_Es_Nulo":
            if Elemento is not None:
                Lista_Final.append(Elemento)
        elif Criterio == "Modulo":
            if Elemento % Valor == Valor2:
                Lista_Final.append(Elemento)
        elif Criterio == "Regex":
            if isinstance(Elemento, str) and isinstance(Valor, (str, re.Pattern)) \
                and re.search(Valor, Elemento):
                Lista_Final.append(Elemento)
        elif Criterio == "Todos_Verdaderos":
            if Valor is not None and callable(Valor) and \
                all(Valor(E) for E in Elemento):
                Lista_Final.append(Elemento)
        elif Criterio == "Alguno_Verdadero":
            if Valor is not None and callable(Valor) and \
                any(Valor(E) for E in Elemento):
                Lista_Final.append(Elemento)
        elif Criterio == "Funcion_Personal":
            if Valor is not None and callable(Valor) and Valor(Elemento):
                Lista_Final.append(Elemento)
        elif Criterio == "Tipo_Igual":
            if type(Elemento) == Valor:
                Lista_Final.append(Elemento)
        elif Criterio == "En_Rango":
            if Valor < Elemento < Valor2:
                Lista_Final.append(Elemento)
        else:
            raise KeyError(
                "El criterio debe ser uno de: =, !=, >, <, <=, >=, "
                "Contiene, No_Contiene, Empieza_Con, Termina_Con, En, "
                "No_En, Es_Instancia, Entre, Longitud, Es_Nulo, "
                "No_Es_Nulo, Modulo, Regex, Todos_Verdaderos, "
                "Alguno_Verdadero, Funcion_Personal, Tipo_Igual, En_Rango."
            )
    
    return Lista_Final

def Eliminar_Duplicados_En_Lista(Lista: list):

    """
    Elimina elementos duplicados de una lista.

    Esta función itera a través de la lista proporcionada y devuelve 
    una nueva lista que contiene solo elementos únicos.

    Parámetros:
    -----------
    Lista : list
        La lista de la cual se deben eliminar los duplicados.

    Retorna:
    --------
    list
        Una nueva lista que contiene solo elementos únicos.

    Ejemplo:
    ---------
    >>> Lista_Unica = Eliminar_Duplicados_En_Lista([1, 2, 2, 3])
    >>> print(Lista_Unica)
    [1, 2, 3]

    """

    Lista_Sin_Duplicados = []
    Vistos = set()  # Para búsquedas optimizadas.
    for Elemento in Lista:
        if Elemento not in Vistos:
            Lista_Sin_Duplicados.append(Elemento)
            Vistos.add(Elemento)
    
    return Lista_Sin_Duplicados

def Encontrar_Elemento(Lista: list, Valor_Elemento: object, 
    Obtener_Indice: bool = False):

    """
    Encuentra un elemento en una lista y opcionalmente recupera su 
    índice.

    Esta función verifica si el valor especificado está presente en la 
    lista proporcionada. Si Obtener_Indice es True, devuelve los 
    índices de todas las ocurrencias; en caso contrario, devuelve un 
    booleano indicando su presencia.

    Parámetros:
    -----------
    Lista : list
        La lista en la cual buscar el valor especificado.

    Valor_Elemento : object
        El valor a buscar en la lista.

    Obtener_Indice : bool
        Si se deben devolver los índices de las ocurrencias en lugar 
        de un booleano. Por defecto es False.

    Retorna:
    --------
    bool or list
        True si el elemento se encuentra (y Obtener_Indice es False); 
        en caso contrario, una lista de índices si Obtener_Indice 
        es True.

    Ejemplo:
    ---------
    >>> Resultado = Encontrar_Elemento([1, 2, 3], 2)
    >>> print(Resultado)
    True

    >>> Indices = Encontrar_Elemento([1, 2, 3, 2], 2, True)
    >>> print(Indices)
    [1, 3]

    """

    Lista_Indices = []

    for Indice, Elemento in enumerate(Lista):
        if Valor_Elemento == Elemento:
            if Obtener_Indice == False:
                return True
            else:
                Lista_Indices.append(Indice)
    
    if Lista_Indices is None:
        return False
    else:
        return Lista_Indices

def Maximo_Caracteres(Iterable: list | tuple | set | dict) -> int:

    """
    Encuentra el número máximo de caracteres entre los elementos de 
    un iterable.

    Esta función calcula la longitud máxima de las representaciones 
    de cadena de los elementos en el iterable proporcionado.

    Parámetros:
    -----------
    Iterable : iterable
        El iterable que contiene los elementos a evaluar.

    Retorna:
    --------
    int
        El número máximo de caracteres entre los elementos.

    Ejemplo:
    ---------
    >>> Max_Caracteres = Maximo_Caracteres([1, 'abc', 3.14159])
    >>> print(Max_Caracteres)
    5

    """

    Maximo_De_Caracteres = 0

    for Elemento in Iterable:
        Caracteres = len(str(Elemento))

        if Caracteres > Maximo_De_Caracteres:
            Maximo_De_Caracteres = Caracteres   

    return Maximo_De_Caracteres

def Generar_Todas_Las_Combinaciones(Lista: list, Elementos: int) -> list:

    """
    Genera todas las combinaciones de una longitud específica a partir 
    de una lista.

    Esta función devuelve todas las combinaciones posibles de un 
    tamaño dado a partir de la lista de entrada.

    Parámetros:
    -----------
    Lista : list
        La lista a partir de la cual se generarán las combinaciones.

    Elementos : int
        El número de elementos en cada combinación.

    Retorna:
    --------
    list
        Una lista de tuplas que representa todas las combinaciones 
        posibles.

    Lanza:
    -------
    ValueError
        Si el número de elementos es mayor que la longitud de la lista.

    Ejemplo:
    ---------
    >>> Combinaciones = Generar_Todas_Las_Combinaciones([1, 2, 3, 4], 2)
    >>> print(Combinaciones)
    [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    
    """

    if Elementos > len(Lista):
        raise ValueError(
            "El número de elementos no puede ser mayor que la longitud "
            "de la lista."
        )

    Lista_De_Combinaciones = list(itertools.combinations(Lista, Elementos))

    return Lista_De_Combinaciones

def Encontrar_Elementos_Diferentes(Primera_Lista: list, 
    Segunda_Lista: list) -> list:

    """
    Encuentra elementos que están presentes en la primera lista pero 
    no en la segunda.

    Esta función compara dos listas y encuentra los elementos que solo 
    existen en la primera lista.

    Parámetros:
    -----------
    Primera_Lista : list
        La lista en la que buscar elementos únicos.

    Segunda_Lista : list
        La lista contra la cual comparar.

    Retorna:
    --------
    list
        Una lista que contiene los elementos que están en la primera 
        lista pero no en la segunda lista.

    Ejemplo:
    ---------
    >>> Elementos = Encontrar_Elementos_Diferentes([1, 2, 3], [2, 4])
    >>> print(Elementos)
    [1, 3]

    """

    Elementos_Unicos = [Elemento for Elemento in Primera_Lista 
                       if Elemento not in Segunda_Lista]

    return Elementos_Unicos