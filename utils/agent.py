#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 17:51
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : agent.py
# @Software: PyCharm
import logging,time,os,requests,json,traceback

APP_KEY = 'd76e3abf3c8900db8d384a1bf902c7b8'
APP_SECRET = 'a892feff56f20341a6a70fdb0f972e3b'


logger = logging.getLogger(__name__)

SERVER_URL = 'http://140.143.206.70:8080/performs/'

def execute_cmd(cmd):
    _fh = os.popen(cmd)
    _cxt = _fh.read()
    _fh.close()
    return _cxt

def get_ip():
    # _cmd = "ifconfig eth0 | grep 'inet' | awk '{print $2}'"
    _cmd =  "curl members.3322.org/dyndns/getip"
    _cxt = execute_cmd(_cmd)
    return str(_cxt.split(':')[-1]).strip()

def collect_cpu():
    _cmd = "top -n 1 | grep Cpu | awk '{print $4}'"
    _cxt = execute_cmd(_cmd)
    return float(_cxt.split('%')[0])

def collect_ram():
    _free = "free -m | sed -n '2p' | awk '{print $3}'"
    _total = "free -m | sed -n '2p' | awk '{print $2}'"
    _cmd_free = execute_cmd(_free)
    _cmd_total = execute_cmd(_total)
    return 100 * float(_cmd_free) / float(_cmd_total)
    '''
    _fh = open('/proc/meminfo')
    _total = float(_fh.readline().split()[1])
    # _free = float(_fh.readline().split()[1])
    _fh.readline()
    _memavailable = float(_fh.readline().split()[1])
    _fh.close()
    return _memavailable / _total
    '''

def collect():
    _rt = {}
    _rt['ip'] = get_ip()
    _rt['cpu'] = collect_cpu()
    _rt['ram'] = collect_ram()
    _rt['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    return _rt

def send(msg):
    try:
        # 将app_key和app_secret加到headers
        _reponse = requests.post(SERVER_URL, data=json.dumps(msg),
                                 headers={"Content-Type":"application/json",'app_key':APP_KEY,'app_secret':APP_SECRET})
        if not _reponse.ok:
            logger.error('error send msg:%s', msg)
        else:
            _json = _reponse.json()
            print(_reponse.headers)
            if _json.get('code') != 200:
                logger.error('error send msg:%s,result:%s',msg,_json)
    except BaseException as e:
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s [%(lineno)d] %(levelname)s:%(message)s",
                    filename="agent.log")
    while True:
        try:
            _msg = collect()
            print(_msg)
            logger.debug(_msg)
            send(_msg)
            time.sleep(1200)
        except BaseException as e:
            logger.error(traceback.format_exc())
