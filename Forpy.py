'''
--OPERACIONES EXCLUSIVAS DEL PROGRAMA DEL FORRAJE--
'''

import Stringpy
from typing import List
import pandas as pd
import time
import pyautogui
import pygetwindow as gw
import subprocess

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
    - The processing includes converting float values to integers,
      applying string transformations, removing unwanted characters,
      replacing empty strings with '0', and converting the results 
      to floats.

    """

    for Provider in Columns_Providers:
        
        # Step 1: Fill NaN values to avoid conversion issues.
        df[Provider] = df[Provider].fillna(0)
        
        # Step 2: Convert floats to integers (remove decimals).
        df[Provider] = df[Provider].apply(lambda x: int(x) if isinstance(x, float) else x)
        
        # Step 3: Apply transformations only to string values.
        df[Provider] = df[Provider].apply(
            lambda x: Stringpy.Remove_Everything_Least_Numbers(x) 
            if isinstance(x, str) else x
        )
        df[Provider] = df[Provider].apply(
            lambda x: Stringpy.Remove_Last_Character(x) 
            if isinstance(x, str) else x
        )
        
        # Step 4: Replace empty strings with "0" and convert to float.
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

def Aumentar_Nex(df: pd.DataFrame, Cantidad_Productos_A_Aumentar: int):

    """
    Simulates the repetitive process of copying data from one application
    and pasting it into another, following the logic provided in the original AutoHotkey script.

    Args:
        Cantidad_Productos_A_Aumentar (int): Number of products to update.

    """

    # Ejecutar NexAdmin.
    subprocess.Popen(['C:/Nex/NexAdmin.exe'])  # Ajusta el camino al archivo ejecutable

    # Esperar un momento para asegurarse de que el programa se abre
    time.sleep(15)

    # Pestaña de productos.
    pyautogui.click(80, 221)
    time.sleep(15)
    
    try:
        for i in range(Cantidad_Productos_A_Aumentar):
            # Obtener datos del DataFrame.
            Producto = df['Descripcion'][i]
            Precio = df['Precio_Fin'][i]
            Costo = df['Costo_Fin'][i]

            # Navegar a la sección de búsqueda.
            time.sleep(1)
            pyautogui.click(577, 371)
            time.sleep(1)
            pyautogui.press('tab', presses=4, interval=0.2)
            time.sleep(1)

            # Pegar el nombre del producto.
            pyautogui.typewrite(str(Producto))  # Escribir el nombre del producto.
            time.sleep(1.5)
            pyautogui.click(486, 314)
            time.sleep(0.2)
            pyautogui.press('enter')
            time.sleep(0.2)

            # Navegar a la sección del precio.
            pyautogui.press('tab', presses=8, interval=0.2)
            time.sleep(0.5)
            pyautogui.press('space')
            time.sleep(0.5)

            # Borrar contenido anterior y pegar el precio.
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(str(Precio))  # Escribir el precio del producto.
            time.sleep(0.5)

            # Navegar a la sección del costo.
            pyautogui.press('tab', presses=3, interval=0.2)
            time.sleep(0.5)

            # Borrar contenido anterior y pegar el costo.
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(str(Costo))  
            time.sleep(0.5)

            # Confirmar cambios.
            pyautogui.press('f2')
            time.sleep(0.5)
            pyautogui.press('space')
            time.sleep(0.5)
            pyautogui.click(486, 314)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("El script fue interrumpido manualmente.")
