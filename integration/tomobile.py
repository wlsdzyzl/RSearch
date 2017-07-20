# -*- coding:utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import sqlite3

def tomobile(conn,num):
    for i in range(1,num+1):
        try:
            abc = conn.execute('''
    select URL from URLS where ID = %s
    '''%i).fetchone()[0]
            abc = abc.replace('http://rs.xidian.edu.cn','http://bbs.rs.xidian.me')+'&mobile=2'
        #print(abc)
            conn.execute('''
        update URLS set URL = '%s' where ID = %s
        '''%(abc,i))
            print('update %s'%i)
        except Exception as e:
            print(i)

if __name__ == '__main__':
    conn = sqlite3.connect('C:\SearchData(0).db',check_same_thread=False)
    print('down')
    #print(conn.execute('select count(ID) from URLS').fetchone()[0])

    tomobile(conn,523888)
    conn.commit()

