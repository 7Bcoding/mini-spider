# /usr/bin/python
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This is main module
author cenquanyu(com@baidu.com)
"""

import log
from worker import SpiderWorker
from worker import param_parser


def main():
    """
    Main method to run mini spider
    """
    # get input params
    parm_parse = param_parser.parm_parser()
    args = parm_parse.get_args()
    # init log config
    log.init_log('./log/mini_spider')
    if args:
        # read config file spider.conf
        conf_params = parm_parse.set_config_by_file(args.conf)
        # use config set up spider initial params
        spider = SpiderWorker.SpiderWorker(conf_params)
        # init result_path, make it complete
        spider.set_path()
        # init url queue
        spider.set_url_queue()
        # start to crawl url
        spider.start_crawl_work()

    return


if __name__ == '__main__':
    main()
