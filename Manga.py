import datetime
import json
import os
import shutil 

import bs4
import requests
from PIL import Image

ABS_REPO_PATH = '/Users/newdev/Hive/Development/personal_projects/manga-downloader' # can get this programatically instead
REPLACE_CH_NUM = '<CH_NUM>'

class Manga:

    def __init__(self, name, ch_num, url_template, html_selector):
        self.name = name
        self.ch_num = ch_num
        self.url_template = url_template
        self.html_selector = html_selector
    
    def get_chapter_url(self, ch_num=None):
        chapter = ch_num or self.ch_num
        if chapter is None: raise("Chapter number is None!")

        return self.url_template.replace(REPLACE_CH_NUM, str(chapter))

    def download_chapter_into_pdf(self, ch_num=None):
        """
            1. downloads webpage
            2. parses HTML for images
            3. downloads images
            4. combines into a pdf
            5. deletes image downloads
        """
        chapter = ch_num or self.ch_num
        if chapter is None: raise("Chapter number is None!")

        # Download webpage HTML
        res = requests.get(self.get_chapter_url(chapter))
        res.raise_for_status()  # Error handling?

        # Parse HTML for images and their source attributes
        html_parser = bs4.BeautifulSoup(res.text, "html.parser")
        img_tags = html_parser.select(
            self.html_selector
        )  # will need to keep this updated w site format
        img_urls = [img_tag.attrs["src"] for img_tag in img_tags]

        # Download images
        img_list = []
        img_filename_list = []
        for i, img_url in enumerate(img_urls):
            # strip any newline special characters that might mess up request
            img_url = img_url.strip()

            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(img_url, stream=True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with wb ( write binary ) permission.
                filename = f"{ABS_REPO_PATH}/{self.name}_{chapter}_img_{i}"
                img_filename_list.append(filename)
                with open(filename, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

                # fails to combine into PDF in 'RGBa' mode
                img_list.append(Image.open(filename).convert('RGB'))
            else:
                error_msg = f"Image {i} Couldn't be retreived\nfailed for unexpected status code = {r.status_code}\n"
                if i == 0:
                    error_msg += "Failed on first image. Assuming manga didn't come out, not incrementing manga number\n"
                print(error_msg)
                break

        # Combine images into PDF
        final_pdf_name = None
        if len(img_urls) == len(
            img_list
        ):  # create pdf if we downloaded as many images as we expected
            final_pdf_name = f"{ABS_REPO_PATH}/{self.name}_{chapter}.pdf"
            im1 = img_list[0]
            im1.save(
                final_pdf_name,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=img_list[1:],
            )
            print(f"Successfully downloaded {final_pdf_name}")

        # Clean up image downloads
        for img in img_filename_list:
            os.remove(img)

        return final_pdf_name


"""
main pseudo

mangas = load config (array of dicts)

for manga in mangas:
    manga_obj = Manga(**manga)
    manga_obj.download_chapter_into_pdf
    mangas[i][ch_num] += 1

mangas = dump config

"""