# encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,flash,session
import os
from functools import wraps
# from Practise.cmdb.user import log2db,loganalysisdb,asset
# from Practise.cmdb.user import userdb as user
import time
import json


from user import app,gconf
from user import models
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
    # _user = user.get_user(uid)
    _user = models.User.get_list(uid)
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
    # rt_list = loganalysisdb.get_topn(topn=topn)
    # rt_list = models.AccessLog.get_list(topn=topn)
    # return render_template('logs.html', rt_list=rt_list, title='Access Top Log')
    # code_list = models.AccessLog.log_code_list()
    # print('++++++++++++++++++')
    # print(code_list)
    # return render_template('logs.html', rt_list=models.AccessLog.get_list(topn=topn),code_list=json.dumps(code_list))
    return render_template('logs.html', rt_list=models.AccessLog.get_list(topn=topn))

@app.route('/uploadlogs/', methods=['POST'])
def uploadlogs():
    _file = request.files.get('logfile')
    if _file:
        _filepath = 'user/temp/%s' % time.time()
        _file.save(_filepath)
        # log2db.log2db(_filepath)
        models.AccessLog.log2db(_filepath)
    return redirect('/logs/')

################################资产列表
'''资产列表显示'''
@app.route('/assets/')
@login_required
def assets():
    #获取所有用户的信息
    _assets = models.Asset.get_list()
    _idcs = models.IDC.get_list_dict()
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
    _is_ok, _errors = models.Asset.validate_add(request.form)
    if _is_ok:
        models.Asset.add(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : '添加成功'})

# 修改资产其实也就是更新资产
@app.route('/asset/modify/')
@login_required
def modify_asset():
    _id = request.args.get('id', '')
    _asset = models.Asset.get_by_key(_id)
    return render_template('asset_modify.html', asset=models.Asset.get_by_key(_id), idcs=models.IDC.get_list())

# 更新资产
@app.route('/asset/update/', methods=['POST'])
@login_required
def update_asset():
    print(request.form)
    _is_ok, _errors = models.Asset.validate_update(request.form)
    if _is_ok:
        print('++++++++++++++')
        models.Asset.update(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : '更新成功'})

# 删除资产
@app.route('/asset/delete/')
@login_required
def delete_asset():
    _id = request.args.get('id', '')
    models.Asset.delete(_id)
    return redirect('/assets/')

@app.route('/asset/perform/')
@login_required
def perform_asset():
    _id = request.args.get('id', '')
    _asset = models.Asset.get_by_key(_id)
    datetime_list, cpu_list, ram_list = models.Performs.get_list(_asset['ip'])
    # datetime_list = ['2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50','2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50']
    # cpu_list = [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
    # ram_list = [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    return render_template('asset_perform.html', datetime_list=json.dumps(datetime_list),
                                                    cpu_list=json.dumps(cpu_list),
                                                    ram_list=json.dumps(ram_list))

@app.route('/asset/cmd/')
@login_required
def cmd_asset():
    _id = request.args.get('id', '')
    return render_template('asset_cmd.html', aid=_id)

@app.route('/asset/cmd_execute/', methods=['POST'])
@login_required
def cmd_execute_asset():
    _is_ok, _errors = models.Command.validate(request.form)
    _success = ''
    if _is_ok:
        _success = models.Command.execute(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : _success})

@app.route('/performs/', methods=['POST'])
def performs():
    # 判断请求头里带的app_key和app_secret
    _app_key = request.headers.get('app_key','')
    _app_secret = request.headers.get('app_secret','')
    if _app_key != gconf.APP_KEY or _app_secret != gconf.APP_SECRET:
        return json.dumps({'code':400,'text':'key or secret error'})
    #获取json数据
    # models.Performs.add(request.json)
    models.Performs.add(request.get_json())
    #0.10 request.get_json()
    return json.dumps({'code' : 200, 'text' : 'success'})

