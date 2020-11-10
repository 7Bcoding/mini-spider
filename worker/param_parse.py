# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
import argparse
import logging
import log
import configparser


class config_parser(object):
    def set_config_by_file(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        urls = config['spider']['feedfile']  # feedfile path
        result = config['spider']['result']  # result storage file
        max_depth = config['spider']['max_depth']  # max scratch depth
        crawl_interval = config['spider']['crawl_interval']  # scratch interval
        crawl_timeout = config['spider']['crawl_timeout']  # scratch timeout
        thread_count = config['spider']['thread_count']  # scratch thread
        return urls, result, max_depth, crawl_interval, crawl_timeout, thread_count


class args_parser(object):
    def get_args(self):
        try:
            parser = argparse.ArgumentParser(prog='mini_spider',
                                             usage='minispider using method',
                                             description='mini_spider is a Multithreaded crawler')
            parser.add_argument('-c', '--conf', help='config_file')
            parser.add_argument('-v', '--version', help='version', action="store_true")
        except argparse.ArgumentError as e:
            logging.error("get option error : %s." % e)
            return
        args = parser.parse_args()
        print(args)
        if args.version:
            self.version()
        if args.conf:
            return args

    def version(self):
        """
        print version
        """
        print("mini_spider version 1.0.0")

