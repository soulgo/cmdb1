#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 10:09
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : utils.py
# @Software: PyCharm
import hashlib
def md5_str(value):
    _md5 = hashlib.md5()
    _md5.update(value.encode('utf-8'))
    return _md5.hexdigest()

if __name__ == '__main__':
    print(md5_str('123'))