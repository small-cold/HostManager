#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

import time
from configs import configs as cfs

SYS_HOSTS_PATH = '/etc/hosts'


def backup(file_name=None, backup_path=None):
    """
    备份系统文件
    """
    if not backup_path:
        raise Exception('备份目录不能为空')
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


def get_common_hosts():
    """
    读取通用配置
    :return:
    """
    if not cfs.common_hosts or len(cfs.common_hosts) == 0:
        return ''

    content = ''
    for hosts in cfs.common_hosts:
        try:
            with open(os.path.join(cfs.work_path, hosts), 'r') as f:
                content += '#------- ' + hosts + ' start --------------\n'
                content += f.read() + '\n'
                content += '#------- ' + hosts + ' end --------------\n'
        except Exception as e:
            print('读取通用配置文件失败', e)
    return content


def switch_by_num(index=0, ignore=''):
    """
    根据文件序号，切换文件
    :param index:
    :param ignore:
    :return:
    """
    path = os.path.join(cfs.work_path, cfs.env_path)
    files = [f for f in os.listdir(path) if os.path.isdir(path)]
    file_name = files[index]
    switch(os.path.join(path, file_name), title=file_name, ignores=ignore.split(','))


def switch(source_path, title='新环境', ignores=[]):
    """
    切换系统 hosts 文件
    """
    if not source_path:
        raise Exception('路径不能为空')
    print(os.path.exists(source_path), os.path.isdir(source_path))
    if not os.path.exists(source_path) or os.path.isdir(source_path):
        raise Exception('文件不存在')
    content = get_common_hosts()
    with open(source_path, 'r') as f:
        content += '#-------------' + title + '------- start -----------------\n'
        while True:
            line = f.readline()
            if not line:
                break
            for ignore in ignores:
                if not ignore or len(ignore) == 0:
                    continue
                if line.rfind(ignore) > -1:
                    print('忽略：', line)
                    line = '#' + line
                    break
            content += line
        content += '#-------------' + title + '------- end -------------------\n'
    # 写入hosts文件
    with open(SYS_HOSTS_PATH, 'w') as f:
        f.write(content)
    # 刷新 hosts
    flush_hosts()


def host_to(host, ip='127.0.0.1'):
    """
    将当期环境切换到本地
    :param ip:
    :param host:
    :return:
    """
    if not host:
        return
    content = ''
    edited = False
    with open(SYS_HOSTS_PATH, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            # 第一个是ip，后面是域名
            attrs = re.compile('[\w\\.-]+').findall(line)
            if not attrs or len(attrs) == 0 or host not in attrs[1:]:
                content += line
                continue
            # 要修改的地址不在该行
            if host in attrs[1:]:
                if len(attrs) == 2 and edited:
                    continue
                # 该配置存在，更换配置，将原来的注释
                if attrs[0] != ip:
                    if line.startswith('#'):
                        content += line
                    else:
                        content += '#' + line
                        content += ip + '\t\t'
                        for host_temp in attrs[1:]:
                            content += host_temp + '\t\t'
                        content += '\n'
                        edited = True
                else:
                    if not line.startswith('#'):
                        print('该配置已经存在', line)
                        return
                    else:
                        content += ip + '\t\t'
                        for host_temp in attrs[1:]:
                            content += host_temp + '\t\t'
                        content += '\n'
                        edited = True
            else:
                content += line

    if not edited:
        content += ip + '\t\t' + host + '\n'
    with open(SYS_HOSTS_PATH, 'w') as f:
        f.write(content)


def flush_hosts():
    # Update dns cache
    # windows
    # os.system('ipconfig /flushdns')
    # mac
    os.system('killall -HUP mDNSResponder')


if __name__ == '__main__':
    # switch_by_num()
    host_to('m.liepin.com')
    host_to('m.liepin.com', '123.123.1.1')
