import requests
from lxml import etree
import random
import threading
from time import sleep
from queue import Queue


class ImageSpider():
    def __init__(self):
        self.urls = 'http://www.xxxx/{}'
        self.detail = 'http://www.xxx.com/xxx/{}'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Cookie': 'UM_distinctid=16b7398b425391-0679d7e790c7ad-3e385b04-1fa400-16b7398b426663'
                      ';Hm_lvt_7a498bb678e31981e74e8d7923b10a80=1561012516;CNZZDATA1270446221 = 1356308073 - '
                      '1561011117 - null % 7C1561021918;Hm_lpvt_7a498bb678e31981e74e8d7923b10a80 = 1561022022',
            'Host': 'xxx.xxx.com',
            'If-None-Match': '"5b2b5dc3-2f7a7"',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.xxxx.com/cosplay/68913_2.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36',
        }
        self.url_queue = Queue()

    def getpages(self):
        response = requests.get(self.urls.format(2))
        strs = response.content.decode()
        html = etree.HTML(strs)
        page = html.xpath('/html/body/section[1]/nav/div/a/text()')
        return page[-2]

    def html_list(self, page):
        print(self.urls.format(page))
        response = requests.get(self.urls.format(page))
        strs = response.content.decode()
        html = etree.HTML(strs)
        page = html.xpath('/html/body/section[1]/div/ul/li/div[1]/a/@href')
        return page

    def page_detail(self, imgde):
        response = requests.get(self.detail.format(imgde))
        strs = response.content.decode()
        html = etree.HTML(strs)
        page = html.xpath("//*[@id='imagecx']/div[4]/a[@class='page-numbers']/text()")
        return page[-1]

    def detail_list(self, imgde, page):
        # 截取链接关键码
        urls = imgde[-10:-5]
        print('开始访问图片页面并抓取图片地址保存')
        for i in range(int(page)):
            print(self.detail.format(urls + '_' + str(i + 1) + '.html'))
            urlss = self.detail.format(urls + '_' + str(i + 1) + '.html')
            self.url_queue.put(urlss)
        for i in range(int(page)):
            t_url = threading.Thread(target=self.pagemore_list)
            # t_url.setDaemon(True)
            t_url.start()
        self.url_queue.join()
        print('主线程结束进行下一个')

    def pagemore_list(self):
        urls = self.url_queue.get()
        response = requests.get(urls)
        strs = response.content.decode()
        html = etree.HTML(strs)
        imgs = html.xpath('//*[@id="imagecx"]/div[3]/p/a/img/@src')
        # 保存图片
        self.save_img(imgs)

    def save_img(self, imgs):
        try:
            print(imgs[0])
            response = requests.get(imgs[0], headers=self.headers)
        except:
            print('超时跳过')
            self.url_queue.task_done()
            return
        else:
            strs = response.content
            s = random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 5)
            a = random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 5)
            with open("./imgsa/" + str(a) + str(s) + ".jpg", "wb") as f:
                f.write(strs)
            print("保存图片")
            self.url_queue.task_done()
            return

    def run(self):
        page = 1
        # 获取总页数
        pageall = self.getpages()
        print('总页数' + str(pageall))
        while True:
            print('访问第' + str(page) + '页')
            # 访问页面，获取10组图片的详情页链接
            html_list = self.html_list(page)
            # 访问图片的详情页
            s = 1
            for htmls in html_list:
                print('访问第' + str(page) + '页第' + str(s) + '组')
                imgdetalpage = self.page_detail(htmls)
                # 址遍历详情页请求获取图片地
                print('第' + str(page) + '页第' + str(s) + '组有' + str(imgdetalpage) + '张图片')
                self.detail_list(htmls, imgdetalpage)
                s += 1
            page += 1
            if page > pageall:
                print('爬取完毕 退出循环')
                return


if __name__ == '__main__':
    spider = ImageSpider()
    spider.run()
