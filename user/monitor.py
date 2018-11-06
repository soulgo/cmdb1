#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 18:00
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : monitor.py
# @Software: PyCharm
from user.dbutils import MySqlConnection
from user.emailutils import sendMail
from user.gconf import ALARN_RECIVERS
import logging
CNT= 3
CPU_PERCENT = 6
RAM_PERCENT = 28
logger = logging.getLogger(__name__)

def has_alarm(ip):
    _sql = 'select cpu,ram from performs where ip = %s order by time desc limit %s'
    _args = (ip,CNT)
    _rt_cnt,_rt_list = MySqlConnection.execute_sql(_sql,_args)
    _cpu_alarm = True
    _ram_alarm = True
    print(_rt_list)
    for _cpu,_ram in _rt_list:
        if _cpu < CPU_PERCENT:
            _cpu_alarm = False
            print(_cpu)
        if _ram < RAM_PERCENT:
            _ram_alarm = False

    return _cpu_alarm,_ram_alarm

def monitor():
    _ip_list = ['140.143.206.70']
    _title = 'CPU内存告警'
    for _ip in _ip_list:
        _cpu_alarm,_ram_alarm = has_alarm(_ip)
        print(_cpu_alarm,_ram_alarm)
        _content_list = ['主机{ip}告警'.format(ip=_ip)]
        if _cpu_alarm:
            _content_list.append('CPU连续{cnt}次超过{persent}%'.format(cnt=CNT,persent=CPU_PERCENT))
        if _ram_alarm:
            _content_list.append('内存连续{cnt}次超过{persent}%'.format(cnt=CNT, persent=RAM_PERCENT))
        print(_content_list)
        sendMail(ALARN_RECIVERS,_title,','.join(_content_list))
        logger.info('send main to:%s,title:%s,msg:%s',ALARN_RECIVERS,_title,','.join(_content_list))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(name)s [%(lineno)d] %(levelname)s:%(message)s",
                        filename="monitor.log")
    monitor()