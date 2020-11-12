# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This main module
"""
from urllib import parse

import log
from worker.SpiderWorker import SpiderWorker
from worker.param_parser import parm_parser


def main():
    """
    the main method to run mini spider
    """
    # 获取控制台输入参数
    args = parm_parser.get_args()
    # 初始化日志配置
    log.init_log('./mini_spider')
    if args:
        # 读取配置文件spider.conf，获取参数
        conf_params = parm_parser.set_config_by_file(args.conf)
        # 通过配置文件设置爬虫初始化参数
        spider = SpiderWorker(conf_params)
        spider.start_work()


if __name__ == '__main__':
    main()

