import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.appdata", "https://www.googleapis.com/auth/drive.file"]

API_NAME = "drive"
API_VERSION = "v3"
CREDENTIALS_FILE_PATH = "config/credentials.json"


def service_setup():
    credentials = None

    if os.path.exists("config/token.json"):
        credentials = Credentials.from_authorized_user_file("config/token.json", SCOPES)

    # If there are no valid credentaials, log in
    if((credentials is None) or (not credentials.valid)):

        try:

            if((credentials is not None) and (credentials.expired) and (credentials.refresh_token)):
                credentials.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE_PATH, SCOPES)
                credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("config/token.json", "w") as token:
                token.write(credentials.to_json())

        except Exception as error:
            print("Error during authorization phase")
            print(error)

            if("(access_denied)" in str(error)):
                print("Please, grant the application all the required permission")
                return

    try:

        service = build("drive", "v3", credentials=credentials)
        print("Service created")
        return service


    except HttpError as error:

        print("Error during service creation")
        print(error)


def upload_file(service, folder_id: str, file_path: str):

    print(folder_id)

    file_name = "test.txt"
    file_mimetype = "text/plain"
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }

    media = MediaFileUpload(file_path, file_mimetype)
    service.files().create(
        body = file_metadata,
        media_body = media,
        fields = "id"
    ).execute()

    return