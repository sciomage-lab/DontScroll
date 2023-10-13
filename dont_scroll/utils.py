import datetime
import os
import random
import string
from typing import Union

import numpy
import requests
from PIL import Image


def read_image_from_url(url, token):
    response = requests.get(
        url, headers={"Authorization": f"Bearer {token}"}, stream=True
    )
    if response.status_code == 200:
        img = Image.open(response.raw)
        return numpy.asarray(img)
    else:
        return None


def set_timescope(
    start_year,
    start_month,
    start_day,
    start_hour,
    start_minute,
    start_second,
    add_day,
    add_hour,
    add_minute,
    add_second,
):
    """
    :return: unix timestamp. ex) 1695970406.104439
    """
    start_date = datetime.datetime(
        start_year, start_month, start_day, start_hour, start_minute, start_second
    )
    datetime_scope = datetime.timedelta(
        days=add_day, hours=add_hour, minutes=add_minute, seconds=add_second
    )

    return int(start_date.timestamp()), int((start_date + datetime_scope).timestamp())


def generate_random_hash(length=16):
    letters_and_digits = string.ascii_letters + string.digits
    random_hash = "".join(random.choice(letters_and_digits) for i in range(length))
    return random_hash


def is_image_file(filepath):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
    _, ext = os.path.splitext(filepath)
    return ext.lower() in image_extensions


def timestamp_to_str(timestamp: str):
    timestamp = float(timestamp)

    # 정수부와 소수부 분리
    int_part, frac_part = divmod(timestamp, 1)

    # 정수부를 datetime 객체로 변환
    dt_object = datetime.datetime.fromtimestamp(int_part)

    # datetime 객체를 문자열로 변환
    dt_string = dt_object.strftime("%Y-%m-%d %H-%M-%S")

    return dt_string


def unix_timestamp_to_datetime(unix_timestamp: Union[int, float]) -> datetime.datetime:
    ret_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
    return ret_datetime


def remove_special_chars_and_spaces(s: str) -> str:
    # 문자열 앞부분에서 특수문자와 공백을 제거
    for i, char in enumerate(s):
        if char.isalnum():
            return s[i:]
    return ""


if __name__ == "__main__":
    import sys

    img_npy = read_image_from_url(sys.argv[0], token=sys.argv[1])
    print(img_npy.shape)
