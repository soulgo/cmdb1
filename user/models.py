#encoding: utf-8

from utils.dbutils import MySqlConnection
from utils import ssh, utils
import time

class DbBase(object):
    table = 'table'
    key = 'id'
    columns_select = []
    columns_add = []
    columns_update = []
    sql_select_by_key = 'SELECT {columns} FROM {table} WHERE {key}=%s'
    sql_select = 'SELECT {columns} FROM {table} WHERE 1=1'
    sql_add = 'INSERT INTO {table}({columns}) VALUES({values})'
    sql_update = 'UPDATE {table} SET {values} WHERE {key}=%s'
    sql_delete = 'DELETE FROM {table} WHERE {key}=%s'

    @classmethod
    def create_object(cls, req):
        return req

    @classmethod
    def execute_sql(cls, sql, args=(), fetch=True):
        return MySqlConnection.execute_sql(sql, args, fetch)

    @classmethod
    def get_by_key(cls, value, key=None):
        key = cls.key if key is None else key
        wheres = [(key, value)]
        _rt_list = cls.get_list(wheres)
        return None if len(_rt_list) == 0 else _rt_list[0]

    @classmethod
    def get_list(cls, wheres=[]):
        _sql = cls.sql_select.format(columns=','.join(cls.columns_select), table=cls.table)
        _args = []
        for _key, _value in wheres:
            _sql += ' AND {key} = %s'.format(key=_key)
            _args.append(_value)

        _count, _rt_list = cls.execute_sql(_sql, _args)
        return [cls.create_object(dict(zip(cls.columns_select, _line))) for _line in _rt_list]

    @classmethod
    def add(cls, req):
        _args = []
        for _column in cls.columns_add:
            _args.append(req.get(_column, ''))
        _sql = cls.sql_add.format(table=cls.table, columns=','.join(cls.columns_add), values=','.join(['%s'] * len(cls.columns_add)))
        cls.execute_sql(_sql, _args, False)

    @classmethod
    def update(cls, req):
        _values = []
        _args = []
        for _column in cls.columns_update:
            _values.append('{column}=%s'.format(column=_column))
            _args.append(req.get(_column, ''))
        _args.append(req.get(cls.key, ''))

        _sql = cls.sql_update.format(table=cls.table, values=','.join(_values), key=cls.key)
        cls.execute_sql(_sql, _args, False)

    @classmethod
    def delete(cls, req):
        _sql = cls.sql_delete.format(table=cls.table, key=cls.key)
        _args = (req.get(cls.key, ''),)
        cls.execute_sql(_sql, _args, False)

class User(DbBase):
    table = 'user'
    key = 'id'
    columns_select = ['id', 'username', 'password', 'age']
    columns_add = ['username', 'password', 'age']
    columns_update = ['age']

    @classmethod
    def validate_login(cls, username, password):
        _columns = ('id', 'username')
        _sql = 'select id,username from user where username=%s and password=%s'
        _count, _rt_list = MySqlConnection.execute_sql(_sql, (username, utils.md5_str(password)))
        return dict(zip(_columns, _rt_list[0])) if _count != 0 else None

    @classmethod
    def validate_add(cls, username, password, age):
        if username.strip() == '':
            return False, u'用户名不能为空'

        #检查用户名是否重复
        if cls.get_by_key(username, 'username'):
            return False, u'用户名已存在'

        #密码要求长度必须大于等于6
        if len(password) < 6:
            return False, u'密码必须大于等于6'

        if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
            return False, u'年龄必须是0到100的数字'

        return True, ''

    @classmethod
    def validate_update(cls, uid, username, password, age):
        if cls.get_by_key(uid) is None:
            return False, u'用户信息不存在'


        if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
            return False, u'年龄必须是0到100的数字'

        return True, ''

    @classmethod
    def validate_charge_password(cls, uid, upassword, musername, mpassword):
        #检查管理员密码是否正确
        if not cls.validate_login(musername, mpassword):
            return False, '管理员密码错误'

        if cls.get_by_key(uid) is None:
            return False, u'用户信息不存在'

        #密码要求长度必须大于等于6
        if len(upassword) < 6:
            return False, u'密码必须大于等于6'

        return True, ''

    @classmethod
    def charge_password(cls, uid, upassword):
        _sql = 'update user set password=%s where id=%s'
        _args = (utils.md5_str(upassword), uid)
        cls.execute_sql(_sql, _args, False)


class IDC(object):

    @classmethod
    def get_list(cls):
        return [(1, '北京-亦庄'), (2, '北京-酒仙桥'), (3, '北京-西单'), (4, '北京-东单')]

    @classmethod
    def get_list_dict(cls):
        return dict(cls.get_list())


