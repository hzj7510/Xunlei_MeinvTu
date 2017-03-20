# _*_coding:utf-8_*_

# from bs4 import BeautifulSoup as bs
import requests
import os
import re
import json
from multiprocessing import Pool

all_url = 'http://act.vip.xunlei.com/ugirls/js/ugirlsdata.js'
pic_url = 'http://data.meitu.xunlei.com/data/image/'
pic_path = '/Users/mac/Desktop/Study/Python/xunlei/pic/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'host': 'act.vip.xunlei.com'}


def requestAllUrl():
    resp = requests.get(all_url, headers=headers)
    jsontext = resp.content
    json_match = re.search(r'\[.*\]', jsontext)
    if json_match is None:
        raise 'match Error'
    else:
        json_a = json.loads(json_match.group())
    if json_a is None:
        raise 'json Error'
    else:
        yield json_a


def pic_request(tup):
    print (tup)
    num = tup[1]
    pic_name = tup[0]
    path = pic_path + pic_name
    os.chdir(path)
    for i in range(int(num)):
        resp = requests.get(built_url(pic_name, i + 1))
        if resp is None:
            raise 'Error'
        else:
            filename = '%s_%s.jpg' % (pic_name, i + 1)
            with open(filename, 'wb') as f:
                f.write(resp.content)


def built_url(name, num):
    url = '%s%s/%s.jpg' % (pic_url, name, num)
    return url


def main():
    try:
        json_a = requestAllUrl()
    except Exception as e:
        print e

    p = Pool(4)
    for dic in json_a:
        try:
            os.chdir(pic_path)
            title = dic['title']
            match = re.search(r'花絮$', title)
            print match
            if match is None and int(dic['totals']) != 1:
                os.makedirs(dic['resource_id'])
                tup = (dic['resource_id'], dic['totals'])
                p.apply_async(pic_request, args=(tup,))
        except Exception as e:
            print e
    p.close()
    p.join()


if __name__ == '__main__':
    main()



