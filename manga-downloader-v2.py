## Importing Necessary Modules
import json
import os
import shutil  # to save it locally

import bs4
import requests  # to get image from the web
from PIL import Image



# Get chapter number from logs
chapter_num = None
with open('logs.json') as f:
    chapter_num = json.load(f).get('chapter_num')

# Download webpage HTML
MANGA_URL = f'https://ww8.readonepiece.com/chapter/one-piece-chapter-{chapter_num}/'
res = requests.get(MANGA_URL)
    # Error handling?

# Parse HTML for images and their source attributes
html_parser = bs4.BeautifulSoup(res.text, 'html.parser')
image_tags = html_parser.select('img.js-page') # will need to keep this updated w site format
image_urls = [
    image_tag.attrs['src'] for 
    image_tag in image_tags
]
# import wdb; wdb.set_trace()

# Download images
img_list = []
img_filename_list = []
for i, image_url in enumerate(image_urls):
    # strip any newline special characters that might mess up request
    image_url = image_url.strip()

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        filename = image_url.split("/")[-1]
        img_filename_list.append(filename)
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)

        img_list.append(Image.open(filename))

        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')
        if i == 0:
            print("Failed on first image. Assuming manga didn't come out, not incrementing manga number")
            exit()

# Combine images into PDF 
final_pdf_name = f"onepiece_chapter_{chapter_num}.pdf"
im1 = img_list[0]
im1.save(final_pdf_name, "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:])

with open('logs.json', 'w') as f:
    json.dump({'chapter_num': int(chapter_num) + 1}, f)

# Clean up image downloads
for img in img_filename_list:
    os.remove(img)