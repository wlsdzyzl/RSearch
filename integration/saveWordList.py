# -*- coding:utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from integration import giveWordId

import codecs
import sqlite3
import time
import gc
#default_encoding = 'utf-8'

wordListValue = giveWordId.wordListValue
def make_Url_list(num,conn):
    conn.execute("DROP TABLE URLS")
    #print('wocao')
    conn.execute('''
    CREATE TABLE URLS (
    ID INT PRIMARY KEY  NOT NULL,
    URL TEXT NOT NULL,
    TITLE NTEXT NOT NULL,
    TIME TEXT NOT NULL,
    CONT NTEXT NOT NULL

    )''')
    for i in range(1,num+1):
        if i %100 == 0:
            print('get %s'%i)
        with codecs.open('D:/TheUrlWeGot/'+str(i)+'.txt','r','utf-8') as f:

            url = f.readline()
            #f.readline()
            title = f.readline()
            #print(title)
            time = f.readline()

            url = url.replace(u'\ufeff','')
            url = url[:-2]
            title = title[:-2]
            #print(i,url)
            time = time[:-2]
            if not time:
                continue
            text = f.read()

            title = title.replace('\'','')
            title = title.replace('\"','')
            title = title.replace('\\','')
            title = title.replace('\0','')
            text = text.replace('\'','')
            text = text.replace('\\','')
            text = text.replace('\0','')
            text = text.replace('\"','')
            text = text.replace('\n','')
            #print(text)
            #if i == 3247:
            #print(time)
            #print('text:'+text+'time:'+time+'title'+title+''+url)

            #text.replace('/','')
            #print(text)
            conn.execute('''
            INSERT INTO URLS (ID,URL,TITLE,TIME,CONT)
            VALUES(%s,'%s','%s','%s','%s')
            '''%(i,url,title,time,text))
            #print(url)
            #print('%s urls are already inserted'%i)
        #print(conn.execute('select url from URLS where ID = 12').fetchone())
def createWordList(conn):
    conn.execute("DROP TABLE WORDID")
    conn.execute('''
            CREATE TABLE WORDID (
            ID INT PRIMARY KEY  NOT NULL,
            WORD NTEXT NOT NULL,
            URLINF TEXT NOT NULL
            )

            ''' )

def saveWordList(wordlist,conn,offset):
    #n = 0
    #dictweNeed = {}
    n = 0
    num = 0
    for i in wordlist.dict:
        num+=1
            #print('save one time')
        #i = i.encode('utf-8')
        if i == u'\'' or i == u' ' or i == u'\"' or i == u'\\' or i == u'\0':
            continue
        result = conn.execute('''
        SELECT URLINF FROM WORDID WHERE WORD = '%s'
        '''%i).fetchone()
        #i = i.decode('utf-8')
        if result:#如果这个字已经在数据库中，我们就更新他的url的信息
            result = str(result[0])
            #print(result)
            abc = wordListValue()
            abc.getValue(result)
            for j in wordlist.dict[i].list:
                if j in abc.list:
                    abc.list[j][0]+=wordlist.dict[i].list[j][0]
                    abc.list[j][1]+=wordlist.dict[i].list[j][1]
                else :
                    abc.list[j] = wordlist.dict[i].list[j]
            while True:
                try:
                    conn.execute('''
            UPDATE WORDID SET URLINF = '%s'WHERE WORD = '%s'
            '''%(str(abc).replace('\'',''),i))
                    break
                except Exception as e:
                    print(e)
                    print(' the database is locked . connectting again...')
                    time.sleep(2)
            print('update one data(%s/%s)'%(num,wordlist.size))
        else:
            n += 1  # 新添加的数据库中文件的个数
            s = str(wordlist.dict[i])
            s = s.replace('\'', '')
            #s = s.replace(',',' ')
            while True:
                try:
                    conn.execute('''
                    INSERT INTO WORDID (ID,WORD,URLINF)
                    VALUES (%s,'%s','%s')
                    ''' % ((n+offset), i, s))
                    break
                except Exception as e:
                    print(' the database is locked . connectting again...')
                    time.sleep(2)
            print('%s datas already inserted (%s/%s) '%((n+offset),num,wordlist.size))
    return n+offset
    #print('already inserted %s files'%)

        #print(n,i)

def make_word_list(num):
    #createWordList(conn)
    begin = 1
    end = num+1
    #offset = 0
    n = 0
    while begin < end:
        n+=1
        pair = giveWordId.makefile(begin,end)
        print('get word list ,size = %s , at %s'%(pair[1].size,time.ctime()))
        wordlist = pair[1]
        #offset = saveWordList(wordlist,conn,offset)
        with codecs.open('D:/index/%s.txt'%n,'w','utf-8') as f:

            for i in wordlist.dict:
                f.write(i)
                for j in wordlist.dict[i].list:
                    f.write(' '+str(j)+' '+str(wordlist.dict[i].list[j]))
                f.write('\r\n')
        del wordlist
        gc.collect()
        begin = pair[0]
        print('already inserted %s files at %s'%((begin-1),time.ctime()))

if __name__ == '__main__':

    conn = sqlite3.connect('D:/SearchData(0).db',check_same_thread=False)

    #print('down')
    #print(u'\u0e13')
    #make_Url_list(1000, conn)
    #print(conn.execute("select * from URLS").fetchall())
    num = 523142#文件的个数
    #make_word_list(num)
    print conn.execute('select count(ID) from WORDID').fetchone()[0]
    #saveWordList(giveWordId.makeList(num), conn)
    make_Url_list(num,conn)
    #print('down')
    #make_Url_list(num,conn)
    #giveWordId.makefile(num)
    #print('urls down')
    #make_Url_list(num,conn)
    #print(giveWordId.makeList(1).size)
    #print(conn.execute('select count(ID) from WORDID').fetchone()[0])
    conn.commit()
    """conn = sqlite3.connect('D:/SearchData.db')
    print('connect to the database')
    num = 100
    #make_Url_list(num,conn)
    #print()
    saveWordList(giveWordId.makeList(num),conn)
    conn.commit()"""
    #conn.commit()
    print('down')
    #for i in conn.execute("select URL from URLS").fetchall():
       # print(i[0])
    #c = conn.execute('select URLINF from WORDID where WORD = \'%s\' '%'科学').fetchone()



