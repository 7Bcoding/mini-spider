# /usr/bin/python

import configparser
import os
from queue import Queue
from lxml import etree
from bs4 import BeautifulSoup
import argparse
import requests
import logging
import logging.handlers


class mini_spider(object):
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


class configparse(object):
    def parse(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        urls = config['spider']['feedfile']  # feedfile path
        result = config['spider']['result']  # result storage file
        max_depth = config['spider']['max_depth']  # max scratch depth
        crawl_interval = config['spider']['crawl_interval']  # scratch interval
        crawl_timeout = config['spider']['crawl_timeout']  # scratch timeout
        thread_count = config['spider']['thread_count']  # scratch thread
        return urls, result, max_depth, crawl_interval, crawl_timeout, thread_count


class argsparse(object):
    def getargs(self):
        parser = argparse.ArgumentParser(prog='mini_spider',
                                         usage='minispider using method',
                                         description='mini_spider is a Multithreaded crawler')
        parser.add_argument('-c', '--conf', help='config_file')
        parser.add_argument('-v', '--version', help='version', action="store_true")
        args = parser.parse_args()
        if args.version:
            print('mini-spider_v1.0')
        else:
            return args


class logger(object):
    def init_log(self, log_path, level=logging.INFO, when="D", backup=7,
                 format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
                 datefmt="%m-%d %H:%M:%S"):
        formatter = logging.Formatter(format, datefmt)
        logger = logging.getLogger()
        logger.setLevel(level)
        dir = os.path.dirname(log_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
                                                            when=when,
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


if __name__ == '__main__':
    args = argsparse().getargs()
    log = logger()
    log.init_log('./mini_spider')
    if args:
        conf_params = configparse().parse(args.conf)
        spider = mini_spider(conf_params)
        spider.getpages()
