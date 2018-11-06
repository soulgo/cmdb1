#encoding:utf-8

from Practise.cmdb.user import dbutils

def get_topn(topn=5):
    _sql = 'select url,ip,code,count(*) as cnt from accesslog group by url,ip,code order by cnt desc limit %s'
    _cnt,_rt_list = dbutils.execute_fetch_sql(_sql,(topn))
    return _rt_list
