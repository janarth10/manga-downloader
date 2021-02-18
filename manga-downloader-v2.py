## Importing Necessary Modules
import datetime
import json

from g_drive_helper import upload_file_to_drive
from Manga import Manga
from sms import send_sms

# printing datetime for debugging purposes. to see if the cron job is running
# %c format gives human readable string
print(f"Last ran { datetime.datetime.now().strftime('%c') }")

ABS_REPO_PATH = '/Users/newdev/Hive/Development/personal_projects/manga-downloader'
MANGAS_CONFIG = f'{ABS_REPO_PATH}/configs/mangas.json'
G_DRIVE_FOLDER_ID = '1jLJ69cn5FcEshFg-uk3kYdwq9-c_QAeZ' # ID to mangas folder

# Get mangas to download from json
mangas = None
with open(MANGAS_CONFIG) as f:
    mangas = json.load(f)['mangas']

# download, upload to google drive, send sms with links to drive
for i, manga_data in enumerate(mangas):
    try:
        import wdb; wdb.set_trace()
        manga_obj = Manga(**manga_data)
        pdf_path = manga_obj.download_chapter_into_pdf()
        mangas[i]['ch_num'] += 1

        # upload to gdrive
        file_data = upload_file_to_drive(
            drive_file_name=pdf_path.split('/')[-1],
            file_path=pdf_path,
            parents=[G_DRIVE_FOLDER_ID]
        )

        # send sms with gdrive links
        sms_body = f"New download: {file_data['name']}\nView Online: {file_data['webViewLink']}\n Download Manga: {file_data['webContentLink']}"
        send_sms(message_body=sms_body, recipient_phone_num='6475233013')

    except:
        # blindly catching exceptions, don't wanna miss other mangas if one fails
        pass

# save config file with incremented chapter nums
with open(MANGAS_CONFIG, 'w') as f:
    json.dump({'mangas': mangas}, f)
