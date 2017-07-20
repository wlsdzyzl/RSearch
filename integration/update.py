# -*- coding:utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
                    
"""邮件发送经常出错，但是不能因为邮件出错而停止搜索引擎的工作，
                         目前想到了几条解决办法，比如设定超时，或者给发邮件重新派送一个进程，下次更新时候通过主进程
                         结束该进程。最最完美的是解决邮件发送出错的bug，目前定位到是从连接到登录中间出了问题
                         ，而上面的办法也是可接受的，不过最近没有时间搞这个，所以暂时把邮件订阅功能停止"""
from Spider import TheParser,threadSpider,getViewThread,FormatUrl
import codecs
import sqlite3
import jieba
import time
import shutil
from email.mime.text import MIMEText
import smtplib
mail_user = 'rsearchws@outlook.com'
mail_pass = 'zgq19961001'
mail_host = 'smtp-mail.outlook.com'


from integration import giveWordId,saveWordList
from multiprocessing import Queue,Process,Manager
cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
         '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
         '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
weNeed = {}

for i in cookie.split(';'):
     key,value =  i.split('=',1)
     weNeed[key] = value
def sendEmail(content,to_lists,sub):
    msg = MIMEText(content,_subtype="html",_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = mail_user
    msg['To'] = to_lists
    s = smtplib.SMTP(mail_host,587)
    print(u"登录邮箱");
    s.ehlo()
    print("start tls")
    s.starttls()
    print(u"初始化完成...")
    s.login(mail_user,mail_pass)
    print(u"登录成功！")

    times = 0
    while True and times < 5:
        try:
            print(u"正在发送");
            s.sendmail(mail_user,to_lists,msg.as_string())
            break
        except Exception as e:
            print (e)
            print(u'发送失败...')
            time.sleep(2)
            times+=1
            print(u'再一次发送...')
    if times >=5:
         print(u'邮件地址不可达')
         return False
    print(u'发送成功')





def task(que,urls):
    while not que.empty():
        url = que.get()
        #print(url)
        curUrl = TheParser.TheParser(url, weNeed).getURL()
        #print('abc')
        #print(curUrl.title)
        if curUrl:
            urls.append(curUrl)

        else:
            que.put(url)
        if que.qsize()%10 == 0:
            print(str(que.qsize()) + ' remained')
def gettime(time):
    if isinstance(time,tuple):
        return 0
    time = time.encode('utf-8')
    abc = []
    n = 0
    for j in time:
        if str.isdigit(j):
            n = n * 10 + ord(j) - ord('0')
        else:
            abc.append(n)
            n = 0
    abc.append(n)
    try:

        abc = (abc[0] - 2010) * 31622400 + abc[1] * 2678400 + abc[2] * 86400 + abc[3] * 3600 + abc[4] * 60 + abc[5]
    except Exception as e:
        print(file, time)
        return 0
    return abc
def mistake(conn):
    for i in range(1152821,1152830):
        print(i)
        abc = conn.execute('''select ID from WORDID where ID = %s'''%i).fetchone()
        #print(abc)
        if abc:
            conn.execute('''delete from WORDID where ID = %s'''%i)
    conn.commit()
def addURLS(num,conn,urls):
    n = num


    with codecs.open('C:/keywords.txt','r','utf-8') as f:
        words = f.readlines()
    wordset = set(words)
    worddict = {}
    for i in urls:
        n+=1
        title = i.title
        text = ''.join(i.text)
        title = title.replace('\'','')
        title = title.replace('\"','')
        title = title.replace('\'','')
        title = title.replace('\0','')

        text = text.replace('\'','')
        text = text.replace('\"','')
        text = text.replace('\'','')
        text = text.replace('\0','')
        while True:
            try:
                conn.execute('''
        INSERT INTO URLS (ID,URL,TITLE,TIME,CONT)
        VALUES(%s,'%s','%s','%s','%s')
        ''' % (n, i.url, title, i.time, text))
                print('insert one')
                break
            except Exception as e:
                print(' the database is locked . connectting again...')
                time.sleep(2)
        for j in wordset:#得到需要发送的信息
            if title.find(j[:-1]) != -1:
                if j in worddict:
                    worddict[j].append([i.url, title, i.time, text])
                else:
                    worddict[j] = []
                    worddict[j].append([i.url, title, i.time, text])

    #print(u'更新完成开始发送邮件：')
    #getContent(worddict)
    return n
def getContent(worddict):
    mconn = sqlite3.connect('C:/MailRemind.db', cached_statements=False)
    for keyword in worddict:
        print(keyword)
		
        while True:
             
            try:
                #print(keyword)
                lists = mconn.execute('''
        select mails from keywords where word = '%s'
        '''%keyword[:-1]).fetchone()[0]
                print(u"接受方:"+lists)
                break
            except Exception as e:
                print(e)
                print(u'查询失败')
                time.sleep(2)
                print(u'再次查询')
                  
        content = u'''
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv=”Content-Type” content=”text/html; charset=utf-8″ />
        <title>$data _RSearch_论坛搜索</title>
        <style>
            .box{width:800px;height:120px;text-align:left}
            .null_er{width:100px;height:120px;}
            a:link { text-decoration: underline;

            overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;
              display:block;

            }

            .text_main {font-size:13px;}
            .green_linker {font-size:12px;color:green;}
        </style>

    </head>
	<body>

        <br/><br/><br/>
        <div style="text-align:left;border;">
            <img src="http://wx4.sinaimg.cn/mw690/e1b491c1ly1fe44ard63mj209602m0sm.jpg" width="280" height="70" title="RSearch" text-align="center">
		<div/>
            '''

        if not lists:
            return []
        for i in worddict[keyword]:
            #print(type(i),type(i[0]),type(i[1]),type(i[2]),type(i[3]))
            content+=u'''

                    <div class="box" style="text-align:left">
                    <a href= '''+i[0]+u''' target="_blank">
                       '''+i[1]+u'''</a>
                                               <a href= '''+(i[0].replace(u'http://bbs.rs.xidian.me',u'http://rs.xidian.edu.cn'))[:-9]+u'''  target=  "_blank"><font size=2 color="#4D4D4D">如果你想访问pc版，点这里！</font></a>

                        <p class="green_linker">
                            '''+i[0]+u'''
                        <font color = "#4D4D4D" > 发表于'''+str(i[2])+u'''</font>
                           </p>
                       
						<div/>'''
        content+=u'''    <p align="center"><font color="#4D4D4D" size=2 >©2017 RSearch for 西电睿思</font></p>
    </body>'''
        times = 0
        print("got content!");
        while True and times < 5:
             try:
                 sendEmail(content,lists,u'你好，你对关键词“'+keyword+u'”的订阅有更新！',s)
                 break
             except Exception as e:
                 print(u'发送失败')
                 print(e)
                 time.sleep(10)
                 times+=1
                 print(u'再次发送')
        if times == 5:
               print(u"无法送达！")
                

def addWordList(num1,num2,conn,urls):
    tlistWeNeed = []
    clistWeNeed = []
    time = []
    wordlist = giveWordId.wordList()
    for i in urls:
        tlistWeNeed.append(jieba.cut_for_search(i.title.lower()))
        clistWeNeed.append(jieba.cut_for_search((''.join(i.text))[:100].lower()))
        #print(i.url,i.time)
        t = gettime(i.time)

        time.append(t)
        #print(type(i.time))
    n = 0
    #print(tlistWeNeed)
    for i in tlistWeNeed:
        n+=1

        for j in i:
            if j and j != ' ' and j!='\0' and j !='\'' and j !='\"' and j !='\\':
                wordlist.addTWordFile(j,n+num2,time[n-1])
    n = 0
    for i in clistWeNeed:
        n+=1
        for j in i:
            if j and j != ' ' and j!='\0' and j !='\'' and j !='\"' and j !='\\':
                wordlist.addCWordFile(j,n+num2,time[n-1])
    print('%s data need to be inserted'%wordlist.size)
    return saveWordList.saveWordList(wordlist,conn,num1)
"""def getNotIn(que,rque,conn):
    while not que.empty():
        url = que.get()
        #conn = sqlite3.connect('D:/SearchData(0).db')
        if not conn.execute('''
        select ID from URLS where URL = '%s'
        '''%url).fetchone():
            rque.put(url)
            print('add '+url)"""
def updateData(pages,conn):
    dsset = set()
    with open('C:/mobileDisplay.txt','r') as f:
        url = f.readline()[:-2]
        while url != '':
            page = FormatUrl.IsPage(url)
            if page<pages:
                #print(url)
                dsset.add(url)
            url = f.readline()[:-2]
    print('getting ViewThread...')
    getViewThread.getViewT((dsset,len(dsset)))
    print('getting ExceptionThread...')
    getViewThread.getEView()
    uset = set()
    uhave = set()
    print('getting URls...')
    abc = conn.execute('''
    select URL from URLS
    ''').fetchall()
    for i in abc:
        #print(i[0])
        uhave.add(i[0])
    print(len(uhave))

    with codecs.open('C:/urls.txt','r','utf-8') as f:
        data = f.readline()[:-2]
        while data != '':
            if data in uhave:
                #print(data)
                pass
            else:
                #print(data)
                uset.add(data)
            data = f.readline()[:-2]
    with codecs.open('C:/urlss.txt','r','utf-8') as f:
        data = f.readline()[:-2]
        while data != '':
            if data in uhave:
                #print(data)
                pass
            else:
                #print(data)
                uset.add(data)
            data = f.readline()[:-2]
    if not len(uset):
        print('updating is needless')
        return 0
    print('got %s urls'%len(uset))
    que = Queue()
    for i in uset:
        que.put(i)
    urls = Manager().list()
    processes = []
    for i in range(5):
        processes.append(Process(target= task,args=(que,urls)))
    for i in processes:
        i.start()

    for i in processes:
        i.join()
    print('got urls\' contents')

    print('update database...')
    with open('C:/num.txt','r') as f:
        nums = f.read()
        nums  =  nums.split(' ')
        num1,num2 = int(nums[0]),int(nums[1])
    # 通过结巴分词放入数据库
    with open('C:/locked','w') as f:
        f.write('1')
    print('update the URLs...')
    num3 = addURLS(num2,conn,urls)
    print('update the wordlist...')
	
    num1 = addWordList(num1,num2,conn,urls)
    
    with open('C:/locked','w') as f:
        f.write('0')
    with open('C:/num.txt','w') as f:
        f.write(str(num1)+' '+str(num3))

    print('down')
    return 1

if __name__ == '__main__':
    #sendEmail(u'今天美美睡了一觉',['1003250467@qq.com'],u'想你了')

    """conn = sqlite3.connect('D:/SearchData(2).db', check_same_thread=False)
    #mistake(conn)
    print(conn.execute('select count(ID) from WORDID').fetchone()[0])
    print(conn.execute('select count(ID) from WORDID').fetchone()[0])
    """
    conn = sqlite3.connect('C:/SearchData(0).db',check_same_thread=False)

    url='http://bbs.rs.xidian.me/forum.php?mod=viewthread&tid=857014&extra=page%3D2&mobile=2'

    curUrl = TheParser.TheParser(url, weNeed).getURL()
    #print(curUrl.title)
    #print(curUrl.time)
    #print(''.join(curUrl.text))
    
    if updateData(10,conn):
        conn.commit()
        shutil.copyfile('C:/SearchData(0).db', 'C:/SearchData(1).db')
        print('copy down')
    conn.close()
    last = time.time()
    while True:
        now = time.time()
        
        if now - last >= 3600:
            last = now
            conn = sqlite3.connect('C:/SearchData(0).db',check_same_thread=False)
            print('start update data at %s'%time.ctime())

            if updateData(5,conn):
                conn.commit()
    #conn.close()
                
                shutil.copyfile('C:/SearchData(0).db','C:/SearchData(1).db')
                print('copy down')
            conn.close()
        else:
            time.sleep(1)




