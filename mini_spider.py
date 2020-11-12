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
    # get input params
    args = parm_parser.get_args()
    # init log config
    log.init_log('./log/mini_spider')
    if args:
        # read config file spider.conf
        conf_params = parm_parser.set_config_by_file(args.conf)
        # use config set up spider initial params
        spider = SpiderWorker(conf_params)
        # init result_path, make it complete
        spider.set_path()
        # init url queue
        spider.set_url_queue()
        # start to crawl url
        spider.start_crawl_work()

    return

if __name__ == '__main__':
    main()

