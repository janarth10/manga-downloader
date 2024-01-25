## Importing Necessary Modules
import datetime

from core.manga_downloader import download_all_configured_mangas

# printing datetime for debugging purposes. to see if the cron job is running
# %c format gives human readable string
print(f"Last ran { datetime.datetime.now().strftime('%c') }")

"""
 File run by the recurring cron.

 LaunchCTL cron runs this script on the 5th minute of every hours as long
 as this computer is on. It will catch up on runs if the computer was off.
"""
download_all_configured_mangas()
