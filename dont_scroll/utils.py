import requests
from PIL import Image
import numpy
import config


def read_image_from_url(url, token):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {token}"}, stream=True
    )
    if response.status_code == 200:
        img = Image.open(response.raw)
        return numpy.asarray(img)
    else:
        return None


if __name__ == "__main__":
    import sys

    img_npy = read_image_from_url(sys.argv[0], token=sys.argv[1])
    print(img_npy.shape)
