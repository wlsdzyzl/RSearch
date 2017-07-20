import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Spider import TheParser,FormatUrl,getDisplay
#import queue
import codecs


def getEView():
    cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
             '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
             '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
    weNeed = {}
    uset = set()
    with open('C:/urlss.txt', 'w') as f:
        f.write('')
    for i in cookie.split(';'):
        key, value = i.split('=', 1)
        weNeed[key] = value
    with open('C:/except.txt','r') as f:
        abc = f.readlines()
        for i in abc:

            i = i[:-2].encode('utf-8')
            print(i)
            par = TheParser.TheParser(i,weNeed)
            urls = par.getURL()
            if urls:
                for url in urls.links:
                    if FormatUrl.IsView(url):
                        uset.add(url)
        with open('C:/urlss.txt','w') as f:
            for i in uset:
                f.write(i+'\r\n')
        with open('C:/except.txt','w') as f:
            f.write('')
		
    
def getViewT(ag):
    cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
             '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
             '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
    weNeed = {}
    for i in cookie.split(';'):
        key, value = i.split('=', 1)
        weNeed[key] = value
    with open('C:/except.txt', 'w') as f:
        f.write('')
    now = 0
    anoSet = set()
    abc = 0
    uset = ag[0]
    n = ag[1]
    #n = 1
    #uset = set()
    #uset.add('http://rs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=157')
    for i in uset:
        now+=1
        par = TheParser.TheParser(i,weNeed)
        urls = par.getURL()
        print('search in '+i)
        if urls:
            for url in urls.links:
                if FormatUrl.IsView(url):
                    #print url
                    anoSet.add(url)
                    abc+=1
                    #print('we got %s urls now we are in display %s. There are %s displays'%(abc,now,n))
        else:
            with open('C:/except.txt','a') as f:
                        f.write(i+'\r\n')
    num = 0
    with codecs.open('C:/urls.txt','w','utf-8') as f:
        for i in anoSet:
            #print(i)
            f.write(i+'\r\n')
            num+=1
			
        #f.write(str(num))