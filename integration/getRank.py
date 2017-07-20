# -*- coding: utf-8 -*-
from integration import giveWordId
import sqlite3
import jieba
default_encoding = 'utf-8'
abc = u'.,-[]()。，【】‘’“”：;'
def getRank(give,conn):
    try:
        print(give)
    except Exception as e:
        pass
    give = give.lower()
    data = jieba.cut(give)
    weNeed = []
    print(u'字符串分割完毕,正在获取内容...')
    for i in data:
        print(u'正在获取\'%s\'的内容...'%i)
        
        
        #print(i)
        try:
            res  = conn.execute('''
        select URLINF from WORDID where WORD = '%s'

        '''%i).fetchone()#得到的信息
        except Exception as e:
            return getRank(give,sqlite3.connect('C:/SearchData(1).db',check_same_thread=False))
        #print(res)
        if res:

            res = res[0]
           
            #print(res)

            #print(i)
            """if len(res)>100000:
                #print('got')
                res = res[:100000]
                i = -1
                while res[i]!=u'>':
                    i-=1
                    #print(i)
                res = res[:i+1]"""
                #print(res)
            weNeed.append(res)# 得到的信息加入
            #print(data)
    print(u'已获取内容，正在提取信息...')
    urlScore = {}
    for i in weNeed:
        #print(i)
        pair = i.split(' ')
        for j in pair:

            if not j:
                continue
            nums = j[1:-1]
            #print(nums)
            num = nums.split(':')
            #print(num)
            urlId = int(num[0])
            toctimes = int(num[1])
            coctimes = int(num[2])
            #print(num[3])
            if num == '[]':
                time = 0
            else :
                time = int(num[3])
            if urlId in urlScore:
                urlScore[urlId][0],urlScore[urlId][1],urlScore[urlId][3]=urlScore[urlId][0]+1,urlScore[urlId][1]+toctimes,urlScore[urlId][3]+coctimes
            else:
                urlScore[urlId]=[1,toctimes,time,coctimes]
    print(u'已得到信息，正在排序筛选...')
    theURL = sorted(urlScore.items(),key = lambda d:d[1],reverse=True)
    print(u'筛选完毕，正在生成返回页面信息...')
    #theURL = urlScore.items()
    theURL = theURL[:100]
    #print(theURL[0][1][0],theURL[0][1][1],theURL[0][1][2])
    #print(theURL[1][1][0], theURL[1][1][1], theURL[1][1][2])
    reaurls = []
    #give = give.decode('utf8')
    for i ,j in theURL:
        #print(i,j)
        data = conn.execute('''
        select URL,TITLE,TIME,CONT from URLS where ID = %s
        '''%i).fetchone()
        #print(i,data)
        data = list(data)


        #data[1] = unicode(data[1])
        res = u""
        p = data[1].find(u' - 西电睿思BBS - Powered by Discuz!')
        if p != -1:
            data[1] = data[1][:p]
        for i in data[1]:
            #print(type(i))
            #print(i)
            if give.find(i)!=-1 or give.find(i.lower())!= -1:
                res+=u'<strong>'+i+u'</strong>'
            else :res+=i
            #print(type(res))
        data[1] = res

        if len(data[3])>89:
            data[3] = data[3][:89]+u'...'
        #data[3] = data[3].replace(u'\n')
        res = u""
        #print(data[3])
        for i in data[3]:
            if i == u'\n':
                continue
            if give.find(i) != -1 or give.find(i.lower())!=-1:
                res+=u'<strong>'+i+u'</strong>'
            else :
            #print(type(i))

                #print('got')
                #continue
                res+=i
            #print(type(res))
        data[3] = res
        #print(data[3])
        reaurls.append(data)
    #print(reaurls[0][3])
    return reaurls

if __name__ == '__main__':
    #conn = sqlite3.connect('D:/SearchData(2).db')
    conn = sqlite3.connect('C:/SearchData(0).db')
    data = jieba.cut_for_search(u' - 西电睿思BBS - Powered by Discuz!')

    for i in data:
        if i == ' ':
            continue
        print(i)
        i = i.lower()
        inf = str(conn.execute('select URLINF from WORDID where WORD = \'%s\''%i).fetchone()[0])
        print(len(inf))
        wlv = giveWordId.wordListValue()
        wlv.getValue(inf)
        delete = []
        for m in wlv.list:
            wlv.list[m][0]-=1
            if not wlv.list[m][0] and not wlv.list[m][1]:
                delete.append(m)
        for m in delete:
            wlv.list.pop(m)
        print(len(str(wlv)))
        conn.execute(' UPDATE WORDID SET URLINF = \'%s\'WHERE WORD = \'%s\''%(str(wlv),i))
        conn.commit()
    """abc = raw_input()

    #print(abc)
    abc = abc.decode('utf-8')
    #print(abc)
    for (i,j,k) in getRank(abc,conn):
        #print(type(i),type(j),type(k))
        print(i+'\n'+j+'\n'+k)"""
    #shutil.copyfile('D:/SearchData.db', 'D:/SearchData(2).db')


