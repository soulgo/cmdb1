#encoding:utf-8
from Practise.cmdb.user import dbutils

def log2db(logfile):
    dbutils.execute_commit_sql('DELETE FROM accesslog;')
    fhandler = open(logfile, 'r')
    _sql = 'insert into accesslog(url,ip,code) values (%s, %s, %s)'
    rt_list = []
    # 统计
    while True:
        line = fhandler.readline()
        if line == '':
            break

        nodes = line.split()
        rt_list.append((nodes[6],nodes[0], nodes[8]))

    fhandler.close()
    dbutils.bulker_commit_sql(_sql,rt_list)

if __name__ == '__main__':
    logfile = 'nginx.log'

    log2db(logfile)