import unittest

from worker import SpiderWorker
from worker import param_parser


class MiniSpiderTest(unittest.TestCase):

    def test_set_config_by_file(self):
        t = param_parser.parm_parser()
        print(t.set_config_by_file('./spider.conf'))

    def test_set_spiderworker_params(self):
        t = SpiderWorker.SpiderWorker("www.baidu.com", "./result.data", 1, 1, 1, 1)
        print(t.set_path())
        print(t.set_url_queue())

    def test_spider_thread_work(self):
        t = SpiderWorker.SpiderWorker("www.baidu.com", "./result.data", 1, 1, 1, 1)
        t.thread_count = 1
        t.timeout = 1
        t.interval = 1
        t.maxdepth = 1
        print(t.start_crawl_work())


if __name__ == '__main__':
    unittest.main()
