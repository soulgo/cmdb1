#encoding: utf-8
import json
import pymysql
from Practise.cmdb.user import gconf,dbutils

'''获取所有用户的信息
返回值: [
            {"username" : "kk", "password" : "123456", "age" : 29},
            {"username" : "woniu", "password" : "abcdef", "age" : 28}
        ]
'''
def get_users(wheres=[]):
    _columns = ('id','username','password','age')
    _sql = 'select * from user where 1=1'
    _args = []
    for _key, _value in wheres:
        _sql += ' AND {key} = %s'.format(key=_key)
        _args.append(_value)
    _count,_rt_list = dbutils.execute_fetch_sql(_sql,_args)
    _rt = []
    for _line in _rt_list:
        _rt.append(dict(zip(_columns,_line)))
    return _rt


'''保存用户数据到文件中'''
def save_users(users):
    fhandler = open(gconf.USER_FILE, 'wb')
    fhandler.write(json.dumps(users).encode('utf-8'))
    fhandler.close()


'''验证用户名，密码是否正确
返回值: True/False
'''
def validate_login(username, password):
    _sql = "select * from user where username=%s and password=md5(%s)"
    _count,rt_list = dbutils.execute_fetch_sql(_sql,(username,password))
    return _count !=0

'''检查新建用户信息
返回值: True/False, 错误信息
'''
def validate_add_user(username, password, age):
    if username.strip() == '':
        return False, u'用户名不能为空'

    #检查用户名是否重复
    _users = get_users()
    for _user in _users:
        if username == _user.get('username'):
            return False, u'用户名已存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False, u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'年龄必须是0到100的数字'

    return True, ''


'''添加用户信息
'''
def add_user(username, password, age):
    _sql = 'insert into user(username,password,age) VALUES (%s,md5(%s),%s)'
    _args = (username, password, age)
    dbutils.execute_commit_sql(_sql, _args)


'''获取用户信息
'''
def get_user(uid):
    # _users = get_users()
    # for _user in _users:
    #     if _user.get('username') == username:
    #         return _user
    #
    # return None
    _rt = get_users([('id', uid)])
    return _rt[0] if len(_rt) > 0 else None

'''检查更新用户信息
返回值: True/False, 错误信息
'''

def validate_update_user(uid,username, password, age):
    if get_user(uid) is None:
        return False, u'用户信息不存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False, u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'年龄必须是0到100的数字'

    return True, ''


'''更新用户信息'''
def update_user(uid,username, password, age):
    _sql = 'update user set age=%s where id=%s'
    dbutils.execute_commit_sql(_sql, (age, uid))

'''删除用户信息'''
def delete_user(uid):
    _sql = "delete from user where id=%s"
    dbutils.execute_commit_sql(_sql,(uid))

#删除用户
def delete_charge_user(uid):
    if get_user(uid) is None:
        return False, u'用户信息不存在'
    return True,''

def validate_update_user_password(uid,upassword,musername,mpassword):
    #检查管理员密码
    if not validate_login(musername,mpassword):
        return False,'管理员密码错误'
    if get_user(uid) is None:
        return False, u'用户信息不存在'
    #密码要求长度必须大于等于6
    if len(upassword) < 6:
        return False, u'密码必须大于等于6'

    return True,''

def validate_update_age(uid,musername,mpassword,mageuser):
    #检查管理员密码
    if not validate_login(musername,mpassword):
        return False,'管理员密码错误'
    if get_user(uid) is None:
        return False, u'用户信息不存在'
    #密码要求长度必须大于等于6
    if not str(mageuser).isdigit() or int(mageuser) <= 0 or int(mageuser) > 100:
        return False, u'年龄必须是0到100的数字'
    return True,''

#更改密码
def charge_user_password(uid,upassword):
    _sql = 'update user set password=md5(%s) where id=%s'
    dbutils.execute_commit_sql(_sql,(upassword,uid))
#更改年龄
def charge_user_age(uid,age):
    _sql = 'update user set age=%s where id=%s'
    dbutils.execute_commit_sql(_sql,(age,uid))