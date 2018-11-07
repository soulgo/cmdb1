#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:56
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : accesslog2db.py
# @Software: PyCharm
'''
ip查询文档geoip2：https://pypi.org/project/geoip2/
'''
from utils.dbutils import MySqlConnection
import time
import geoip2.database

if __name__ == '__main__':
    logfile = 'nginx2.log'
    MySqlConnection.execute_sql('DELETE FROM accesslog2;', (), False)
    reader = geoip2.database.Reader('D:\\python_projext\\Practise\\cmdb\\user\\static\\GeoLite2-City.mmdb')
    fhandler = open(logfile, 'r')
    rt_list = []
    # 统计
    while True:
        line = fhandler.readline()
        if line == '':
            break

        nodes = line.split()
        ip,logtime,url,status = nodes[0],nodes[3][1:],nodes[6],nodes[8]
        logtime = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(logtime,'%d/%b/%Y:%H:%M:%S'))
        try:
            # IP不在中国的不存入数据库
            response = reader.city(ip)
            if 'China' != response.country.name:
                continue
            city = response.city.names.get('zh-CN', '')
            if city == '':
                continue
            # 经度和纬度
            lat = response.location.latitude
            lng = response.location.longitude
            rt_list.append((logtime,ip,url,status,lat,lng,city))
        except BaseException as e:
            print('此IP不在China:%s' %ip)

    fhandler.close()

    _sql = 'insert into accesslog2(logtime,ip,url,status,lat,lng,city) values (%s, %s, %s, %s, %s, %s, %s)'
    MySqlConnection.bulker_execute_sql(_sql, rt_list)
