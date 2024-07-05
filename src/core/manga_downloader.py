
import datetime
import json
import traceback

from models.Manga import Manga
from constants import ABS_REPO_PATH

MANGAS_CONFIG = f"{ABS_REPO_PATH}/configs/mangas.json"

# folder ids are in the URL
# G_DRIVE_FOLDER_ID = "1jLJ69cn5FcEshFg-uk3kYdwq9-c_QAeZ"  # ID to mangas folder
ONE_PIECE_FOLDER_ID = "1qrHhGErUjHzhyVUsLelz11Z_88-XpmCL"

"""
Download, upload to google drive, send sms with links to drive

LaunchCTL cron runs this script on the 5th minute of every hours as long
as this computer is on. It will catch up on runs if the computer was off.

Google Drive API is used to upload the completed PDF to Google Drive.

Twilio is used to send myself an SMS with the link to the PDF on Google Drive.

Increments the manga chapter number in the config file if the download was successful.
""" 
def download_all_configured_mangas():

    # Get mangas to download from config json
    manga_download_json = None
    with open(MANGAS_CONFIG) as f:
        manga_download_json = json.load(f)["mangas"]

    for i, manga_data in enumerate(manga_download_json):
        try:
            _download_and_send_manga(manga_data)

            # Incrementing this value essentially indicates the operations as a success.
            #   Because the script will only be trying to download the next manga in future executions.
            manga_download_json[i]["ch_num"] += 1

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
        json.dump({"mangas": manga_download_json}, f)


"""
{
    "name": "one_piece",
    "url_template": "https://ww8.readonepiece.com/chapter/one-piece-chapter-<CH_NUM>/",
    "ch_num": 1105,
    "html_selector": "img",
    "phone_numbers": ["16475233013"]
}
"""
def _download_and_send_manga(manga_download_data):
    manga_obj = Manga(**manga_download_data)
    pdf_path = manga_obj.download_chapter_into_pdf()

    # upload to gdrive
    # file_data = upload_file_to_drive(
    #     drive_file_name=pdf_path.split("/")[-1],
    #     file_path=pdf_path,
    #     parents=[manga_download_data["g_drive_folder_id"]],
    # )

    # OUT OF FUNDS - Might just leave this out
    # send sms with gdrive links
    # sms_body = f"New download: {file_data['name']}\nView Online: {file_data['webViewLink']}\n Download Manga: {file_data['webContentLink']}"
    # for phone_number in manga_download_data["phone_numbers"]:
    #     send_sms(message_body=sms_body, recipient_phone_num=phone_number)