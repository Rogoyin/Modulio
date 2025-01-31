from typing import Optional
import os

def Obtener_Backup_Mas_Reciente(Directorio: str) -> Optional[str]:

    """
    Obtiene el archivo más reciente en un directorio basándose en la 
    fecha de modificación.

    Esta función examina todos los archivos en el directorio 
    especificado y determina cuál fue modificado más recientemente.

    Parámetros:
    -----------
    Directorio : str
        La ruta al directorio.

    Retorna:
    --------
    Optional[str]
        La ruta al archivo más reciente o None si no se encuentran 
        archivos.

    Ejemplo:
    --------
    >>> Backup = Obtener_Backup_Mas_Reciente('/ruta/al/directorio')
    >>> print(Backup)
    '/ruta/al/directorio/archivo_reciente.txt'

    """

    # Lista todos los archivos en el directorio.
    Archivos = [
        os.path.join(Directorio, Archivo) 
        for Archivo in os.listdir(Directorio) 
        if os.path.isfile(os.path.join(Directorio, Archivo))
    ]
    
    # Verifica si el directorio está vacío.
    if not Archivos:
        return None
    
    # Obtiene el archivo más reciente por fecha de modificación.
    Backup_Mas_Reciente = max(Archivos, key = os.path.getmtime)
    
    return Backup_Mas_Reciente