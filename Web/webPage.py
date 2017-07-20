# -*- coding: utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import web
import sqlite3
from integration import getRank
import codecs
import time
import re
urls = (
    '/', 'hello',
)
def creatTable(conn):
    conn.execute(
        '''
        create table users
        (
        id INT PRIMARY KEY NOT NULL,
        mail TEXT NOT NULL
        )
        ''')
    conn.execute('''
    create table keywords
    (
    id int primary key not null,
    word text not null,
    mails text not null
    )
    ''')

def SaveMail(conn,keywords,mail):

    if not keywords or not mail:
        return False
    format_mail = re.compile(r'^[\w.]+@[\w]+.com$')
    if not format_mail.match(mail):
        print(u'邮箱格式错误')
        return False
    print(u"正在添加")
    result = conn.execute('''
    select mails from keywords where word = '%s'
    '''%keywords).fetchone()
    if result:
        result = result[0]
        if result.find(mail)!=-1:
            print(u'已经订阅')
            return 0
        else:
            result+=';'+mail
            conn.execute('''
            update keywords set mails = '%s' where word = '%s'
            '''%(result,keywords))
    else:
        with codecs.open('C:/keywords.txt','a','utf-8') as f:
            f.write(keywords+'\n')
        id = conn.execute('''
        select count(id) from keywords
        ''').fetchone()[0]
        conn.execute('''
        insert into keywords (id,word,mails) values(%s,'%s','%s')
        '''%(id,keywords,mail))
    user = conn.execute('''
    select id from users where mail = '%s'
    '''%mail).fetchone()
    if user:
        user = user[0]
        id = conn.execute('''
        select count(id) from %s
        '''%('mail'+str(user))).fetchone()[0]
        conn.execute('''
        insert into %s (id,keywords) values (%s,'%s')
        '''%(('mail'+str(user)),id,keywords))
    else:
        id = conn.execute('''
        select count(id) from users
        ''').fetchone()[0]
        #mail_ = u'rsearch'+mail.replace(u'@','_')
        conn.execute('''
    create table %s (
    id INT PRIMARY KEY NOT NULL,
    keywords TEXT NOT NULL
    )
        '''%('mail'+str(id)))
        conn.execute('''
        insert into %s (id,keywords) values (%s,'%s')
        '''%(('mail'+str(id)),0,keywords))
        conn.execute('''
        insert into users (id,mail) values (%s,'%s')
        '''%(id,mail))
    conn.commit()
red = web.template.render('template/')
def getInf(conn,mail):
    user = conn.execute('''
       select id from users where mail = '%s'
       ''' % mail).fetchone()
    if user:
        user = user[0]
        return conn.execute('''
        select * from %s
        '''%('mail'+str(user))).fetchall()

    else:
        return []
def getAllInf(conn):
    mails = conn.execute('''
select mail from users
''').fetchall()
    count = conn.execute('''
select count(id) from users''').fetchone()[0]
    userlist = []
    for i in range(0,count):
        userlist.append(conn.execute('''select * from %s
        '''%('mail'+str(i))).fetchall())
    return mails,userlist
    
    
class hello:
    def GET(self):
        user_agent = web.ctx.env.get("HTTP_USER_AGENT");
        if isinstance(user_agent,str):
            index = user_agent.lower().find("mobile") != -1;
        else:index=False;
        return red.index(index)
    def POST(self):
        data2=''
        data3=''
        user_agent = web.ctx.env.get("HTTP_USER_AGENT");
        if isinstance(user_agent,str):
            index = user_agent.lower().find("mobile") != -1;
        else:index=False;
        winput = web.input();
        #data = winput['title']
        if 'keywords' in winput:
            data2 = winput['keywords'] 
            print(data2)
        if 'mail' in winput:
            data3 = winput['mail']
            print(data3)
        mconn = sqlite3.connect('C:/MailRemind.db',cached_statements=False)

            
        while True:
            try:
                SaveMail(mconn,data2,data3)
                break
            except Exception as e:
                print(e,u'添加失败')
                time.sleep(2)
                print(u'重新添加')
        mconn.close()
        if 'selectt' not in winput and 'title' not in winput:
            return red.index(index)
        def forum(data):
            if not data:
                return red.index(index)
            
        #print('start connect:')

        #print('down')
            with open('C:/locked','r') as f:
                abc = f.read()
        #result = getRank.getRank(data,conn)
            if abc == '1':
                print('goto copied database')
            #return red.index()
                conn1 = sqlite3.connect('C:/SearchData(1).db',check_same_thread = False)
                result = getRank.getRank(data,conn1)
                conn1.close()
                return red.update(data,result,index)
            #print(result)
            conn = sqlite3.connect('C:/SearchData(0).db', check_same_thread=False)
            result = getRank.getRank(data,conn)
            conn.close()
            return red.main(data,result,index)
        def select(data):
            if data == u'跑酷':
                return red.tracer(index)
            mconn = sqlite3.connect('C:/MailRemind.db',cached_statements=False)
            
            if data == u'all':
                #print(len(getAllInf(mconn)))
                temp = getAllInf(mconn)
                mconn.close()
                return red.allinf(data,temp,index)
            temp = getInf(mconn,data)
            mconn.close()
            return red.inf(data,temp,index)

        if not winput["selectt"]:
            return forum(winput["title"])
        else:
            
            return select(winput["selectt"])



def run():
    #conn = sqlite3.connect('D:/SearchData(0).db', check_same_thread=False)
    app = web.application(urls, globals())
    app.run()
if __name__ == '__main__':
    #conn = sqlite3.connect('C:/MailRemind.db', check_same_thread=False)
	#conn = sqlite3
    #creatTable(conn)
    run()
