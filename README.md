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
3. figure out the url on its own
4. cron job to do this weekly


## TODOs
- always clean up image files on every execution (failure/success)
- do I need the chapter_num to defined in logs.json for first iteration?
