## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally

## Set up the image URL and filename
image_num = 0
# how do we dynamically get this url?
# image_url = "https://cdn.readdetectiveconan.com/file/mangap/2/11002000/1.jpeg"
# image_url = "https://cdn.pixabay.com/photo/2020/02/06/09/39/summer-4823612_960_720.jpg"

another_image = True
while(another_image):
    # update image url number for next image
    image_num += 1
    image_url = f"https://cdn.readdetectiveconan.com/file/mangap/2/11002000/{image_num}.jpeg"
    print(image_url)

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        filename = image_url.split("/")[-1]
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

        # lets assume file download only fails bc we increased the image number and they url didn't exist
        #   on second thought a v2 would be to check the return status and fail accordingly
        #   404 - page doesn't exist = last image
        #   anything else is unexpected failure = investigate
        another_image = False

