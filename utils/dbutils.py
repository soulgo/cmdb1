#encoding: utf-8
from configs import gconf
import pymysql

class MySqlConnection(object):
    def __init__(self,host,port,user,passwd,db,charset='utf-8'):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db = db
        self.__charset = charset
        self.__conn = None
        self.__cur = None
        self.__connect()

    def __connect(self):
        try:
            self.__conn = pymysql.connect(host=self.__host,port=self.__port,\
                            user=self.__user,passwd=self.__passwd,\
                            db=self.__db,charset=self.__charset)
            self.__cur = self.__conn.cursor()
        except BaseException as e:
            print(e)

    def execute(self,sql,args=()):
        try:
            _cnt = 0
            if self.__cur:
                _cnt = self.__cur.execute(sql,args)
            return _cnt
        except BaseException as e:
            self.__conn.rollback()

    def fetch(self,sql,args=()):
        try:
            _cnt = 0
            _rt_list = []
            _cnt  =self.execute(sql,args)
            if self.__cur:
                _rt_list = self.__cur.fetchall()
            return _cnt,_rt_list
        except BaseException as e:
            self.__conn.rollback()

    def commit(self):
        if self.__conn:
            self.__conn.commit()

    def close(self):
        self.commit()
        if self.__cur:
            self.__cur.close()
            self.__cur = None
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    @classmethod
    def execute_sql(cls,sql,args=(),fetch=True):
        _count = 0
        _rt_list = []
        _conn =  MySqlConnection(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT, \
                                 user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWD, \
                                 db=gconf.MYSQL_DB, charset=gconf.MYSQL_CHARSET)
        if fetch:
            _count,_rt_list = _conn.fetch(sql,args)
        else:
            _count = _conn.execute(sql,args)
        _conn.close()
        return _count,_rt_list



    @classmethod
    def bulker_execute_sql(cls, sql, args_list=[]):
        _count = 0
        _rt_list = []
        _conn = MySqlConnection(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT, \
                                user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWD, \
                                db=gconf.MYSQL_DB, charset=gconf.MYSQL_CHARSET)

        for _args in args_list:
            _count += _conn.execute(sql, _args)
        _conn.close()
        return _count, _rt_list

if __name__ == '__main__':
    print(MySqlConnection.execute_sql('select * from user'))

############################################################最开始的代码

# def execute_fetch_sql(sql, args=()):
#     return execute_sql(sql, args, True)
#
# def execute_commit_sql(sql, args=()):
#     return execute_sql(sql, args, False)
#
# def execute_sql(sql, args=(), fetch=True):
#     _conn = None
#     _cur = None
#     _count = 0
#     _rt_list = []
#     try:
#         _conn = pymysql.connect(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT, \
#                         user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWD, \
#                         db=gconf.MYSQL_DB, charset=gconf.MYSQL_CHARSET)
#
#         #_conn.autocommit(True)              #autocommit
#         _cur = _conn.cursor()
#         _count = _cur.execute(sql, args)
#         if fetch:
#             _rt_list = _cur.fetchall()
#         else:
#             _conn.commit()                      #commit, 和autocommit任选其一
#     except BaseException as e:
#         _conn.rollback()
#     finally:
#         if _cur:
#             _cur.close()
#         if _conn:
#             _conn.close()
#     return _count, _rt_list
#
# def bulker_commit_sql(sql, args_list=[]):
#     _conn = None
#     _cur = None
#     _count = 0
#     _rt_list = []
#     try:
#         _conn = pymysql.connect(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT, \
#                         user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWD, \
#                         db=gconf.MYSQL_DB, charset=gconf.MYSQL_CHARSET)
#
#         #_conn.autocommit(True)              #autocommit
#         _cur = _conn.cursor()
#         for _args in args_list:
#             _count += _cur.execute(sql, _args)
#         _conn.commit()                      #commit, 和autocommit任选其一
#     except BaseException as e:
#         _conn.rollback()
#     finally:
#         if _cur:
#             _cur.close()
#         if _conn:
#             _conn.close()
#
#     return _count, _rt_list