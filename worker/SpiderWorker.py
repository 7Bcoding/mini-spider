# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################

from queue import Queue
from bs4 import BeautifulSoup
import requests
import log
import logging


class SpiderWorker(object):
    def __init__(self, *args, **kwargs):
        params = args[0]
        self.urls = params[0]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
        self.result = params[1]
        self.maxdepth = params[2]
        self.interval = params[3]
        self.timeout = params[4]
        self.thread_count = params[5]
        self.target_url = ".*\.(gif|png|jpg|bmp)$"
        self.urlqueue = Queue()

    def getpages(self):
        url_arr = []  # 首页链接列表
        try:
            response = requests.get(self.urls, self.headers['User-Agent'])
            soup = BeautifulSoup(response.text, 'html.parser')
            url_list = soup.select('a')
            for links in url_list:
                if links.has_attr('href'):
                    self.urlqueue.put(self.urls + links['href'])
                    url_arr.append(self.urls + links['href'])
            urlarr = list(set(url_arr))
            print(len(urlarr), urlarr)
            self.page_detail()
            # logging.info('there is the page:')
            # logging.info(urlarr)
        except Exception as e:
            logging.error(e)

    def page_detail(self):
        urls = self.urlqueue.get()
        print(urls, '详细内容为：')
        response = requests.get(urls, self.headers['User-Agent'])
        soup = BeautifulSoup(response.text, 'html.parser')
        url_list = soup.select('a')
        for links in url_list:
            if links.has_attr('href'):
                print(links['href'], end=',')

