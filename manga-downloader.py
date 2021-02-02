## Importing Necessary Modules
from PIL import Image
import json
import os
import requests # to get image from the web
import shutil # to save it locally


## Set up the image URL and filename
image_num = 0
chapter_num = None
with open('logs.json') as f:
    chapter_num = json.load(f).get('last_chapter')

another_image = True
img_list = []
img_filename_list = []
while(another_image):
    # update image url number for next image
    image_num += 1
    image_url = f"https://cdn.readdetectiveconan.com/file/mangap/2/1{chapter_num}000/{image_num}.jpeg"
    print(image_url)

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
        if image_num == 1:
            print("Failed on first image. Assuming manga didn't come out, not incrementing manga number")
            exit()

        # lets assume file download only fails bc we increased the image number and they url didn't exist
        #   on second thought a v2 would be to check the return status and fail accordingly
        #   404 - page doesn't exist = last image
        #   anything else is unexpected failure = investigate
        another_image = False

final_pdf_name = f"onepiece_chapter_{chapter_num}.pdf"
im1 = img_list[0]
im1.save(final_pdf_name, "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:])

with open('logs.json', 'w') as f:
    json.dump({'last_chapter': int(chapter_num) + 1}, f)

# clean up image downloads
for img in img_filename_list:
    os.remove(img)

