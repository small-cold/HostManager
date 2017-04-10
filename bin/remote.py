#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import requests


def download_remote_env(remotes, path=''):
    """
    下载远程环境文件
    :param remotes:
    :param path:
    :return:
    """
    if not remotes or len(remotes) == 0:
        return
    if not os.path.exists(path) or os.path.isfile(path):
        os.makedirs(path)

    for remote in remotes:
        name = remote.get('name', None)
        url = remote.get('url', None)
        if not name or not url:
            continue

        with open(os.path.join(path, name), 'w') as f:
            f.write(requests.get(url).text)

if __name__ == '__main__':
    from configs import configs
    download_remote_env(configs.remote_env, os.path.join(configs.work_path, configs.env_path))
