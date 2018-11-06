# encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,flash,session
import os
from functools import wraps
from Practise.cmdb.user import log2db,loganalysisdb,asset
from Practise.cmdb.user import userdb as user
import time
import json


from Practise.cmdb.user import app
from Practise.cmdb.user import models
'''session装饰器'''
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user') is None:
            return redirect('/')

        rt = func(*args,**kwargs)
        return rt
    return wrapper

'''打开用户界面'''
@app.route('/')
def index():
    return render_template('login.html')

'''用户登录信息检查'''
@app.route('/login/',methods=['POST','GET'])
def login():
    #在flask中，get获取参数用form
    #判断是GET请求还是POST请求
    params = request.args if request.method == 'GET' else request.form
    username = params.get('username','')
    password = params.get('password','')
    _user = models.User.validate_login(username,password)
    if _user:
        session['user'] = _user
        return redirect('/users/')
    else:
        return render_template('login.html',username=username,error = '用户名或密码错误')
    return ''
    '''
    if user.validate_login(username,password):
        session['user'] = {'username':username}
        return redirect('/users/')
    else:
        return render_template('login.html',username=username,error = '用户名或密码错误')
    return ''
    '''

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect('/')

'''用户列表显示'''
@app.route('/users/')
@login_required
def users():
    #获取所有用户的信息
    # _users = user.get_users()
    return render_template('users.html',users=models.User.get_list())

'''跳转到新建用户信息输入的页面'''
@app.route('/user/create/')
@login_required
def create_user():
    return render_template('user_create.html')

'''存储新建用户的信息'''
@app.route('/user/add/',methods=['POST'])
# @login_required
def add_user():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    age = request.form.get('age', '')
    img = request.files.get('img')
    if img:
        print(img.filename)
        img.save(img.filename)
    #############实例化
    '''
    _user = models.User(id=None, username=username, password=password, age=age)
    _is_ok, _error = _user.validate_add2()
    if _is_ok:
        _user.save()
        '''
    #############面向对象

    #检查用户信息
    _is_ok, _error = models.User.validate_add(username, password, age)
    if _is_ok:
        models.User.add_user(username,password,age)
    return json.dumps(({'is_ok':_is_ok,'error':_error}))

    #####################面向过程的代码
    '''
    #检查用户信息
    _is_ok, _error = user.validate_add_user(username, password, age)
    if _is_ok:
        user.add_user(username,password,age)
    return json.dumps(({'is_ok':_is_ok,'error':_error}))
    '''
    '''
    #下面的是第一个按钮的添加
    if _is_ok:
        user.add_user(username, password, age)      #检查ok，添加用户信息
        flash('新增用户信息成功')
        return redirect(url_for('users', msg='create_user'))                  #跳转到用户列表url_for
    else:
        #跳转到用户新建页面，回显错误信息&用户信息
        return render_template('user_create.html',error=_error, username=username,password=password, age=age)
    '''

'''打开用户信息修改页面'''
@app.route('/user/modify/')
@login_required
def modify_user():
    uid = request.args.get('id', '')
    _user = user.get_user(uid)
    _error = ''
    _uid = ''
    _username = ''
    _password = ''
    _age = ''
    if _user is None:
        _error = '用户信息不存在modify'
    else:
        _uid = _user.get('id')
        _username = _user.get('username')
        _password = _user.get('password')
        _age = _user.get('age')

    return render_template('user_modify.html', error=_error, password=_password, age=_age, username=_username, uid=_uid)

