
import os
import google.oauth2.credentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.http import MediaFileUpload
from email.mime.base import MIMEBase
from email import encoders

def Authenticate_Gmail_And_Drive() -> tuple:

    """
    Authenticates and creates service objects to interact with both the Gmail and Google Drive APIs.

    This function authenticates the user and creates service objects for both the Gmail and Google Drive APIs. It checks if valid credentials exist and, if not, runs the OAuth flow to authenticate the user.

    Example usage:
        gmail_service, drive_service = Authenticate_Gmail_And_Drive()

    Returns:
        tuple: The Gmail API service object and the Google Drive API service object.

    Raises:
        FileNotFoundError: If the 'credentials.json' file is not found.
        ValueError: If the token is invalid or cannot be refreshed.

    """
    
    # Define the required scopes for Gmail and Google Drive.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/drive.file']
    
    Creds = None
    
    # Check if token.json exists and is valid.
    if os.path.exists('A:/Descargas/token.json'):
        Creds = google.oauth2.credentials.Credentials.from_authorized_user_file('A:/Descargas/token.json', SCOPES)

    # If no credentials are available or are invalid, initiate login.
    if not Creds or not Creds.valid:
        if Creds and Creds.expired and Creds.refresh_token:
            Creds.refresh(Request())
        else:
            Flow = InstalledAppFlow.from_client_secrets_file(
                'A:/Descargas/credentials.json', SCOPES)  # Replace with the correct path
            Creds = Flow.run_local_server(port=0)

        # Save the credentials for the next time the script is run.
        with open('A:/Descargas/token.json', 'w') as Token:
            Token.write(Creds.to_json())

    # Build both Gmail and Drive services with the authenticated credentials.
    Gmail_Service = build('gmail', 'v1', credentials=Creds, cache_discovery=False)
    Drive_Service = build('drive', 'v3', credentials=Creds, cache_discovery=False)

    return Gmail_Service, Drive_Service

def Send_Email(Gmail_Service: 'googleapiclient.discovery.Resource', Drive_Service: 'googleapiclient.discovery.Resource', # type: ignore
               Sender: str, To: str, Subject: str, Body: str, File_Paths: list = []) -> None:
   
    """
    Sends an email using the Gmail API, with multiple optional attachments.

    This function sends an email through the Gmail API, optionally including file attachments. If the files exceed 25 MB, they are uploaded to Google Drive and the links are included in the email body.

    Example usage:
        Send_Email(gmail_service, drive_service, 'sender@example.com', 'recipient@example.com', 'Subject', 'Body', ['file1.txt', 'file2.txt'])

    Args:
        Gmail_Service (googleapiclient.discovery.Resource): The Gmail API service object.
        Drive_Service (googleapiclient.discovery.Resource): The Google Drive API service object.
        Sender (str): The email address of the sender.
        To (str): The email address of the recipient.
        Subject (str): The subject of the email.
        Body (str): The body content of the email.
        File_Paths (list, optional): A list of file paths to be attached. Default is an empty list.

    Raises:
        HttpError: If an error occurs while sending the email.

    """

    try:
        # Create the email message.
        Message = MIMEMultipart()
        Message['to'] = To
        Message['subject'] = Subject
        Msg = MIMEText(Body)
        Message.attach(Msg)

        # List to store Google Drive links for large files.
        Large_File_Links = []

        # Attach files or upload large files to Drive.
        if len(File_Paths) > 0:
            for File_Path in File_Paths:
                File_Size = os.path.getsize(File_Path)
                
                if File_Size > 25 * 1024 * 1024:  # File size exceeds 25 MB.
                    print(f"File '{os.path.basename(File_Path)}' exceeds 25 MB. Uploading to Google Drive...")
                    
                    # Upload file to Google Drive.
                    File_Metadata = {'name': os.path.basename(File_Path)}
                    Media = MediaFileUpload(File_Path, mimetype='application/octet-stream', resumable=True)
                    Uploaded_File = Drive_Service.files().create(body=File_Metadata, media_body=Media, fields='id, webViewLink').execute()

                    # Get the link and add it to the email body.
                    File_Link = Uploaded_File.get('webViewLink')
                    Large_File_Links.append(f"{os.path.basename(File_Path)}: {File_Link}")
                else:
                    # Attach files smaller than 25 MB.
                    with open(File_Path, 'rb') as Attachment:
                        Part = MIMEBase('application', 'octet-stream')
                        Part.set_payload(Attachment.read())
                        encoders.encode_base64(Part)
                        Part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(File_Path)}')
                        Message.attach(Part)

        # Add links for large files to the email body.
        if Large_File_Links:
            Body += "\n\nLinks to large files:\n" + "\n".join(Large_File_Links)
            Message.attach(MIMEText(Body, 'plain'))

        # Convert the message to raw format.
        Raw_Message = base64.urlsafe_b64encode(Message.as_bytes()).decode('utf-8')

        # Send the message.
        Send_Message = Gmail_Service.users().messages().send(userId="me", body={'raw': Raw_Message}, timeout=60).execute()
        print(f'Message sent: {Send_Message["id"]}')
    
    except Exception as Error:
        print(f'An error occurred: {Error}')



