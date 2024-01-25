## Importing Necessary Modules
import datetime

from core.manga_downloader import download_all_configured_mangas

# printing datetime for debugging purposes. to see if the cron job is running
# %c format gives human readable string
print(f"Last ran { datetime.datetime.now().strftime('%c') }")

download_all_configured_mangas()

# Get mangas to download from json
# mangas = None
# with open(MANGAS_CONFIG) as f:
#     mangas = json.load(f)["mangas"]

# def special_script_jjk():
#     print('special_script_jjk')
#     for ch_num in range(58, 140):
#         manga_config = {
#             "name": "jujutsu_kaisen",
#             "url_template": "https://ww8.jujmanga.com/manga/jujutsu-kaisen-chapter-<CH_NUM>-2/",
#             # "url_template": "https://ww8.readonepiece.com/chapter/one-piece-chapter-<CH_NUM>/",
#             "ch_num": ch_num,
#             "html_selector": "img"
#         }
#         manga_obj = Manga(**manga_config)
#         pdf_path = manga_obj.download_chapter_into_pdf()

#         # upload to gdrive
#         file_data = upload_file_to_drive(
#             drive_file_name=pdf_path.split("/")[-1],
#             file_path=pdf_path,
#             parents=[JUJUTSU_KAISEN_FOLDER_ID],
#         )


# ### --------- special_script_woooo ---------------

# def special_script_woooo():
#     print('special_script_woooo')
#     onepiece_config = {
#         "name": "one_piece",
#         "url_template": "https://ww8.readonepiece.com/chapter/one-piece-chapter-<CH_NUM>/",
#         "ch_num": 1100,
#         "html_selector": "img.js-page"
#     }
#     manga_obj = Manga(**onepiece_config)
#     pdf_path = manga_obj.download_chapter_into_pdf()

#     # upload to gdrive
#     file_data = upload_file_to_drive(
#         drive_file_name=pdf_path.split("/")[-1],
#         file_path=pdf_path,
#         parents=[G_DRIVE_FOLDER_ID],
#     )

#     # send sms with gdrive links
#     sms_body = f"New download: {file_data['name']}\nView Online: {file_data['webViewLink']}\n Download Manga: {file_data['webContentLink']}"
#     send_sms(message_body=sms_body, recipient_phone_num="16475233013")

# ### --------- special_script_woooo ---------------

# # # special one time script
# # if len(sys.argv) == 2:
# #     special_script_woooo()

# # # Downloading a specific manga through terminal
# # elif len(sys.argv) == 3:
# #     print("arg list: ", str(sys.argv))
# #     chapter_name = str(sys.argv[1])
# #     ch_num = int(sys.argv[2])

# #     manga_data = [manga for manga in mangas if manga.get("name") == chapter_name][0]
# #     manga_data["ch_num"] = ch_num
# #     manga_obj = Manga(**manga_data)
# #     pdf_path = manga_obj.download_chapter_into_pdf()

# # # Recurring cron to send out new mangas
# # elif len(sys.argv) == 1:

# #     # download, upload to google drive, send sms with links to drive
# #     for i, manga_data in enumerate(mangas):
# #         try:
# #             manga_obj = Manga(**manga_data)
# #             pdf_path = manga_obj.download_chapter_into_pdf()

# #             # upload to gdrive
# #             file_data = upload_file_to_drive(
# #                 drive_file_name=pdf_path.split("/")[-1],
# #                 file_path=pdf_path,
# #                 parents=[G_DRIVE_FOLDER_ID],
# #             )

# #             # send sms with gdrive links
# #             sms_body = f"New download: {file_data['name']}\nView Online: {file_data['webViewLink']}\n Download Manga: {file_data['webContentLink']}"
# #             for phone_number in manga_data["phone_numbers"]:
# #                 send_sms(message_body=sms_body, recipient_phone_num=phone_number)

# #             # Incrementing this value essentially indicates the operations as a success.
# #             #   Because the script will only be trying to download the next manga in future executions.
# #             mangas[i]["ch_num"] += 1

# #         except Exception as e:
# #             # blindly catching exceptions, don't wanna miss other mangas if one fails
# #             print("------------ start: exception --------------")
# #             traceback.print_exc()
# #             print(f"Exception at { datetime.datetime.now().strftime('%c') }")
# #             print(e)
# #             print("------------ end: exception --------------")
# #             pass

# #     # save config file with incremented chapter nums
# #     with open(MANGAS_CONFIG, "w") as f:
# #         json.dump({"mangas": mangas}, f)

# # else:
# #     raise Exception("Unexpected amount of command line arguments!!")

# # special_script_woooo()
# # special_script_jjk()