class Asset(DbBase):
    table = 'assets'
    key = 'id'
    columns_select = [
                        'id', 'sn', 'ip', 'hostname', 'os',
                        'cpu', 'ram', 'disk',
                        'idc_id', 'admin', 'business',
                        'purchase_date', 'warranty',
                        'vendor', 'model'
                    ]

    columns_add = [
                    'sn', 'ip', 'hostname', 'os',
                    'cpu', 'ram', 'disk',
                    'idc_id', 'admin', 'business',
                    'purchase_date', 'warranty',
                    'vendor', 'model'
                    ]
    columns_update = [
                        'sn', 'ip', 'hostname', 'os',
                        'cpu', 'ram', 'disk',
                        'idc_id', 'admin', 'business',
                        'purchase_date', 'warranty',
                        'vendor', 'model'
                    ]

    sql_delete = 'UPDATE FROM {table} SET status=1 WHERE {key}=%s'

    @classmethod
    def get_list(cls, wheres=[]):
        wheres.append(('status', 0))
        return super(Asset, cls).get_list(wheres)

    @classmethod
    def validate_add(cls, req):
        _is_ok = True
        _errors = {}

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

        if req.get('idc_id') not in [str(_value[0]) for _value in IDC.get_list()]:
            _is_ok = False
            _errors['idc'] = '机房选择不正确'

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

        if not req.get('purchase_date', ''):
            _is_ok = False
            _errors['purchase_date'] = '采购日期不同为空'

        return _is_ok, _errors

    @classmethod
    def validate_update(cls, req):
        return True, {}

    @classmethod
    def delete(cls, id):
        _sql = 'UPDATE assets SET status=1 WHERE id=%s'
        _args = (id, )
        MySqlConnection.execute_sql(_sql, _args, False)


class AccessLog(object):

    @classmethod
    def get_list(cls, topn=10):
        _sql = 'select url,ip,code,count(*) as cnt from accesslog group by url,ip,code order by cnt desc limit %s'
        _args = (topn, )
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

    # @classmethod
    # def log_code_list(cls):
    #     _sql = 'select code,count(code) from accesslog group by code;'
    #     print(_sql)
    #     _sql_count, _rt_list = MySqlConnection.execute_sql(_sql)
    #     _code_list = []
    #     print(_sql_count,_rt_list)
    #     all_code = 0
    #     if _sql_count != 0:
    #         for _code, _nums in _rt_list:
    #             all_code += _nums
    #         for _code, _nums in _rt_list:
    #             rt = {}
    #             rt['name'] = _code
    #             rt['y'] = round(_nums / all_code, 2)
    #             _code_list.append(rt)
    #         return _code_list
    #     return []

class Performs(object):

    @classmethod
    def add(cls, req):
        _ip = req.get('ip')
        _cpu = req.get('cpu')
        _ram = req.get('ram')
        _time = req.get('time')
        _sql = 'insert into performs(ip, cpu, ram, time)values(%s, %s, %s, %s);'
        MySqlConnection.execute_sql(_sql, (_ip, _cpu, _ram, _time), False)

    @classmethod
    def get_list(cls, ip):
        _sql = 'SELECT cpu, ram, time FROM performs WHERE ip=%s and time>=%s order by time asc'
        _args = (ip, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 60 * 60)))
        _count, _rt_list = MySqlConnection.execute_sql(_sql, _args)
        datetime_list = []
        cpu_list = []
        ram_list = []
        for _cpu, _ram, _time in _rt_list:
            cpu_list.append(_cpu)
            ram_list.append(_ram)
            datetime_list.append(_time.strftime('%H:%M:%S'))

        return datetime_list, cpu_list, ram_list


class Command(object):

    @classmethod
    def validate(cls, req):
        return True, {}

    @classmethod
    def execute(cls, req):
        _id = req.get('id', '')
        _username = req.get('username', '')
        _password = req.get('password', '')
        _cmds = req.get('cmds', '').splitlines()
        _asset = Asset.get_by_key(_id)
        _result = ssh.ssh_excute(_asset['ip'], _username, _password, _cmds)
        _echos = []
        for _cmd, _outs, _errs in _result:
            _echos.append(_cmd)
            _echos.append(''.join(_outs))
        return '\n'.join(_echos)

class Accesslog2(object):
    @classmethod
    def get_status_distribution(cls):
        _sql = 'select status,count(*) from accesslog2 group by status;'
        _rt_cnt,_rt_list = MySqlConnection.execute_sql(_sql)
        '_rt_list = ((200, 578), (304, 190), (404, 32))'
        _legends = []
        _datas = []
        _legends = [_node[0] for _node in _rt_list]
        _datas = [dict(zip(("name","value"),_node)) for _node in _rt_list]
        # 上面两行相当于下面三行
        '''
        for _status,_cnt in _rt_list:
            _legends.append(_status)
            _datas.append({"name":_status,"value":_cnt})
        '''
        return _legends,_datas

    @classmethod
    def get_time_status_stack(cls):
        _sql = "select DATE_FORMAT(logtime, '%%Y-%%m-%%d %%H:00:00') as ltime, status, count(*) from accesslog2 where logtime >= %s group by ltime, status;"
        _lasttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 12 * 60 * 60))
        _lasttime = '2014-08-23 00:00:00'
        _rt_cnt, _rt_list = MySqlConnection.execute_sql(_sql, (_lasttime,))
        _legends = []
        _xaxis = []
        _datas = []

        _temp_dict = {}
        for _ltime, _status, _cnt in _rt_list:
            if _status not in _legends:
                # 将int类型转换为字符串类型，加上双引号，不然页面上没法显示
                _status = "%d" % _status
                _legends.append(_status)
            if _ltime not in _xaxis:
                _xaxis.append(_ltime)
            _temp_dict.setdefault(_status, {})
            _temp_dict[_status][_ltime] = _cnt

        for _status, _stat in _temp_dict.items():
            _node = {
                "name": _status,
                "type": 'bar',
                "stack": 'time_status_stack',
                "data": []
            }
            for _ltime in _xaxis:
                _cnt = _stat.get(_ltime, 0)
                _node['data'].append(_cnt)

            _datas.append(_node)
        return _legends, _xaxis, _datas
