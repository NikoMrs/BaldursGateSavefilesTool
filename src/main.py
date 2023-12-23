from typing import Union

import psutil

import json

from google_lib import service_setup, upload_file

import requests

def load_config() -> dict:

    file = open("config/config.json")
    data = json.load(file)

    return data

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


# Gestire metadati ??
def upload_savefile2():

    print("Uploaded")


def upload_savefile(folder_id: str, file_path: str):

    service = service_setup()
    upload_file(service, folder_id, file_path)

    print("Uploaded")



def main():

    # Lista processi --> Baldur running? --> Si: End
    #                                    --> No: Carico su drive

    config_data = load_config()

    processes = get_process_list()
    if(is_baldur_running(processes)):
        print("Baldur's Gate is running")
        return
    else:
        print("Baldur's Gate is closed. Uploading savefiles.")
        upload_savefile(config_data['drive_savefile_path'], config_data['local_savefile_path'])


main()