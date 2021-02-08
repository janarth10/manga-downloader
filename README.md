# manga-downloader

## goal
- every week automatically download the latest chapter of one piece then upload it to my kobo

## steps
1. given a url for first image, download all images for chapter
2. combine images into a pdf named onepiece-chapter-{}.pdf
3. figure out the url on its own
4. cron job to do this weekly


## TODOs
- always clean up image files on every execution (failure/success)
- do I need the chapter_num to defined in logs.json for first iteration?