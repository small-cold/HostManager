#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

import config_default

configs = None


class Setting(dict):
    """
    配置类
    """

    def __init__(self, names=(), values=(), **kw):
        super(Setting, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def to_setting(d):
    D = Setting()
    for k, v in d.items():
        D[k] = to_setting(v) if isinstance(v, dict) else v
    return D


def merge(defaults, override):
    r = defaults
    for k, v in override.items():
        if k in defaults:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def get_user_configs(work_path, config_file_name='setting-user.json'):
    """
    初始化插件配置
    """
    setting_user_path = os.path.join(work_path, config_file_name)
    if not os.path.exists(setting_user_path) or not os.path.isfile(setting_user_path):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../conf/' + config_file_name), 'r') as file:
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


# 加载默认配置和用户配置
if not configs:
    work_path = config_default.configs.get('work_path', None)
    if not work_path:
        raise Exception('工作目录不能为空')
    configs = to_setting(merge(config_default.configs, get_user_configs(work_path, config_default.configs.get('config_file', 'setting-user.json'))))


