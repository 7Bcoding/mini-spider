import os
import urllib
import urllib3
from urllib import parse
import logging
import chardet
from bs4 import BeautifulSoup
import requests
from worker import SpiderWorker


class UrlHandler(object):
    """
    public url tools for handle url
    """

    @staticmethod
    def is_url(url):
        """
        ignore url starts with javascipt
        :param url:
        :return:True False
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
            response = requests.get(url)
        except requests.HTTPError as e:
            logging.error("url %s request error : %s" % (url, e))
            return None

        try:
            content = response.text
        except Exception as e:
            logging.error("response content error : %s" % e)
            return None

        return content

    @staticmethod
    def decode_html(content):
        """
        decode content
        :param content: the origin content
        :return: returen decoded content. Error return None
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
        get the suburls of this url
        :param url: origin url
        :return:the set of sub_urls
        """
        urlset = set()
        if not UrlHandler.is_url(url):
            return urlset

        content = UrlHandler.get_content(url)
        if content is None:
            return urlset

        tag_list = ['img', 'a', 'style', 'script']
        linklist = []

        # for tag in tag_list:
        #     linklist.extend(BeautifulSoup(content).find_all(tag))

        linklist.extend(BeautifulSoup(content, 'html.parser').select('a'))

        for link in linklist:
            # if link.has_attr('src'):
            #     urlset.add(link)
            if link.has_attr('href'):
                urlset.add(link)

        return urlset
