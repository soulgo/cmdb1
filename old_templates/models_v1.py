#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/27 18:28
# @Author  : 罗小贱
# @email: ljq906416@gmail.com
# @File    : models.py
# @Software: PyCharm
from utils.dbutils import MySqlConnection

class User(object):
    def __init__(self,id,username,password,age):
        self.id = id
        self.username = username
        self.password = password
        self.age = age

    '''验证用户名，密码是否正确
    返回值: True/False
    '''
    @classmethod
    def validate_login(cls,username, password):
        _columns = ('id','username')
        _sql = "select * from user where username=%s and password=md5(%s)"
        _count, rt_list = MySqlConnection.execute_sql(_sql, (username, password))
        print(rt_list)
        return dict(zip(_columns,rt_list[0])) if _count != 0 else None

    '''获取所有用户的信息
    返回值: [
                {"username" : "kk", "password" : "123456", "age" : 29},
                {"username" : "woniu", "password" : "abcdef", "age" : 28}
            ]
    '''
    @classmethod
    def get_list(cls,wheres=[]):
        _columns = ('id','username','password','age')
        _sql = 'select * from user where 1=1'
        _args = []
        for _key, _value in wheres:
            _sql += ' AND {key} = %s'.format(key=_key)
            _args.append(_value)
        _count,_rt_list = MySqlConnection.execute_sql(_sql,_args)
        _rt = []
        return [User(**dict(zip(_columns,_line))) for _line in _rt_list]
        #上面return的一句简写为下面的代码
        '''
        for _line in _rt_list:
            _user_dict = dict(zip(_columns,_line))
            _user = User(_user_dict['id'],_user_dict['username'],_user_dict['password'],_user_dict['age'])
            _rt.append(_user)
            #上面三行代码等下下面的一行代码 
            # _rt.append(dict(zip(_columns,_line)))
        return _rt
        '''

    '''添加用户信息'''
    @classmethod
    def validate_add(cls,username, password, age):
        if username.strip() == '':
            return False, u'用户名不能为空'
        # 检查用户名是否重复
        # _users = get_users()
        if cls.get_user_by_name(username):
            return False, u'用户名已存在'
        # 密码要求长度必须大于等于6
        if len(password) < 6:
            return False, u'密码必须大于等于6'
        if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
            return False, u'年龄必须是0到100的数字'
        return True, ''

    @classmethod
    def get_user_by_name(cls,username):
        _rt = cls.get_list([('username',username)])
        return _rt[0] if len(_rt) > 0 else None

    @classmethod
    def add_user(cls,username, password, age):
        _sql = 'insert into user(username,password,age) VALUES (%s,md5(%s),%s)'
        _args = (username, password, age)
        print(_args)
        MySqlConnection.execute_sql(_sql, _args,False)

#############实例化添加用户
    def validate_add2(self):
        if self.username.strip() == '':
            return False, u'用户名不能为空'

        #检查用户名是否重复
        if self.get_by_name(self.username):
            return False, u'用户名已存在'

        #密码要求长度必须大于等于6
        if len(self.password) < 6:
            return False, u'密码必须大于等于6'

        if not str(self.age).isdigit() or int(self.age) <= 0 or int(self.age) > 100:
            return False, u'年龄必须是0到100的数字'

        return True, ''

    def save(self):
        _sql = 'insert into user(username, password, age) values(%s, md5(%s), %s)'
        _args = (self.username, self.password, self.age)
        MySqlConnection.execute_sql(_sql, _args, False)
