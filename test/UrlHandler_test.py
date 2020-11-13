import unittest

from worker import UrlHandler


class UrlHandlerTest(unittest.TestCase):

    def test_get_urls(self):
        """
        test get urls in the original url
        :return: nothing
        """
        UrlHandler.UrlHandler.get_urls('www.baidu.com')

    def test_download(self):
        """
        test download url to file
        :return: nothing
        """
        UrlHandler.UrlHandler.download_url("D:\\test\\test", "https://www.baidu.com/")

    def test_get_html_content(self):
        """
        get the html code from from url
        :return: nothing
        """
        print(UrlHandler.UrlHandler.get_content("https://www.baidu.com"))

    def test_get_url(self):
        """
        test get urls in the original url
        :return: nothing
        """
        print(UrlHandler.UrlHandler.get_urls("http://www.baidu.c)om"))

    def test_is_url(self):
        """
        test check url
        :return:nothing
        """
        print(UrlHandler.UrlHandler.is_url("javadscriptddddddd"))


if __name__ == '__main__':
    unittest.main()
