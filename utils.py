# -*- coding:utf-8 -*-
# Created by yanlei on 16-8-18 at 上午11:02.
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S'
                    )

log = logging

image_type = ['.jpg', 'png', 'jpeg']


def check_is_image_url(image_url):
    """
    check url is a right image url
    :param image_url:
    :return:
    """
    image_name = os.path.split(image_url)[-1]
    for img_type in image_type:
        image_name_ = image_name.lower()
        if image_name_.endswith(img_type):
            return True
    else:
        return False


if __name__ == "__main__":
    url = 'https://upload.wikimedia.org/wikipedia/commons/4/40/Showy_Primrose.JPEG'
    print check_is_image_url(url)
    logging.info("checked")
