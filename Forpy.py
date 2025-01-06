'''
--OPERACIONES EXCLUSIVAS DEL PROGRAMA DEL FORRAJE--
'''

import Stringpy
from typing import List
import pandas as pd # type: ignore
import time
import pyautogui # type: ignore
import pygetwindow as gw # type: ignore
import subprocess
import pyperclip # type: ignore

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
    pyautogui.click(80, 230)
    time.sleep(15)
    
    Productos = list(df['Descripcion'])

    try:
        for i in range(Cantidad_Productos_A_Aumentar):
            # Obtener datos del DataFrame.
            Producto = Productos[i]
            Precio = df['Precio_Fin'][i]
            Costo = df['Costo_Fin'][i]

            # Navegar a la sección de búsqueda.
            time.sleep(1)
            pyautogui.click(577, 371)
            time.sleep(1)
            pyautogui.press('tab', presses=4, interval=0.5)
            time.sleep(1)

            # Pegar el nombre del producto.
            # Copiar el producto al portapapeles.
            pyperclip.copy(Producto)
    
            # Esperar un poco antes de pegar.
            time.sleep(1)
            
            # Pegar el texto del portapapeles.
            pyautogui.hotkey('ctrl', 'v')  
            pyautogui.press('enter')  
            time.sleep(1.5)
            pyautogui.click(486, 314)
            time.sleep(0.2)
            pyautogui.press('enter')
            time.sleep(0.2)

            # Navegar a la sección del precio.
            pyautogui.press('tab', presses=9, interval=0.5)
            time.sleep(0.5)
            pyautogui.press('space')
            time.sleep(0.5)

            # Borrar contenido anterior y pegar el precio.
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(str(Precio))  # Escribir el precio del producto.
            time.sleep(0.5)

            # Navegar a la sección del costo.
            pyautogui.press('tab', presses=3, interval=0.5)
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

def Cambiar_Descripcion_Nex(df: pd.DataFrame, Cantidad_Productos_A_Cambiar: int):

    """
    This function automates the process of changing the description of products 
    in the NexAdmin software. It opens NexAdmin, navigates through its interface, 
    and modifies product descriptions based on a given DataFrame containing the 
    old and new descriptions.

    Args:
        df (pd.DataFrame): A DataFrame with two columns: 'Descripcion' (old 
                            product descriptions) and 'Editado' (new product 
                            descriptions). The function will loop through the rows 
                            and update the descriptions of the products in NexAdmin.
        Cantidad_Productos_A_Cambiar (int): The number of products to change. 
                                            This controls how many rows in the 
                                            DataFrame are processed.

    Returns:
        None: The function does not return any value. It modifies the product 
            descriptions directly in the NexAdmin software.

    Example:
        # Sample DataFrame containing old and new product descriptions
        data = {
            'Descripcion': ['Old Description 1', 'Old Description 2'],
            'Editado': ['New Description 1', 'New Description 2']
        }
        df = pd.DataFrame(data)

        # Call the function to change descriptions for 2 products
        Cambiar_Descripcion_Nex(df, 2)

    Notes:
        - Ensure that NexAdmin is installed at the specified path 
        ('C:/Nex/NexAdmin.exe').
        - The function uses `pyautogui` and `pyperclip` for automating GUI 
        interactions and copying text.
        - The script pauses for specific time intervals (`time.sleep`) to allow 
        for transitions between steps.
        - The function assumes that the layout and screen coordinates of NexAdmin 
        are fixed.
        - Keyboard shortcuts and mouse clicks are automated to simulate human-like 
        interactions with the software.
        - The function will be interrupted if the user presses Ctrl+C during 
        execution.

    """

    # Ejecutar NexAdmin.
    subprocess.Popen(['C:/Nex/NexAdmin.exe'])  # Ajusta el camino al archivo ejecutable

    # Esperar un momento para asegurarse de que el programa se abre
    time.sleep(15)

    # Pestaña de productos.
    pyautogui.click(80, 230)
    time.sleep(15)
    
    Nombres_Viejos = list(df['Descripcion'])
    Nombres_Nuevos = list(df['Editada'])

    try:
        for i in range(Cantidad_Productos_A_Cambiar):

            # Obtener datos del DataFrame.
            Nombre_Viejo = Nombres_Viejos[i]
            Nombre_Nuevo = Nombres_Nuevos[i]

            # Navegar a la sección de búsqueda.
            time.sleep(1)
            pyautogui.click(577, 371)
            time.sleep(1)
            pyautogui.press('tab', presses=4, interval=0.5)
            time.sleep(1)

            # Pegar el nombre del producto.
            # Copiar el producto al portapapeles.
            pyperclip.copy(Nombre_Viejo)
    
            # Esperar un poco antes de pegar.
            time.sleep(1)
            
            # Pegar el texto del portapapeles.
            pyautogui.hotkey('ctrl', 'v')  
            pyautogui.press('enter')  
            time.sleep(1.5)
            pyautogui.click(486, 314)
            time.sleep(0.2)
            pyautogui.press('enter')
            time.sleep(0.2)

            # Navegar a la sección del nombre.
            pyautogui.press('tab', presses=4, interval=0.5)
            time.sleep(0.5)

            # Borrar contenido anterior y pegar el nombre nuevo.
            pyautogui.press('delete')
            time.sleep(0.5)
            pyautogui.typewrite(str(Nombre_Nuevo))  # Escribir la descripción nueva del producto.
            time.sleep(0.5)

            # Navegar a la sección del costo.
            pyautogui.press('tab', presses=3, interval=0.5)
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
