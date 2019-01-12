# -*- coding: utf-8 -*-

"""
--------------------------------------------------------
# @Version : python3.7
# @Author  : wangTongGen
# @File    : 001_爬取微博页.py
# @Software: PyCharm
# @Time    : 2019/1/12 15:44
--------------------------------------------------------
# @Description: 
--------------------------------------------------------
"""

import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo



client = pymongo.MongoClient(host='localhost', port=27017)  # 连接mongodb
db = client['spider']  # 指定数据库 client.spider也可以
collection = db['weibo']  # 指定集合 db['students']也可以

base_url = "https://m.weibo.cn/api/container/getIndex?"

headers = {
    'Host':'m.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',

}


def get_page(page):

    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page,
    }

    url = base_url + urlencode(params)


    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Error: ", e)


def parse_json(json):

    if json:
        items = json.get('data').get('cards')

        for item in items:
            item = item.get('mblog')
            if item:
                weibo = {}
                weibo['id'] = item.get('id') # 微博id
                weibo['text'] = pq(item.get('text')).text() # 微博正文
                weibo['attitudes'] = item.get('attitudes_count') # 获赞次数
                weibo['comments'] = item.get('comments_count') # 评论数
                weibo['reposts'] = item.get('reposts_count') # 转发数

                yield weibo



def write2mongodb(result):
    if collection.insert_one(result):
        print("Successful!")
    else:
        print("Failed!....................")



if __name__ == '__main__':

    for page in range(1,11):
        json = get_page(page)
        results = parse_json(json)

        for result in results:
            write2mongodb(result)