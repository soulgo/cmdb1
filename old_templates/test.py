#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 16:49
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : test.py
# @Software: PyCharm
'''遍历目录里的某些文件'''
'''
import os
def get_files(dirpath):
    _rt_list = []
    if os.path.isdir(dirpath):
        _names = os.listdir(dirpath)
        for _name in _names:
            _path = dirpath + "\\" + _name
            if os.path.isdir(_path):
                _rt_list.extend(get_files(_path))
            elif _path.endswith('.py'):
                _rt_list.append(_path)

    return _rt_list


if __name__ == '__main__':
    print(get_files(r"D:\python_projext\Practise"))
'''
#logging模块
'''
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(level=logging.INFO)
formatter = logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")
'''
################argparse模块
'''
import argparse,sys
_parser = argparse.ArgumentParser()
_parser.add_argument('-H','--host',help='connect host ip addr')
_parser.add_argument('-P','--port',help='connect host port addr',type=int,default=80)
_args = _parser.parse_args()
if _args.host is None or _args.port is None:
    print(_parser.print_help())
    sys.exit(-1)
print(_args.host)
print(_args.port)
print('success')
'''
# Jsyd@2017!^
import paramiko,getpass
def ssh_excute(host,username,password,cmds=[],port=22):
    _rt_list = []
    #创建连接对象
    ssh = paramiko.SSHClient()
    #设置客户端登录验证方式
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #连接服务器信息
    ssh.connect(host,port,username,password)
    for _cmd in cmds:
        #操作命令
        stdin,stdout,stderr = ssh.exec_command(_cmd)
        #获取反馈信息
        _rt_list.append([_cmd,stdout.readlines(),stderr.readlines()])

    ssh.close()
    return _rt_list
#上传文件
def ssh_upload(host,username,password,files=[],port=22):
    t = paramiko.Transport(host,port)
    t.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    for _local,_remote in files:
        sftp.put(_local,_remote)
    t.close()

if __name__ == '__main__':
    host = '140.143.206.70'
    port = 22
    username = 'root'
    # password = 'Jsyd@2017!^'
    password = getpass.getpass('Please input password:')
    cmds = ["ps -ef|grep python|grep lxj|awk '{print $2}'|xargs kill -9",'nohup python3 /tmp/lxj.py >/dev/null 2>&1 &']
    files = [('test2.py','/tmp/lxj.py')]
    ssh_upload(host,username,password,files,port)
    _rt_list = ssh_excute(host,username,password,cmds,port)
    for _cmd,_out,_err in _rt_list:
        print(_cmd,_out,_err)