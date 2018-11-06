#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 11:13
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : test2.py
# @Software: PyCharm
'''
import time
if __name__ == '__main__':
    while True:
        print(time.time())
        time.sleep(5)
'''
from pyquery import PyQuery as pq
input_ip = input("请输入查询的IP：")
txt_html = pq('http://ip.tool.chinaz.com/' + input_ip)
ip_list = txt_html('.IcpMain02').find('.bor-b1s').find('span')
_ip = '域名：' + ip_list.text().split(' ')[0]
_math_address = '数字地址：' + ip_list.text().split(' ')[2]
_ip_physical_location = 'IP的物理位置：' + ip_list.text().split(' ')[3] + ip_list.text().split(' ')[4]
print(_ip)
print(_math_address)
print(_ip_physical_location)