import unittest

from worker import SpiderWorker


class SpiderWorkerTest(unittest.TestCase):
    def test_set_path(self):
        t = SpiderWorker.SpiderWorker("www.baidu.com", "output", 1, 1, 1, 1)
        self.result_path = './result.data'
        t.set_path()
        print(t.result_path)

    def test_set_abs_dir(self):
        t = SpiderWorker.SpiderWorker("www.baidu.com", "output", 1, 1, 1, 1)
        filepath = t.set_abs_dir('./result.data')
        print(filepath)


if __name__ == '__main__':
    unittest.main()
