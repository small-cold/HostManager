#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

import time
from configs import configs as cfs

SYS_HOSTS_PATH = '/etc/hosts'

DOMAIN_RE = re.compile(r'[\w\\.-]+')
IP_RE = re.compile(r'(?<![\\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\\.\d])')

'''
hosts 解析实体
'''

class Host(object):
    def __init__(self, domain=None, ip=None, enable=True):
        self.enable = enable
        self.ip = ip
        self.domain = domain
        self.comment = None

    def __setattr__(self, key, value):
        # print(key, value)
        if key == 'ip':
            if value is None or isinstance(value, str) and IP_RE.match(value):
                self._ip = value
            else:
                raise Exception('IP 格式错误 value=' + value)
        elif key == 'domain':
            if value is None:
                self._domain = value
            elif isinstance(value, str):
                self._domain = DOMAIN_RE.findall(value)
                self.enable = value
            elif isinstance(value, list):
                self._domain = value
            elif isinstance(value, tuple):
                self._domain = list(value)
            else:
                raise Exception('domain 类型错误 value=' + value)
        elif key == 'enable':
            if value is None:
                self._enable = True
            elif isinstance(value, str):
                self._enable = not value.strip().startswith('#')
            elif isinstance(value, bool):
                self._enable = value
            else:
                raise Exception('enable 类型错误 value=' + value)
        else:
            super().__setattr__(key, value)

    def __str__(self):
        result = ''
        if self.comment is not None:
            result = self.comment + "\n"
        if self._ip is not None and '' != self.get_ip().strip() and self._domain is not None:
            if not self.get_enable():
                result += '# '
            result += self._ip + '\t\t' + self._domain[0]
            if len(self._domain) >= 2:
                for dm in self._domain[1:]:
                    result += '  ' + dm
            result += '\n'
        return result

    def __eq__(self, other):
        if not isinstance(other, Host):
            return False
        if self.get_domain() is not None and other.get_domain() is not None:
            domain_eq = self.get_domain() == other.get_domain() or set(self.get_domain()).issubset(set(other.get_domain())) \
                        or set(other.get_domain()).issubset(set(self.get_domain()))
        else:
            domain_eq = self.get_domain() == other.get_domain()

        return domain_eq and self.get_ip() == other.get_ip() and self.get_enable() == other.get_enable()

    def init(self, line):
        if not isinstance(line, str):
            raise Exception('line is Not str')
        if line is None:
            raise Exception('line is not allow None or blank')
        line = line.strip()
        if line.startswith('#') and not DOMAIN_RE.search(line):
            self.comment = line
        elif IP_RE.search(line):
            # 第一个是ip，后面是域名
            attrs = DOMAIN_RE.findall(line)
            if len(attrs) >= 2:
                self.domain = attrs[1:]
                self.ip = attrs[0]
                self.enable = line
            else:
                self.comment = line
        else:
            self.comment = line
        return self

    def switch(self, domain, ip):
        if self.get_domain() is None or self.get_ip() is None:
            return [self]
        if len(self.get_domain()) > 0 and domain in self.get_domain():
            if ip != self.get_ip():
                if len(self.get_domain()) == 1:
                    self.enable = not self._enable
                else:
                    self.get_domain().remove(domain)
                    return [Host(domain, ip), self]
            else:
                self.enable = True
        return [self]

    def get_ip(self):
        return self._ip

    def get_domain(self):
        return self._domain

    def get_enable(self):
        return self._enable

    def get_comment(self):
        return self.comment

    def is_config(self, domain, ip):
        return self._ip == ip and domain in self._domain and self._enable


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
    files = [f for f in os.listdir(path) if os.path.isdir(path) and not f.startswith(".")]
    file_name = files[index]
    switch(os.path.join(path, file_name),
           title=file_name, ignores=ignore.split(','))


def switch(source_path, title='新环境', ignores=[]):
    """
    切换系统 hosts 文件
    """
    if not source_path:
        raise Exception('路径不能为空')
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


def get_host_list_by_domain(domain, path=SYS_HOSTS_PATH):
    return [host for host in get_host_list(path) if host.get_domain() is not None and domain in host.get_domain()]


def get_host_list(path=SYS_HOSTS_PATH):
    host_list = []
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            host = Host().init(line)
            host_list.append(host)
    return host_list


def host_to(domain, ip='127.0.0.1', path=SYS_HOSTS_PATH):
    """
    将当期环境切换到指定IP
    :param ip:
    :param domain:
    :return:
    """
    if domain is None:
        raise Exception('域名不能为 None')
    domain = domain.strip()
    ip = ip.strip()
    if not domain:
        return
    host_list = get_host_list(path)
    new_host_list = []
    for host in host_list:
        # result = host.switch(domain, ip)
        # for r in result:
            # print('host result is ', r)
        new_host_list.extend(host.switch(domain, ip))

    dest_host = Host(domain, ip)
    if dest_host not in new_host_list:
        new_host_list.append(dest_host)
    with open(SYS_HOSTS_PATH, 'w') as f:
        for host in new_host_list:
            f.write(str(host))


def flush_hosts():
    # Update dns cache
    # windows
    # os.system('ipconfig /flushdns')
    # mac
    os.system('killall -HUP mDNSResponder')


if __name__ == '__main__':
    # switch_by_num()
    # host_to('baidu.com')
    # host_to('m.baidu.com', '123.123.1.1')
    print(Host('baidu.com', '11.11.11.11') in [Host('baidu.com', '11.11.11.11')])
    print("", Host('baidu.com', '11.11.11.11') == Host('m.baidu.com  baidu.com', '11.11.11.11'))
    # host_list = []
    # hosts_content = ''
    # with open(SYS_HOSTS_PATH, 'r') as f:
    #     while True:
    #         lineTemp = f.readline()
    #         if not lineTemp:
    #             break
    #         host = Host().init(lineTemp)
    #         host_list.append(host)
    #         print('对比一行结果：', lineTemp, host, '--------------------', sep="\n")
    host_temp = Host().init('#11.11.11.11 m.baidu.com\t\twww.baidu.com')
    print(host_temp)
    print('-------')
    result = host_temp.switch('m.baidu.com', '11.11.11.12')
    print(len(result))
    if isinstance(result, list):
        for h in result:
            print(h)
    if Host('m.baidu.com', '11.11.11.12') not in result:
        print(Host('m.baidu.com', '11.11.11.12'))
