# manga-downloader

## goal
- every week automatically download the latest chapter of one piece then upload it to my kobo

## currently working
1. launchctl (macOs version of cron jobs) to run the manga-downloader-v2.py script on the 5th minute of
    every hour
2. PIL to combine images into a PDF
3. beautifulsoup to parse through HTML of webpage to find all images with a given class attr (have
to find this for every manga I'm trying to download)

## steps
1. given a url for first image, download all images for chapter
2. combine images into a pdf named onepiece-chapter-{}.pdf
3. figure out the image url on its own
4. cron job to do this weekly
5. using json file to store mangas to downloads, and the most recent chapter


## TODOs
- always clean up image files on every execution (failure/success)
- sometimes image will download for the next chapter saying  ("manga isn't out yet"). in which case do a check to see num images of chapter is > 5 (arbitrary number)
- add more mangas to json


## cron
cp manga-downloader-cron.plist to /Users/newdev/Library/LaunchAgents/

launchctl unload /Users/newdev/Library/LaunchAgents/manga-downloader-cron.plist
launchctl load /Users/newdev/Library/LaunchAgents/manga-downloader-cron.plist
