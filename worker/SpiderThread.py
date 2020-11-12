# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is the multi thread class for mini_spider
author cenquanyu@baidu.com
"""

import logging
import re
import time
import threading
from queue import Queue
from urllib import parse
from worker.UrlHandler import UrlHandler
from worker import SpiderWorker


class SpiderThread(threading.Thread):
    """
    This module provide multi thread for mini spider
    """

    def __init__(self, urlqueue, result_path, max_depth, interval, timeout, filter_url, total_urlset):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        self.result_path = result_path
        self.max_depth = max_depth
        self.interval = interval
        self.timeout = timeout
        self.filter_url = filter_url
        self.total_urlset = total_urlset
        self.lock = threading.Lock()

    def can_download(self, url):
        """
        judge whether the url can be download. write your download rules here.
        :param url: the url
        :return: True, False
        """
        if not UrlHandler.is_url(url):
            return False
        try:
            # Regular expression matching image URL
            pattern = re.compile(self.filter_url)
        except Exception as e:
            logging.error("the filter url %s is not re..compile fail: %s" % (self.filter_url, e))
            return False
        # if url length < 1 or url is not image type url
        if len(url.strip(' ')) < 1 or not pattern.match(url.strip(' ')):
            return False
        # if url has been in total url set (avoid repeat downloads)
        if url in self.total_urlset:
            return False
        return True

    def run(self):
        """
        Run crawling thread
        Get  task from queue and add sub url into queue, crawling page strategy -- BFS.
        :return: no return
        """
        while True:
            try:
                # get url and the page level
                url, level = self.urlqueue.get(block=True, timeout=self.timeout)
            except Exception as e:
                logging.error('Can not finish the task. job done. %s' % e)
                break

            # print url is None
            self.urlqueue.task_done()
            # sleep interval
            time.sleep(self.interval)

            # judge if url can be download
            if self.can_download(url):
                UrlHandler.download_url(self.result_path, url)
            self.lock.acquire()
            self.total_urlset.add(url)
            self.lock.release()

            suburls = UrlHandler.get_urls(url)

            suburl_level = level + 1

            # if sub url level larger than max_depth, stop crawling page deeper
            if suburl_level > self.max_depth:
                continue

            for suburl in suburls:
                self.urlqueue.put((suburl, suburl_level))