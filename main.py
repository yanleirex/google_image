# -*- coding:utf-8 -*-
# Created by yanlei on 16-8-18 at 上午9:25.
import lxml
import lxml.html
import re

import requests

sess = requests.Session()

params = {
    'newwindow': '1',
    'hl': 'zh-CN',
    'site': 'imghp',
    'tbm': 'isch',
    'source': 'hp',
    'biw': '1855',
    'bih': '568',
    'q': 'pink+primrose',
    'oq': 'pink+primrose',
    'gs_l': 'img.12..0i19k1l3j0i30i19k1j0i8i30i19k1l3j0i5i30i19k1l2j0i8i30i19k1.28649.28649.0.35298.1.1.0.0.'
            '0.0.95.95.1.1.0....0...1ac.1.64.img..0.1.94.qBJzYeL01xA'
}

params_ = {
    'ei': 'AA61V4WOKsnk0gTyt4DIAg',
    'hl': 'zh-CN',
    'yv': '2',
    'q': 'pink+primrose',
    'start': '200',
    'asearch': 'ichunk',
    'newwindow': '1',
    'tbm': 'isch',
    'vet': '10ahUKEwiFjqjn5snOAhVJspQKHfIbACkQuT0IHygB.AA61V4WOKsnk0gTyt4DIAg.i',
    'ved': '0ahUKEwiFjqjn5snOAhVJspQKHfIbACkQuT0IHygB',
    'ijn': '2'
}

headers = {
    'Host': 'letsgg.tk',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://letsgg.tk/',
    'Cookie': 'GZ=Z=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

url = 'https://letsgg.tk/search'

sess.headers = headers
eid = None
vet = None
ved = None

response = sess.get(url, params=params)
if response.status_code == 200:
    # print response.content
    image_urls = re.findall('"ou":"(.*?)","ow"', response.content)
    doc = lxml.html.fromstring(response.content)
    eid = doc.xpath('//div[@id="rso"]/@eid')[0]
    ved = doc.xpath('//div[@id="rg"]/@data-ved')
    params_['ei'] = eid
    params_['ved'] = ved[0]
    vet = '1' + ved[0] + '.' + eid + '.i'
    params_['vet'] = vet

results = set()


def read_key_words(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def search():
    key_words = read_key_words('labels.txt')
    for key_word in key_words:
        for page in range(1, 10):
            print "Parsing page: {}".format(page)
            url_2 = 'https://letsgg.tk/search?async=_id:rg_s,_pms:s&ei=%s&hl=zh-CN&yv=%s&q=%s&start=%s&asearch=' \
                'ichunk&newwindow=1&tbm=isch&vet=%s&ved=%s&ijn=%s' % (eid, str(page), key_word, str(page*100),
                                                                      vet, ved, str(page))
            resp = sess.get(url_2)
            if resp.status_code == 200:
                result = resp.json()
                urls = re.findall('"ou":"(.*?)","ow"', result[1][1])
                for url_ in urls:
                    print url_
                    results.add(url_)


if __name__ == "__main__":
    search()
    with open('result1.txt', 'a') as f:
        for url in results:
            f.write(url + '\n')
    print "Done"