'''更新用户信息：保存修改用户数据'''
@app.route('/user/update/',methods=['POST'])
@login_required
def update_user():
    #根据POST信息获取用户信息
    uid = request.form.get('id', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    age = request.form.get('age', '')
    #检查用户信息
    _is_ok, _error =models.User.validate_update_user(uid,username, password, age)
    if _is_ok:
        models.User.update_user(uid,username, password, age)
        return redirect('/users/')
    else:
        return render_template('user_modify.html', error=_error, username=username, password=password, age=age,uid=uid)
    ###########下面的是用面向过程写的
'''
    #检查用户信息
    _is_ok, _error = user.validate_update_user(uid,username, password, age)
    if _is_ok:
        user.update_user(uid,username, password, age)
        flash('修改用户信息成功')
        return redirect('/users/')
    else:
        return render_template('user_modify.html', error=_error, username=username, password=password, age=age,uid=uid)
'''

#更改密码
@app.route('/user/charge-password/',methods=['POST'])
def charge_user_password():
    uid = request.form.get('userid')
    manager_password = request.form.get('manager-password')
    user_password = request.form.get('user-password')
    _is_ok, _error = models.User.validate_charge_password(uid,user_password,session['user']['username'],manager_password)
    if _is_ok:
        models.User.charge_password(uid,user_password)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    ##############下面的代码是面向过程写的
    '''
    _is_ok, _error = user.validate_update_user_password(uid,user_password,session['user']['username'],manager_password)
    if _is_ok:
        user.charge_user_password(uid,user_password)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    '''
#更改年龄
@app.route('/user/updateage/',methods=['POST'])
def updateage():
    uid = request.form.get('userid')
    manager_password = request.form.get('manager-password')
    age_user = request.form.get('age-user')
    _is_ok, _error = models.User.validate_update_age(uid,session['user']['username'],manager_password,age_user)
    if _is_ok:
        models.User.charge_user_age(uid,age_user)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    ##############下面的代码是面向过程写的
    '''
    _is_ok, _error = user.validate_update_age(uid,session['user']['username'],manager_password,age_user)
    if _is_ok:
        user.charge_user_age(uid,age_user)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    '''


'''删除用户信息'''
@app.route('/user/delete/',methods=['POST'])
@login_required
def delete_user():
    uid = request.form.get('userid','')
    _is_ok, _error = models.User.delete_charge_user(uid)
    if _is_ok:
        models.User.delete_user(uid)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    ##############下面的代码是面向过程写的
    '''
    _is_ok, _error = user.delete_charge_user(uid)
    if _is_ok:
        user.delete_user(uid)
    return json.dumps({'is_ok':_is_ok,'error':_error})
    '''
    '''
    #需要把上面的method=['post']去掉
    user.delete_user(uid)
    flash('删除用户信息成功')
    return redirect('/users/')
    '''

@app.route('/logs/')
@login_required
def logs():
    #在flask中，get获取参数用args
    topn = request.args.get('topn','10')
    topn = int(topn) if topn.isdigit() else 10
    rt_list = loganalysisdb.get_topn(topn=topn)
    return render_template('logs.html', rt_list=rt_list, title='Access Top Log')

@app.route('/uploadlogs/', methods=['POST'])
def uploadlogs():
    _file = request.files.get('logfile')
    if _file:
        _filepath = 'user/temp/%s' % time.time()
        _file.save(_filepath)
        log2db.log2db(_filepath)
    return redirect('/logs/')

################################资产列表
'''资产列表显示'''
@app.route('/assets/')
@login_required
def assets():
    #获取所有用户的信息
    _assets = asset.get_list()
    _idcs = dict(asset.get_idc_list())
    return render_template('assets.html',assets=_assets, idcs=_idcs)

@app.route('/asset/create/',methods=['POST','GET'])
@login_required
def create_asset():
    _idcs = [(1, '北京-亦庄'), (2, '北京-酒仙桥'), (3, '北京-西单'), (4, '北京-东单')]
    return render_template('asset_create.html',idcs=_idcs)

#资产管理的添加
@app.route('/asset/add/',methods=['POST','GET'])
@login_required
def add_asset():
    _is_ok, _errors = asset.validate_create(request.form)
    if _is_ok:
        asset.create(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : '添加成功'})

# 修改资产其实也就是更新资产
@app.route('/asset/modify/')
@login_required
def modify_asset():
    _id = request.args.get('id', '')
    _asset = asset.get_by_id(_id)
    print(_id)
    print(_asset)
    return render_template('asset_modify.html', asset=_asset, idcs=asset.get_idc_list())

# 更新资产
@app.route('/asset/update/', methods=['POST'])
@login_required
def update_asset():
    _is_ok, _errors = asset.validate_update(request.form)
    if _is_ok:
        asset.update(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : '更新成功'})

# 删除资产
@app.route('/asset/delete/')
@login_required
def delete_asset():
    _id = request.args.get('id', '')
    asset.delete(_id)
    return redirect('/assets/')