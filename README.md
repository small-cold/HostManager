# 1. 使用说明
## 1.1 安装与使用
1. 系统安装有Python3.5 +
2. 下载或者clone到本地
3. 设置软连接 bin/hm.py 到 /usr/bin  或者 /usr/local/bin
```
ln -s bin/hm.py /usr/local/bin/hm
```
4. 输入 
```hm -V``` 
能看见输出就可以使用了。具体帮助请使用 hm --help 命令

## 1.1 配置接口，自动获取host内容
根据常用配置，设置是否启用配置，配置文件默认存放路径为 
~/.hosts/setting-user.json
```json
{
  //  远程环境数组
  "remote_env": [
    {"name": "名字1", "url": "http://localhost/hosts1"},
    {"name": "名字1", "url": "http://localhost/hosts2"},
  ],
  //  是否开启自动备份，如果开启，在切换环境前，会备份当前hosts文件
  "auto_backup": false,
  //  备份数量，最早的将被删除
  "backup_limit_count": 10,
  // 通用配置文件
  "common_hosts": ["environments/common"]
}
```


# 2. 参数说明
```
Options:
  -h, --help            show this help message and exit
  -L, --list            可选环境列表
  -s SWITCH, --switch=SWITCH
                        切换环境，需要管理员权限，默认不会备份当前host
  -i IGNORE, --ignore=IGNORE
                        切换环境，需要忽略的内容
  --detail=ENV_NAME_DETAIL
                        打印环境的详细信息
  -d, --download        下载环境
  -c CURRENT, --current=CURRENT
                        当前配置
  --ip=IP               指定IP地址
  -V, --version         显示版本
  --config              显示配置信息

  备份命令：:
    备份当前系统host文件内容，可以指定文件名称

    -b, --backup        备份当前的hosts环境
    --name=BACKUPNAME   备份名称，默认为当前时间
```