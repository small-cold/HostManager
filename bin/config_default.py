#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
默认配置
"""

import os

__author__ = 'Small Cold'

configs = {
    "version": "1.0.0",
    'work_path': os.path.join(os.path.expanduser('~'), '.hosts'),
    'env_path': 'environments',
    'backup_path': 'backup',
    'config_file': 'setting-user.json',
}
