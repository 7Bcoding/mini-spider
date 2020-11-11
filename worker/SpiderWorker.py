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

from worker.UrlHandler import UrlHandler


class SpiderWorker(object):
    def __init__(self, *args, **kwargs):
        params = args[0]
        self.urls = params[0]
        self.result = params[1]
        self.maxdepth = params[2]
        self.interval = params[3]
        self.timeout = params[4]
        self.thread_count = params[5]
        self.target_url = ".*\.(gif|png|jpg|bmp)$"
        self.urlqueue = Queue()

    def start_work(self):
        url_arr = []  # 首页链接列表
        try:
            content = UrlHandler.get_content(self.urls)
            sub_urls = UrlHandler.get_urls(self.urls)
            for url in sub_urls:
                self.urlqueue.put(url)
            print(len(sub_urls), sub_urls)
            self.page_detail()
            # logging.info('there is the page:')
            # logging.info(urlarr)
        except Exception as e:
            logging.error(e)

    def page_detail(self):
        urls = self.urlqueue.get()
        print(urls, '子页面链接为：')
        response = requests.get(urls)
        soup = BeautifulSoup(response.text, 'html.parser')
        url_list = soup.select('a')
        for links in url_list:
            if links.has_attr('href'):
                print(links['href'], end=',')

