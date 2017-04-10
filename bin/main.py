#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-04-03 19:48:30
# @Author  : Small Cold (small.cold.go@gmail.com)
# @Link    : https://github.com/small-cold
# @Version : 0.0.1

import os
import time
from optparse import OptionParser, OptionGroup

from hosts import backup, switch_by_num, host_to
from remote import download_remote_env
from configs import configs as cfs


def show_list(title, path):
    """
    展示可选环境列表
    :param path:
    :param title:
    :return:
    """
    print(title)
    files = [f for f in os.listdir(path) if os.path.isdir(path)]
    index = 0
    for env in files:
        if str(env).startswith('.'):
            continue
        print(index, env, sep=':', end=', ')
        index += 1
    print()


def main():
    cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 读取配置文件
    # 初始化命令解析器
    parser = OptionParser()

    # 备份命令组
    group_bak = OptionGroup(parser, "备份命令：",
                            "备份当前系统host文件内容，可以指定文件名称")
    group_bak.add_option("-b", "--backup", action="store_true",
                         dest='backup', help="备份当前的hosts环境")
    group_bak.add_option("--name", action="store", dest='backupname',
                         default=cur_time, help="备份名称，默认为当前时间")
    parser.add_option_group(group_bak)

    # 切换环境
    parser.add_option("-L", "--list", action="store_false", default=True,
                      dest="show_list", help="可选环境列表")
    # 备份命令组
    parser.add_option("-s", "--switch", action="store", type='int',
                            dest="switch", help="切换环境，需要管理员权限，默认会备份当前host")

    parser.add_option('-i', '--ignore', action='store', type='string', default='',
                      dest="ignore", help="切换环境，需要忽略的内容")

    parser.add_option("--detail", action="store",
                      dest="env_name_detail", help="打印环境的详细信息")
    # 下载环境
    parser.add_option("-d", "--download", action="store_true", default=False,
                      dest="download", help="下载环境", metavar="FILE")
    # 本地环境列表
    parser.add_option("-l", "--local", action="store", dest="local", default=True,
                      help="切换域名至本地")
    parser.add_option("--ip", action="store", dest="ip", default='127.0.0.1',
                      help="指定IP地址")
    # 版本
    parser.add_option("-V", "--version", action="store_false", dest="verbose", default=True,
                      help="显示版本")
    parser.add_option("--config", action="store_true", dest="show_configs", default=False,
                      help="显示版本")
    (options, args) = parser.parse_args()
    # print(options, args)
    if options.verbose:
        print('Host Manage 版本为', cfs.version)

    # 备份系统环境
    if options.show_configs:
        print('配置信息：')
        for k, v in cfs.items():
            print('   ', k, '=', v)

    # 备份环境
    if options.backup or cfs.auto_backup:
        backup(options.backupname, os.path.join(cfs.work_path, cfs.backup_path))

    # 切换环境
    if options.switch:
        switch_by_num(options.switch, options.ignore)

    if options.local:
        host_to(options.local, options.ip)

    if options.show_list:
        show_list('可选环境如下', os.path.join(cfs.work_path, cfs.env_path)),
        show_list('可恢复备份如下', os.path.join(cfs.work_path, cfs.backup_path))

    if options.download:
        download_remote_env(cfs.remote_env, os.path.join(cfs.work_path, cfs.env_path))


if __name__ == '__main__':
    main()
