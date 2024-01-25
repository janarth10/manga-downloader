

import datetime
import json
import sys
import traceback

from entities.google_drive import upload_file_to_drive
from entities.sms import send_sms
from models.Manga import Manga

# TODO use sys to get the path to the repo
ABS_REPO_PATH = "/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader"
MANGAS_CONFIG = f"{ABS_REPO_PATH}/configs/mangas.json"

# folder ids are in the URL
G_DRIVE_FOLDER_ID = "1jLJ69cn5FcEshFg-uk3kYdwq9-c_QAeZ"  # ID to mangas folder
JUJUTSU_KAISEN_FOLDER_ID = "1mQ45A3XbW9l5Vehmcno5d0TCQC7T6toA"
ONE_PIECE_FOLDER_ID = "1qrHhGErUjHzhyVUsLelz11Z_88-XpmCL"

"""
Download, upload to google drive, send sms with links to drive

LaunchCTL cron runs this script on the 5th minute of every hours as long
as this computer is on. It will catch up on runs if the computer was off.

Google Drive API is used to upload the completed PDF to Google Drive.

Twilio is used to send myself an SMS with the link to the PDF on Google Drive.
""" 
def download_all_configured_mangas():
    # Get mangas to download from json
    mangas = None
    with open(MANGAS_CONFIG) as f:
        mangas = json.load(f)["mangas"]

    for i, manga_data in enumerate(mangas):
        try:
            manga_obj = Manga(**manga_data)
            pdf_path = manga_obj.download_chapter_into_pdf()

            # upload to gdrive
            file_data = upload_file_to_drive(
                drive_file_name=pdf_path.split("/")[-1],
                file_path=pdf_path,
                parents=[G_DRIVE_FOLDER_ID],
            )

            # send sms with gdrive links
            sms_body = f"New download: {file_data['name']}\nView Online: {file_data['webViewLink']}\n Download Manga: {file_data['webContentLink']}"
            for phone_number in manga_data["phone_numbers"]:
                send_sms(message_body=sms_body, recipient_phone_num=phone_number)

            # Incrementing this value essentially indicates the operations as a success.
            #   Because the script will only be trying to download the next manga in future executions.
            mangas[i]["ch_num"] += 1

        except Exception as e:
            # blindly catching exceptions, don't wanna miss other mangas if one fails
            print("------------ start: exception --------------")
            traceback.print_exc()
            print(f"Exception at { datetime.datetime.now().strftime('%c') }")
            print(e)
            print("------------ end: exception --------------")
            pass

    # save config file with incremented chapter nums
    with open(MANGAS_CONFIG, "w") as f:
        json.dump({"mangas": mangas}, f)