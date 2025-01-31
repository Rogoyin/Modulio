import Frampy as fr
import pandas as pd
from typing import Optional, Tuple, Dict, List

def Obtener_Historial(
    df: pd.DataFrame, 
    Equipo1: str, 
    Equipo2: str, 
    Campo: Optional[str] = None, 
    Tipo_Torneo: Optional[str] = None, 
    Torneos: Optional[List[str]] = None, 
    Periodo: bool = False, 
    Anio1: int = 1900, 
    Anio2: int = 2024, 
    Partidos_Jugados: bool = True, 
    Victorias_Equipo1: bool = True, 
    Victorias_Equipo2: bool = True, 
    Padre: bool = True, 
    Diferencia: bool = True, 
    Diferencia_Goles: bool = True, 
    Min_Goles_Equipo1: Optional[int] = None, 
    Max_Goles_Equipo1: Optional[int] = None, 
    Min_Goles_Equipo2: Optional[int] = None, 
    Max_Goles_Equipo2: Optional[int] = None, 
    Estadio: Optional[str] = None, 
    Arbitro: Optional[str] = None
) -> Tuple[Dict[str, int], pd.DataFrame]:
    
    """
    Obtiene datos históricos de partidos entre dos equipos según varios 
    filtros.

    Parametros:
    - df (pd.DataFrame): DataFrame con el historial de partidos.
    - Equipo1 (str): Nombre del primer equipo.
    - Equipo2 (str): Nombre del segundo equipo.
    - Campo (Optional[str]): Especifica por qué equipo filtrar.
    - Tipo_Torneo (Optional[str]): Filtrar por tipo de torneo.
    - Torneos (Optional[List[str]]): Lista de torneos específicos a filtrar.
    - Periodo (bool): Si se debe filtrar por rango de años.
    - Anio1 (int): Año inicial para filtrar.
    - Anio2 (int): Año final para filtrar.
    - Partidos_Jugados (bool): Incluir total de partidos en resultados.
    - Victorias_Equipo1 (bool): Incluir victorias del Equipo1.
    - Victorias_Equipo2 (bool): Incluir victorias del Equipo2.
    - Padre (bool): Identificar el equipo dominante.
    - Diferencia (bool): Incluir diferencia de victorias.
    - Diferencia_Goles (bool): Incluir diferencia de goles.
    - Min_Goles_Equipo1 (Optional[int]): Goles mínimos del Equipo1.
    - Max_Goles_Equipo1 (Optional[int]): Goles máximos del Equipo1.
    - Min_Goles_Equipo2 (Optional[int]): Goles mínimos del Equipo2.
    - Max_Goles_Equipo2 (Optional[int]): Goles máximos del Equipo2.
    - Estadio (Optional[str]): Filtrar por nombre de estadio.
    - Arbitro (Optional[str]): Filtrar por nombre de árbitro.

    Retorna:
    - Tuple[Dict[str, int], pd.DataFrame]: Un diccionario con datos de 
      partidos y un DataFrame de partidos filtrados.

    """
    
    Datos_Historial = {}
    
    df_Historial = fr.Get_Selected_Rows_By_Two_Columns(
        df, 
        'Home_Team', 
        'Away_Team', 
        [Equipo1, Equipo2], 
        Condition='Match either'
    )

    if Campo == 'Equipo1':
        df_Historial = df_Historial[
            df_Historial['Home_Team'] == Equipo1
        ]
    elif Campo == 'Equipo2':
        df_Historial = df_Historial[
            df_Historial['Home_Team'] == Equipo2
        ]

    if Tipo_Torneo is not None:
        df_Historial = df_Historial[
            df_Historial['Tournament'] == Tipo_Torneo
        ]

    if Torneos is not None:
        df_Historial = df_Historial[
            df_Historial['Tournament'].isin(Torneos)
        ]
    
    if Periodo:
        df_Historial = df_Historial[
            (df_Historial['Year'] >= Anio1) & 
            (df_Historial['Year'] <= Anio2)
        ]

    if Min_Goles_Equipo1 is not None:
        df_Historial = df_Historial[
            ((df_Historial['Home_Team'] == Equipo1) & 
             (df_Historial['Home_Goals'] >= Min_Goles_Equipo1)) |
            ((df_Historial['Away_Team'] == Equipo1) & 
             (df_Historial['Away_Goals'] >= Min_Goles_Equipo1))
        ]
    
    if Max_Goles_Equipo1 is not None:
        df_Historial = df_Historial[
            ((df_Historial['Home_Team'] == Equipo1) & 
             (df_Historial['Home_Goals'] <= Max_Goles_Equipo1)) |
            ((df_Historial['Away_Team'] == Equipo1) & 
             (df_Historial['Away_Goals'] <= Max_Goles_Equipo1))
        ]

    if Min_Goles_Equipo2 is not None:
        df_Historial = df_Historial[
            ((df_Historial['Home_Team'] == Equipo2) & 
             (df_Historial['Home_Goals'] >= Min_Goles_Equipo2)) |
            ((df_Historial['Away_Team'] == Equipo2) & 
             (df_Historial['Away_Goals'] >= Min_Goles_Equipo2))
        ]
    
    if Max_Goles_Equipo2 is not None:
        df_Historial = df_Historial[
            ((df_Historial['Home_Team'] == Equipo2) & 
             (df_Historial['Home_Goals'] <= Max_Goles_Equipo2)) |
            ((df_Historial['Away_Team'] == Equipo2) & 
             (df_Historial['Away_Goals'] <= Max_Goles_Equipo2))
        ]

    if Estadio is not None:
        df_Historial = df_Historial[
            df_Historial['Stadium'] == Estadio
        ]
    
    if Arbitro is not None:
        df_Historial = df_Historial[
            df_Historial['Referee'] == Arbitro
        ]

    if Partidos_Jugados:
        Datos_Historial['Partidos'] = len(df_Historial)

    if Victorias_Equipo1:
        Datos_Historial[f'Victorias {Equipo1}:'] = len(df_Historial[
            ((df_Historial['Result'] == 'Home') & 
             (df_Historial['Home_Team'] == Equipo1)) |
            ((df_Historial['Result'] == 'Away') & 
             (df_Historial['Away_Team'] == Equipo1))
        ])

    if Victorias_Equipo2:
        Datos_Historial[f'Victorias {Equipo2}:'] = len(df_Historial[
            ((df_Historial['Result'] == 'Home') & 
             (df_Historial['Home_Team'] == Equipo2)) |
            ((df_Historial['Result'] == 'Away') & 
             (df_Historial['Away_Team'] == Equipo2))
        ])
    
    if Diferencia:
        Victorias_Equipo1 = Datos_Historial.get(f'Victorias {Equipo1}:', 0)
        Victorias_Equipo2 = Datos_Historial.get(f'Victorias {Equipo2}:', 0)
        
        if Victorias_Equipo1 > Victorias_Equipo2:
            Datos_Historial['Padre'] = Equipo1
        elif Victorias_Equipo2 > Victorias_Equipo1:
            Datos_Historial['Padre'] = Equipo2
        else:
            Datos_Historial['Padre'] = 'Ninguno'
    
    if Diferencia:
        Datos_Historial['Diferencia'] = '+' + str(
            abs(Victorias_Equipo1 - Victorias_Equipo2)
        )

    if Diferencia_Goles:
        Datos_Historial['Diferencia_Goles'] = '+' + str(abs(
            df_Historial['Home_Goals'].sum() - 
            df_Historial['Away_Goals'].sum()
        ))

    return Datos_Historial, df_Historial