##############################

    '''更新用户信息'''
    @classmethod
    def validate_update_user(cls,uid, username, password, age):
        if username.strip() == '':
            return False,u'用户名不能为空'
        if cls.get_user_by_name(uid) is None:
            return False, u'用户信息不存在'
        # 密码要求长度必须大于等于6
        if len(password) < 6:
            return False, u'密码必须大于等于6'
        if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
            return False, u'年龄必须是0到100的数字'
        return True, ''

    @classmethod
    def update_user(cls,uid, username, password, age):
        _sql = 'update user set age=%s where id=%s'
        _args = (uid,age)
        MySqlConnection.execute_sql(_sql,_args,False)

    @classmethod
    def get_by_id(cls, uid):
        _rt = cls.get_list([('id', uid)])
        return _rt[0] if len(_rt) > 0 else None

    '''更新用户密码'''
    @classmethod
    def validate_charge_password(cls,uid, upassword, musername, mpassword):
        # 检查管理员密码
        if not cls.validate_login(musername,mpassword):
            return False, '管理员密码错误'
        if cls.get_by_id(uid) is None:
            return False, u'用户信息不存在'
        # 密码要求长度必须大于等于6
        if len(upassword) < 6:
            return False, u'密码必须大于等于6'
        return True, ''

    @classmethod
    def charge_password(cls, uid, upassword):
        _sql = 'update user set password=md5(%s) where id=%s'
        _args = (upassword, uid)
        MySqlConnection.execute_sql(_sql, _args, False)

    '''修改用户年龄'''
    @classmethod
    def validate_update_age(cls,uid, musername, mpassword, mageuser):
        # 检查管理员密码
        if not cls.validate_login(musername,mpassword):
            return False, '管理员密码错误'
        if cls.get_by_id(uid) is None:
            return False, u'用户信息不存在'
        # 密码要求长度必须大于等于6
        if not str(mageuser).isdigit() or int(mageuser) <= 0 or int(mageuser) > 100:
            return False, u'年龄必须是0到100的数字'
        return True, ''

    @classmethod
    # 更改年龄
    def charge_user_age(cls,uid, age):
        _sql = 'update user set age=%s where id=%s'
        _args = (age,uid)
        MySqlConnection.execute_sql(_sql,_args)

    @classmethod
    # 删除用户
    def delete_charge_user(cls,uid):
        if cls.get_by_id(uid) is None:
            return False, u'用户信息不存在'
        return True, ''

    '''删除用户信息'''
    @classmethod
    def delete_user(cls,uid):
        _sql = "delete from user where id=%s"
        _args = (uid)
        MySqlConnection.execute_sql(_sql,_args)

class IDC(object):

    @classmethod
    def get_list(cls):
        return [(1, '北京-亦庄'), (2, '北京-酒仙桥'), (3, '北京-西单'), (4, '北京-东单')]

    @classmethod
    def get_list_dict(cls):
        return dict(cls.get_list())

