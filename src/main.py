from typing import Union

import psutil

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import requests

def get_process_list() -> list[dict[str, Union[str, int]]]:

    processes = []
    for p in psutil.process_iter(['pid', 'name']):
        processes.append(p.info)

    #print(processes)
    return processes
    

def is_baldur_running(processes: list[dict[str, Union[str, int]]]) -> bool:

    if("chromae.exe" in (p['name'] for p in processes)):
        return True
    else:
        return False


def upload_savefile2():

    credentials = ""

    try:
        service = build("drive", "v3", credentials=credentials)

    except HttpError as errorLog:
        print("Error: " + errorLog)

    print("Uploaded")


def upload_savefile():

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"

    print("Uploaded")



def main():

    # Lista processi --> Baldur running? --> Si: End
    #                                    --> No: Carico su drive
    
    processes = get_process_list()
    if(is_baldur_running(processes)):
        print("Baldur's Gate is running")
        return
    else:
        print("Baldur's Gate is closed. Uploading savefiles.")
        upload_savefile()

main()