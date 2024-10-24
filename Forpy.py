'''
--OPERACIONES EXCLUSIVAS DEL PROGRAMA DEL FORRAJE--
'''

import Stringpy
from typing import List
import pandas as pd

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# Diccionarios.
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

Markup_And_Unity = {
    "Gato Granel": {"Markup %": "48", "Unidad": "KG"},
    "Gato": {"Markup %": "32", "Unidad": "UN"},
    "Perro Adulto Granel": {"Markup %": "48", "Unidad": "KG"},
    "Perro Adulto": {"Markup %": "32", "Unidad": "UN"},
    "Perro Cachorro Granel": {"Markup %": "48", "Unidad": "KG"},
    "Perro Cachorro": {"Markup %": "32", "Unidad": "UN"},
    "Ropa": {"Markup %": "70", "Unidad": "UN"},
    "Mascotas": {"Markup %": "50", "Unidad": "UN"},
    "Limpieza": {"Markup %": "50", "Unidad": "UN"},
    "Veterinaria": {"Markup %": "60", "Unidad": "UN"},
    "Balanceados Granel": {"Markup %": "45", "Unidad": "KG"},
    "Balanceados": {"Markup %": "32", "Unidad": "UN"},
    "Venenos": {"Markup %": "50", "Unidad": "UN"},
    "Liquidos": {"Markup %": "40", "Unidad": "UN"},
    "Pileta": {"Markup %": "50", "Unidad": "UN"},
    "General": {"Markup %": "50", "Unidad": "UN"},
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# Funciones.
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def Column_Provider_Processing(df: pd.DataFrame, Columns_Providers: List[str]) -> pd.DataFrame:
    
    """
    Processes specified columns containing provider prices by applying 
    a series of text transformations and conversions.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the columns to be 
      processed.
    - Columns_Providers (List[str]): A list of column names in the 
      DataFrame that contain provider prices to process.

    Returns:
    - pd.DataFrame: The modified DataFrame with processed columns.

    Notes:
    - The processing includes converting values to strings, removing 
      unwanted characters, replacing empty strings with '0', and 
      converting the results to floats.

    """

    for Provider in Columns_Providers:
        df[Provider] = df[Provider].astype(str).apply(Stringpy.Remove_Everything_Least_Numbers)
        df[Provider] = df[Provider].apply(Stringpy.Remove_Last_Character)
        df[Provider] = df[Provider].replace("", "0")
        df[Provider] = df[Provider].astype(float)
    return df

def Find_Best_Provider(df: pd.DataFrame, Columns_Providers: List[str]) -> pd.DataFrame:

    """
    Identifies the best provider based on matching values in specified columns.

    Parameters:
    - df: DataFrame containing provider information and prices.
    - Columns_Providers: List of column names to check for matching values.

    Returns:
    - The modified DataFrame with the 'Proveedor' column updated to the best provider.

    """

    for Index, Row in df.iterrows():
        for Provider in Columns_Providers:
            if Row["Precio"] == Row[Provider]:
                df.at[Index, "Proveedor"] = Provider
                break
    return df