class Asset(object):

    def __init__(self, sn, ip, hostname, os,
                        cpu, ram, disk,
                        idc_id, admin, business,
                        purchase_date, warranty, vendor, model, id=None, status=0):
        self.id = id
        self.sn = sn
        self.ip = ip
        self.hostname = hostname
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.idc_id = idc_id
        self.admin = admin
        self.business = business
        self.purchase_date = purchase_date
        self.warranty = warranty
        self.vendor = vendor
        self.model = model
        self.status = status

    @classmethod
    def create_object(self, obj):
        obj['purchase_date'] = obj['purchase_date'].strftime('%Y-%m-%d')
        return obj

    '''通过主键返回资产信息None/{}'''
    @classmethod
    def get_by_key(cls, value, key='id'):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
        _columns = _column.split(',')
        _sql = 'SELECT {column} FROM assets WHERE status=0 and {key}=%s'.format(column=_column, key=key)
        _args = (value,)
        _count, _rt_list = MySqlConnection.execute_sql(_sql, _args)
        return None if _count == 0 else cls.create_object(dict(zip(_columns, _rt_list[0])))

    '''返回所有资产信息'''
    @classmethod
    def get_list(cls):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
        _columns = _column.split(',')
        _sql = 'SELECT {column} FROM assets WHERE status=0'.format(column=_column)
        _count, _rt_list = MySqlConnection.execute_sql(_sql)
        return [cls.create_object(dict(zip(_columns, _line))) for _line in _rt_list]

    '''在创建资产时对输入信息进行验证True/False,error_msg{}'''
    @classmethod
    def validate_add(cls, req):
        _is_ok = True
        _errors = {}
        '''
        字符串类型: sn,ip,hostname,os,admin,business,vendor,model
        检查是否为空(不允许),最小长度,最大长度
        '''
        for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
            _value = req.get(_key, '').strip()
            if _value == '':
                _is_ok = False
                _errors[_key] = '%s不允许为空' % _key
            elif len(_value) > 64:
                _is_ok = False
                _errors[_key] = '%s不允许超过64个字符' % _key

        if cls.get_by_key(req.get('sn'), 'sn'):
            _is_ok = False
            _errors[_key] = 'sn已存在'

        '''取值选项:idc_id'''
        if req.get('idc_id') not in [str(_value[0]) for _value in IDC.get_list()]:
            _is_ok = False
            _errors['idc'] = '机房选择不正确'
        '''数字类型: cpu,ram,disk,warranty
        检查数字类型isdigit, 最大值, 最小值'''
        _rules = {
            'cpu' : {'min' : 2, 'max' : 64},
            'ram' : {'min' : 2, 'max' : 512},
            'disk' : {'min' : 2, 'max' : 2048},
            'warranty' : {'min' : 1, 'max' : 5},
        }
        for _key in 'cpu,ram,disk,warranty'.split(','):
            _value = req.get(_key, '').strip()
            if not _value.isdigit():
                _is_ok = False
                _errors[_key] = '%s不是整数' % _key
            else:
                _value = int(_value)
                _min = _rules.get(_key).get('min')
                _max = _rules.get(_key).get('max')
                if _value < _min or _value > _max:
                    _is_ok = False
                    _errors[_key] = '%s取值范围应该为%s ~ %s' % (_key, _min, _max)
        '''日期类型: purchase_date'''
        if not req.get('purchase_date', ''):
            _is_ok = False
            _errors['purchase_date'] = '采购日期不同为空'

        return _is_ok, _errors

    '''创建资产，操作数据库返回True/False'''
    @classmethod
    def add(cls, req):
        _column_str = 'sn,ip,hostname,os,admin,business,vendor,model,idc_id,cpu,ram,disk,warranty,purchase_date'
        _columns = _column_str.split(',')
        _args = []
        for _column in _columns:
            _args.append(req.get(_column, ''))

        _sql = 'INSERT INTO assets({columns}) VALUES({values})'.format(columns=_column_str, values=','.join(['%s'] * len(_columns)))
        MySqlConnection.execute_sql(_sql, _args, False)

    '''在修改资产时对输入信息进行检查True/False,error_msg{}'''
    @classmethod
    def validate_update(cls, req):
        return True, {}

    '''更新资产，操作数据库返回True/False'''
    @classmethod
    def update(cls, req):
        _column_str = 'sn,ip,hostname,os,admin,business,vendor,model,idc_id,cpu,ram,disk,warranty,purchase_date'
        _columns = _column_str.split(',')
        _values = []
        _args = []
        for _column in _columns:
            _values.append('{column}=%s'.format(column=_column))
            _args.append(req.get(_column, ''))

        _args.append(req.get('id'))

        _sql = 'UPDATE assets SET {values} WHERE id=%s'.format(values=','.join(_values))
        MySqlConnection.execute_sql(_sql, _args, False)

    '''删除资产，操作数据库返回True/False'''
    @classmethod
    def delete(cls, id):
        _sql = 'UPDATE assets SET status=1 WHERE id=%s'
        _args = (id, )
        MySqlConnection.execute_sql(_sql, _args, False)

class AccessLog(object):

    @classmethod
    def get_list(cls, topn=10):
        # _sql = 'select ip, url, code, cnt from accesslog order by cnt desc limit %s'
        _sql = 'select url,ip,code,count(*) as cnt from accesslog group by url,ip,code order by cnt desc limit %s'
        _args = (topn, )
        print(_sql,_args)
        _count, _rt_list = MySqlConnection.execute_sql(_sql, _args)
        return _rt_list


    @classmethod
    def log2db(cls, logfile):
        MySqlConnection.execute_sql('DELETE FROM accesslog;', (), False)
        fhandler = open(logfile, 'r')
        _sql = 'insert into accesslog(url,ip,code) values (%s, %s, %s)'
        rt_list = []
        # 统计
        while True:
            line = fhandler.readline()
            if line == '':
                break

            nodes = line.split()
            rt_list.append((nodes[6], nodes[0], nodes[8]))

        fhandler.close()
        MySqlConnection.bulker_execute_sql(_sql, rt_list)