# -*- coding:utf-8 -*-
# Created by yanlei on 16-8-18 at 上午11:27.
import re
import types

import lxml
import lxml.html

from download import HtmlDownloader
from utils import log
from main import headers


class Parser(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def convert_content_to_html(content):
        try:
            if isinstance(content, types.StringType):
                document = lxml.html.fromstring(content)
                return document
        except TypeError as e:
            log.error(e)

    @staticmethod
    def re_find_all(pattern, content):
        try:
            if isinstance(content, types.StringType):
                result = re.findall(pattern=pattern, string=content)
                return result
        except TypeError as e:
            log.error(e)

    @staticmethod
    def xpath_find(xpath, document):
        result = document.xpath(xpath)
        if result:
            return result[0]
        else:
            return None


class GoogleImageParser(Parser):
    def __init__(self, name):
        self.name = name
        super(GoogleImageParser, self).__init__(name=self.name)
        self.base_url = 'https://letsgg.tk/search'
        self.params = {
            'newwindow': '1',
            'hl': 'zh-CN',
            'site': 'imghp',
            'tbm': 'isch',
            'source': 'hp',
            'biw': '1855',
            'bih': '568',
            'oq': 'pink+primrose',
            'gs_l': 'img.12..0i19k1l3j0i30i19k1j0i8i30i19k1l3j0i5i30i19k1l2j0i8i30i19k1.28649.28649.0.35298.1.1.0.0.'
                    '0.0.95.95.1.1.0....0...1ac.1.64.img..0.1.94.qBJzYeL01xA'
            }
        self.downloader = HtmlDownloader()
        self.downloader.headers = headers

    def parse_parameter(self, content):
        document = self.convert_content_to_html(content)
        eid = self.xpath_find('//div[@id="rso"]/@eid', document)
        ved = self.xpath_find('//div[@id="rg"]/@data-ved', document)
        vet = '1' + ved + '.' + eid + '.i'
        return {'eid': eid, 'ved': ved, 'vet': vet}

    def parse_first_page(self, content):
        parameter = self.parse_parameter(content)
        image_urls = self.re_find_all('"ou":"(.*?)","ow"', content)

    def build_search_url(self, key_word):
        self.params['q'] = key_word
        return self.downloader.download_html(self.base_url, params=self.params, method='get')


if __name__ == "__main__":
    parser = GoogleImageParser('google')
    response = parser.build_search_url('pink+primrose')
    content = response.content
    parser.parse_first_page(content)
