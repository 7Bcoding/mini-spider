# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This main module
"""
import log
from worker import param_parser
from worker import spider_engine


def main():
    """
    the main method to run mini spider
    """
    # 获取控制台输入参数
    parm_parse = param_parser.parm_parser()
    args = parm_parse.get_args()
    # 初始化日志配置
    log.init_log('./mini_spider')
    if args:
        # 读取配置文件spider.conf，获取参数
        conf_params = parm_parse.set_config_by_file(args.conf)
        # 通过配置文件设置爬虫初始化参数
        spider = spider_engine.SpiderEngine(conf_params)
        spider.getpages()


if __name__ == '__main__':
    main()
