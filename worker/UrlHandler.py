# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module is used to handle URL and HTTP related requests
author cenquanyu@baidu.com
"""
import os
from urllib import parse, request
import logging
import chardet
from bs4 import BeautifulSoup
import requests


class UrlHandler(object):
    """
    Public url tools for handle url
    """

    @staticmethod
    def is_url(url):
        """
        Ignore url starts with Javascipt
        :param url:
        :return: True or False
        """
        if url.startswith("javascript"):
            return False
        return True

    @staticmethod
    def get_content(url, timeout=10):
        """
        Get html contents
        :param url: the target url
        :param timeout: request timeout, default 10
        :return: content of html page, return None when error happens
        """
        try:
            response = requests.get(url, timeout=timeout)
        except requests.HTTPError as e:
            logging.error("url %s request error : %s" % (url, e))
            return None
        except Exception as e:
            logging.error(e)
            return None

        return UrlHandler.decode_html(response.content)

    @staticmethod
    def decode_html(content):
        """
         Decode html content
        :param content: origin html content
        :return: returen decoded html content. Error return None
        """
        encoding = chardet.detect(content)['encoding']
        if encoding == 'GB2312':
            encoding = 'GBK'
        else:
            encoding = 'utf-8'
        try:
            content = content.decode(encoding, 'ignore')
        except Exception as err:
            logging.error("Decode error: %s.", err)
            return None
        return content

    @staticmethod
    def get_urls(url):
        """
        Get all suburls of this url
        :param url: origin url
        :return: the set of sub_urls
        """
        urlset = set()
        if not UrlHandler.is_url(url):
            return urlset

        content = UrlHandler.get_content(url)
        if content is None:
            return urlset

        tag_list = ['img', 'a', 'style', 'script']
        linklist = []
        for tag in tag_list:
            linklist.extend(BeautifulSoup(content).find_all(tag))

        # get url has attr 'src' and 'href'
        for link in linklist:
            if link.has_attr('src'):
                urlset.add(UrlHandler.parse_url(link['src'], url))
            if link.has_attr('href'):
                urlset.add(UrlHandler.parse_url(link['href'], url))

        return urlset

    @staticmethod
    def parse_url(url, base_url):
        """
        Parse url to make it complete and standard
        :param url: the current url
        :param base_url: the base url
        :return: completed url
        """
        if url.startswith('http') or url.startswith('//'):
            url = parse.urlparse(url, scheme='http').geturl()
        else:
            url = parse.urljoin(base_url, url)

        return url

    @staticmethod
    def download_image_file(result_dir, url):
        """
        Download image as file, save in result dir
        :param result_dir: base_path
        :param url: download url
        :return: succeed True, fail False
        """

        if not os.path.exists(result_dir):
            try:
                os.mkdir(result_dir)
            except os.error as err:
                logging.error("download to path, mkdir errror: %s" % err)

        try:
            path = os.path.join(result_dir, url.replace('/', '_').replace(':', '_')
                                .replace('?', '_').replace('\\', '_'))
            logging.info("download url..: %s" % url)
            request.urlretrieve(url, path, None)
        except Exception as e:
            logging.error("download url %s fail: %s " % (url, e))
            return False
        return True

    @staticmethod
    def download_url(result_file, url):
        """
        Download the URL that matches the characteristics, and save in a file
        :param result_file: base_path
        :param url: download url
        :return: succeed True, fail False
        """

        try:
            path = os.path.join(os.getcwd(), result_file)
            logging.info("download url..: %s" % url)
            with open(path, 'a') as f:
                f.write(url + '\n')
        except Exception as e:
            logging.error("download url %s fail: %s " % (url, e))
            return False
        return True

