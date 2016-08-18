# -*- coding:utf-8 -*-
# Created by yanlei on 16-8-18 at 上午10:55.
import os

import requests

from utils import check_is_image_url
from utils import log


class HtmlDownloader(object):
    def __init__(self, headers=None):
        self.sess = requests.Session()
        self.headers = headers
        self.sess.headers = self.headers

    def download_html(self, url, params=None, method='get'):
        log.info("Downloading: {}".format(url))
        if method == 'get':
            return self._do_get(url=url, params=params)
        else:
            return self._do_post(url=url, params=params)

    def _do_get(self, url, params=None):
        response = self.sess.get(url=url, params=params)
        if response.status_code == 200:
            return response
        else:
            log.error("Download html failed")

    def _do_post(self, url, params):
        response = self.sess.post(url=url, params=params)
        if response.status_code:
            return response
        else:
            log.error("Download html failed")


class ImageDownloader(HtmlDownloader):
    def __init__(self, headers, path):
        super(ImageDownloader, self).__init__(headers)
        self.path = path

    def download_image(self, url):
        if check_is_image_url(url):
            log.info("Downloading image: {}".format(url))
            return self._do_get(url)

    def write_image_to_file(self, content, image_name):
        image_path = os.path.join(self.path, image_name)
        try:
            with open(image_path) as f:
                f.write(content)
            log.info("Saved image to {}".format(image_path))
        except IOError as e:
            log.error("Save image failed.\n {}".format(e))
