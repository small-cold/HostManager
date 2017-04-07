#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-04-03 19:48:30
# @Author  : Small Cold (small.cold.go@gmail.com)
# @Link    : https://github.com/small-cold
# @Version : 0.0.1

import os
import time
import json
from optparse import OptionParser, OptionGroup

# 工作目录
import requests

WORK_PATH_NAME = '.hosts'

# PATH_SETTING_FILE = os.path.join(WORK_PATH, 'setting.json')

# PATH_BACKUP_FOLDER = os.path.join(WORK_PATH, 'backup')

# 系统hosts文件路径，程序目标就是对其进行修改
SYS_HOSTS_PATH = '/etc/hosts'


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


def backup(file_name=None):
    """
    备份系统文件
    """
    backup_path = os.path.join(get_work_path(), "backup")
    if not os.path.exists(backup_path):
        print('创建文件夹', backup_path)
        os.makedirs(backup_path)

    with open(SYS_HOSTS_PATH, 'r') as file:
        content = file.read()
    if not file_name:
        file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    with open(os.path.join(backup_path, file_name), 'w') as file:
        file.write(content)
    print('备份当前Hosts文件成功：', file_name)


def get_work_path():
    return os.path.join(os.path.expanduser('~'), WORK_PATH_NAME)


def get_configs():
    """
    初始化插件配置
    """
    setting_user_path = os.path.join(get_work_path(), "setting-user.json")
    if not os.path.exists(setting_user_path) or not os.path.isfile(setting_user_path):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../conf/setting-user.json'), 'r') as file:
            default_content = file.read()
        with open(setting_user_path, 'w') as file:
            file.write(default_content)
    # 读取配置文件，解析为字典
    config_json = ''
    with open(setting_user_path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            # 删除注释
            if line.strip().startswith('//'):
                continue
            config_json += line
    return json.loads(config_json)


def download_remote_env(remotes, path='env'):
    """
    下载远程环境文件
    :param urls:
    :param path:
    :return:
    """
    if not remotes or len(remotes) == 0:
        return
    env_path = os.path.join(get_work_path(), path)
    if not os.path.exists(env_path) or os.path.isfile(env_path):
        os.makedirs(env_path)

    for remote in remotes:
        name = remote.get('name', None)
        url = remote.get('url', None)
        if not name or not url:
            continue

        with open(os.path.join(env_path, name), 'w') as f:
            f.write(requests.get(url).text)


def show_list():
    print('可选环境列表如下:')
    env_path = os.path.join(get_work_path(), 'env')
    files = [f for f in os.listdir(env_path) if os.path.isdir(env_path)]
    index = 0
    for env in files:
        if str(env).startswith('.'):
            continue
        print(index, env)
        index += 1
    print('可选备份文件列表如下:')
    backup_path = os.path.join(get_work_path(), 'backup')
    files = [f for f in os.listdir(backup_path) if os.path.isdir(backup_path)]
    index = 0
    for env in files:
        if str(env).startswith('.'):
            continue
        print(index, env)
        index += 1


def main():

    cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 读取配置文件
    configs = get_configs()
    print('配置信息：', configs)

    # 初始化命令解析器
    parser = OptionParser()

    # 备份命令组
    group = OptionGroup(parser, "备份命令：",
                        "备份当前系统host文件内容，可以指定文件名称")
    group.add_option("-b", "--backup", action="store_true",
                     dest='backup', help="备份当前的hosts环境")
    group.add_option("--name", action="store", dest='backupname',
                     default=cur_time, help="备份名称，默认为当前时间")
    parser.add_option_group(group)

    # 切换环境
    parser.add_option("-L", "--list", action="store_true", default=False,
                      dest="show_list", help="可选环境列表")
    parser.add_option("-e", "--environment", action="store",
                      dest="env_name", help="切换环境，需要管理员权限，默认会备份当前host")
    parser.add_option("--detail", action="store",
                      dest="env_name_detail", help="打印环境的详细信息")
    # 下载环境
    parser.add_option("-d", "--download", action="store_true", default=False,
                      dest="download", help="下载环境", metavar="FILE")
    # 本地环境列表
    parser.add_option("-l", "--local", action="store", dest="local", default=True,
                      help="切换域名至本地")
    # 版本
    parser.add_option("-V", "--version", action="store_false", dest="verbose", default=True,
                      help="显示版本")
    (options, args) = parser.parse_args()
    print(options, args)
    # 备份系统环境
    if options.backup:
        backup(options.backupname)

    if options.show_list:
        show_list()

    if options.download:
        download_remote_env(configs.get('remote_env', None))


if __name__ == '__main__':
    main()
