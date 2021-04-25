## Importing Necessary Modules
import datetime
import json
import sys
import traceback

from g_drive_helper import upload_file_to_drive
from Manga import Manga
from sms import send_sms

# printing datetime for debugging purposes. to see if the cron job is running
# %c format gives human readable string
print(f"Last ran { datetime.datetime.now().strftime('%c') }")

ABS_REPO_PATH = "/Users/newdev/Hive/Development/personal_projects/manga-downloader"
MANGAS_CONFIG = f"{ABS_REPO_PATH}/configs/mangas.json"
G_DRIVE_FOLDER_ID = "1jLJ69cn5FcEshFg-uk3kYdwq9-c_QAeZ"  # ID to mangas folder

# Get mangas to download from json
mangas = None
with open(MANGAS_CONFIG) as f:
    mangas = json.load(f)["mangas"]


# Downloading a specific manga through terminal
if len(sys.argv) == 3:
    print("arg list: ", str(sys.argv))
    chapter_name = str(sys.argv[1])
    ch_num = int(sys.argv[2])

    manga_data = [manga for manga in mangas if manga.get("name") == chapter_name][0]
    manga_data["ch_num"] = ch_num
    manga_obj = Manga(**manga_data)
    pdf_path = manga_obj.download_chapter_into_pdf()


# Recurring cron to send out new mangas
elif len(sys.argv) == 1:

    # download, upload to google drive, send sms with links to drive
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

else:
    raise Exception("Unexpected amount of command line arguments!!")
