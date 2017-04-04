#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-04-03 19:48:30
# @Author  : Small Cold (small.cold.go@gmail.com)
# @Link    : https://github.com/small-cold
# @Version : 0.0.1

from optparse import OptionParser

# 工作目录
WORK_PATH = '~/.hostSetting'

SETTING_PATH = WORK_PATH + '/setting.json'


class HostSetting(object):

    def __init__(self, path):
        super(HostSetting, self).__init__()
        if not path:
            raise Exception('配置路径不能为空')
        # 配置文件读写路径
        self.path = path
        # 环境地址，可以是一个conf
        self.environment = [{'default', 'env/default'}, ]
        # 本地常用地址
        self.local_domain = []

    def get_remote_host(self):
        return self.remote_host

    def get_local_domain(self):
        return self.local_domain

    def read_setting(self):
        """
        读取配置文件，初始化配置类实例
        """
        setting_str = ''
        with open(SETTING_PATH, 'r') as file:
            setting_str = file.read()
        print()


def init_configs():
    """
    初始化插件配置
    """


def main():
    # 读取配置文件
    configs = init_configs()
    # 初始化命令解析器
    parser = OptionParser()
    # 切换环境
    parser.add_option("-L", "--list", action="store_true",
                      dest="show_list", help="展示环境列表")
    parser.add_option("-d", "--download", action="store_true",
                      dest="download", help="下载环境", metavar="FILE")
    parser.add_option("-e", "--environment", action="store",
                      dest="env_name", help="切换环境", metavar="FILE")
    parser.add_option("-l", "--local", action="store", dest="local", default=True,
                      help="切换域名至本地")
    parser.add_option("-V", "--version", action="store_false", dest="verbose", default=True,
                      help="显示版本")
    (options, args) = parser.parse_args()
    if options.get('show_list', None):


if __name__ == '__main__':
    main()
