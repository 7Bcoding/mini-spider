# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is main worker, central module for crawling tasks
author cenquanyu(com@baidu.com)
"""
import os
from queue import Queue
import logging
from worker.SpiderThread import SpiderThread


class SpiderWorker(object):
    def __init__(self, *args, **kwargs):
        params = args[0]
        self.urls = params[0]
        self.result_path = params[1]
        self.maxdepth = params[2]
        self.interval = params[3]
        self.timeout = params[4]
        self.thread_count = params[5]
        self.filter_url = params[6]
        self.total_urlset = set()
        self.urlqueue = Queue()

    def set_abs_dir(self, path):
        """
        Complete url path ,and mkdir if it not exits
        :param path: url path
        :return: result output path
        """
        file_dir = os.path.join(os.getcwd(), path)
        if not os.path.exists(file_dir):
            try:
                os.mkdir(file_dir)
            except os.error as err:
                logging.error("mkdir result-saved dir error: %s. " % err)
        return str(file_dir)

    def set_path(self):
        """
        Complete the path
        :return:
        """
        self.result_path = self.set_abs_dir(self.result_path)

    def set_url_queue(self):
        """
        Set url queue
        :return: True or False
        """
        try:
            self.urlqueue.put((self.urls, 0))
        except Exception as e:
            logging.error(e)
            return False
        return True

    def start_crawl_work(self):
        """
        Start to work
        :return: nothing
        """
        thread_list = []
        for i in range(self.thread_count):
            thread = SpiderThread(self.urlqueue, self.result_path, self.maxdepth, self.interval,
                                  self.timeout, self.filter_url, self.total_urlset)
            thread_list.append(thread)
            logging.info("%s start..." % thread.name)
            thread.start()
        for thread in thread_list:
            thread.join()
            logging.info("thread %s work is done " % thread.name)

        self.urlqueue.join()
        logging.info("queue is all done")

        return

