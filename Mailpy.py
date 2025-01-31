import os
import base64
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import google.oauth2.credentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

def Autenticar_Gmail_Y_Drive() -> tuple:

    """
    Autentica y crea objetos de servicio para interactuar con las APIs 
    de Gmail y Google Drive.

    Esta función autentica al usuario y crea objetos de servicio tanto 
    para Gmail como para Google Drive. Verifica si existen credenciales 
    válidas y, si no, ejecuta el flujo OAuth para autenticar al usuario.

    Ejemplo de uso:
    --------------
    >>> Servicio_Gmail, Servicio_Drive = Autenticar_Gmail_Y_Drive()

    Retorna:
    --------
    tuple
        El objeto de servicio de la API de Gmail y el objeto de servicio 
        de la API de Google Drive.

    Lanza:
    ------
    FileNotFoundError
        Si no se encuentra el archivo 'credentials.json'.
    ValueError
        Si el token es inválido o no puede ser actualizado.

    """
    
    # Define los ámbitos requeridos para Gmail y Google Drive.
    Ambitos = ['https://www.googleapis.com/auth/gmail.send', 
               'https://www.googleapis.com/auth/drive.file']
    
    Credenciales = None
    
    # Verifica si existe token.json y es válido.
    if os.path.exists('A:/Descargas/token.json'):
        Credenciales = google.oauth2.credentials.Credentials.\
            from_authorized_user_file('A:/Descargas/token.json', Ambitos)

    # Si no hay credenciales o son inválidas, inicia el login.
    if not Credenciales or not Credenciales.valid:
        if Credenciales and Credenciales.expired and \
            Credenciales.refresh_token:
            Credenciales.refresh(Request())
        else:
            Flujo = InstalledAppFlow.from_client_secrets_file(
                'A:/Descargas/credentials.json', Ambitos)
            Credenciales = Flujo.run_local_server(port=0)

        # Guarda las credenciales para la próxima ejecución.
        with open('A:/Descargas/token.json', 'w') as Token:
            Token.write(Credenciales.to_json())

    # Construye servicios de Gmail y Drive con las credenciales.
    Servicio_Gmail = build('gmail', 'v1', credentials=Credenciales, 
                          cache_discovery=False)
    Servicio_Drive = build('drive', 'v3', credentials=Credenciales, 
                          cache_discovery=False)

    return Servicio_Gmail, Servicio_Drive

def Enviar_Email(Servicio_Gmail: 'Resource',
    Servicio_Drive: 'Resource',
    Remitente: str, Destinatario: str, Asunto: str, Cuerpo: str, 
    Rutas_Archivos: list = []) -> None:
   
    """
    Envía un email usando la API de Gmail, con múltiples archivos 
    adjuntos opcionales.

    Esta función envía un email a través de la API de Gmail, 
    opcionalmente incluyendo archivos adjuntos. Si los archivos 
    exceden los 25 MB, se suben a Google Drive y los enlaces se 
    incluyen en el cuerpo del email.

    Ejemplo de uso:
    --------------
    >>> Enviar_Email(servicio_gmail, servicio_drive, 
            'remitente@ejemplo.com', 'destinatario@ejemplo.com', 
            'Asunto', 'Cuerpo', ['archivo1.txt', 'archivo2.txt'])

    Parámetros:
    -----------
    Servicio_Gmail : googleapiclient.discovery.Resource
        El objeto de servicio de la API de Gmail.
    
    Servicio_Drive : googleapiclient.discovery.Resource
        El objeto de servicio de la API de Google Drive.
    
    Remitente : str
        La dirección de email del remitente.
    
    Destinatario : str
        La dirección de email del destinatario.
    
    Asunto : str
        El asunto del email.
    
    Cuerpo : str
        El contenido del cuerpo del email.
    
    Rutas_Archivos : list, opcional
        Una lista de rutas de archivos para adjuntar. Por defecto es 
        una lista vacía.

    Lanza:
    ------
    HttpError
        Si ocurre un error al enviar el email.

    """

    try:
        # Crea el mensaje de email.
        Mensaje = MIMEMultipart()
        Mensaje['to'] = Destinatario
        Mensaje['subject'] = Asunto
        Mensaje_Texto = MIMEText(Cuerpo)
        Mensaje.attach(Mensaje_Texto)

        # Lista para almacenar enlaces de Google Drive para archivos grandes.
        Enlaces_Archivos_Grandes = []

        # Adjunta archivos o sube archivos grandes a Drive.
        if len(Rutas_Archivos) > 0:
            for Ruta_Archivo in Rutas_Archivos:
                Tamanio_Archivo = os.path.getsize(Ruta_Archivo)
                
                # Tamaño del archivo excede 25 MB.
                if Tamanio_Archivo > 25 * 1024 * 1024:  
                    print(
                        f"El archivo '{os.path.basename(Ruta_Archivo)}' "
                        f"excede 25 MB. Subiendo a Google Drive..."
                    )
                    
                    # Sube archivo a Google Drive.
                    Metadatos_Archivo = {
                        'name': os.path.basename(Ruta_Archivo)
                    }
                    Medio = MediaFileUpload(
                        Ruta_Archivo, 
                        mimetype = 'application/octet-stream',
                        resumable = True
                    )

                    Archivo_Subido = Servicio_Drive.files().create( # type: ignore
                                body = Metadatos_Archivo,
                                media_body = Medio,
                                fields = 'id, webViewLink'
                            ).execute()

                    # Obtiene el enlace y lo añade al cuerpo del email.
                    Enlace_Archivo = Archivo_Subido.get('webViewLink')
                    Enlaces_Archivos_Grandes.append(
                        f"{os.path.basename(Ruta_Archivo)}: "
                        f"{Enlace_Archivo}"
                    )
                else:
                    # Adjunta archivos menores de 25 MB.
                    with open(Ruta_Archivo, 'rb') as Adjunto:
                        Parte = MIMEBase('application', 'octet-stream')
                        Parte.set_payload(Adjunto.read())
                        encoders.encode_base64(Parte)
                        Parte.add_header(
                            'Content-Disposition',
                            f'attachment; filename ='
                            f'{os.path.basename(Ruta_Archivo)}'
                        )
                        Mensaje.attach(Parte)

        # Añade enlaces para archivos grandes al cuerpo del email.
        if Enlaces_Archivos_Grandes:
            Cuerpo += "\n\nEnlaces a archivos grandes:\n" + \
                "\n".join(Enlaces_Archivos_Grandes)
            Mensaje.attach(MIMEText(Cuerpo, 'plain'))

        # Convierte el mensaje a formato raw.
        Mensaje_Raw = base64.urlsafe_b64encode(
            Mensaje.as_bytes()
        ).decode('utf-8')

        # Envía el mensaje.
        Mensaje_Enviado = Servicio_Gmail.users().messages().send( # type: ignore
            userId="me",
            body={'raw': Mensaje_Raw},
            timeout=60
        ).execute()
        print(f'Mensaje enviado: {Mensaje_Enviado["id"]}')
    
    except Exception as Error:
        print(f'Ocurrió un error: {Error}')



