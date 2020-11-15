#!/usr/bin/env python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is used to parse params
@Time    : 2020/11/09
@File    : param_parser.py
@Author  : cenquanyu@baidu.com
"""
import argparse
import logging
import configparser


class parm_parser(object):

    @staticmethod
    def set_config_by_file(config_file):
        """
        Set spiderworker params by config file
        :param : config file
        :return: True, False
        """
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        urls = config['spider']['feedfile']  # feedfile path
        result_path = config['spider']['result']  # result storage file
        max_depth = config['spider']['max_depth']  # max scratch depth
        crawl_interval = config['spider']['crawl_interval']  # scratch interval
        crawl_timeout = config['spider']['crawl_timeout']  # scratch timeout
        thread_count = config['spider']['thread_count']  # scratch thread
        filter_url = config['spider']['filter_url']  # URL characteristics
        return urls, result_path, int(max_depth), int(crawl_interval), int(crawl_timeout), int(thread_count), filter_url

    @staticmethod
    def get_args():
        """
        Get console args and parse
        :return: nothing
        """
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
        if args.version:
            parm_parser.version()
        if args.conf:
            return args

    @staticmethod
    def version():
        """
        Print mini spider version
        """
        print("mini_spider version 1.0.0")

