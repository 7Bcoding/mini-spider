# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This main module
"""
# /usr/bin/python

import log
from worker import param_parse
from worker import spider_engine


def main():
    """
    the main method to run mini spider
    """
    # 配置文件参数初始化
    conf_parser = param_parse.config_parser()
    argsparser = param_parse.args_parser()
    # 获取控制台输入参数
    args = argsparser.get_args()
    # 初始化日志配置
    log.init_log('./mini_spider')
    if args:
        # 读取配置文件spider.conf，获取参数
        conf_params = conf_parser.set_config_by_file(args.conf)
        # 通过配置文件设置爬虫初始化参数
        spider = spider_engine.SpiderEngine(conf_params)
        spider.getpages()


if __name__ == '__main__':
    main()

