#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 14:14
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : email.py
# @Software: PyCharm


from user.gconf import *
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendMail(to_list,subject, content):
    try:
        """发送邮件"""
        _msg = MIMEText(content,'html','utf-8')
        _msg["Subject"] = Header(subject,'utf-8')
        _msg["From"] = SMTP_USER
        to_addrs = to_list.split(',')
        _msg["To"] = ';'.join(to_addrs)
        _server = smtplib.SMTP_SSL(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        _server.login(SMTP_USER, SMTP_PWD)
        _server.sendmail(SMTP_USER, to_addrs, _msg.as_string()) #from,to,msg
        _server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败~~" + e.message)

if __name__ == '__main__':
    sendMail('luojunquan_gz@139.com,1406221797@qq.com','告警邮件9','<html><h1>不忘初心，不负本心！</h1></html>')







