import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from multiprocessing import Process,Queue,Manager,Lock
from Spider import TheParser,FormatUrl,threadSpider
import queue
import codecs
cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
         '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
         '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
weNeed = {}
for i in cookie.split(';'):

     key,value =  i.split('=',1)
     weNeed[key] = value
def task(que,l):
        while not que.empty():
            i = que.get()
            with codecs.open('D:/TheUrlWeGot(1)/u ('+str(i)+').txt','r','utf-8') as f:
                a = f.readline()
                l.append(a[:a.find('&extra=')])
                #print(a)
            #print('got',i)
def getExcept(xx):
    bset = set()
    que = Queue()
    l = Manager().list()
    for i in range(1,xx+1):
        que.put(i)

    processes = []
    for i in range(5):
        processes.append(Process(target = task,args = (que,l)))
    for i in range(5):
        processes[i].start()
    for i in processes:
        i.join()
    sset = set(l)
    #print(sset)	
    with codecs.open('D:/urls.txt','r','utf-8') as f:
        data = f.readline()
        n = 0
        while data !=''and n<100:
            n+=1
            bset.add(data[:data.find('&extra=')])
            #print(data[:-2])
            data = f.readline()
    #print(bset)
    #bset = set([1,2,3,4])
    #sset = set([2,3,4])
    subset = bset - sset
    with codecs.open('D:/except.txt','w','utf-8') as f2:
        for i in subset:
            f2.write(i+'\n')	   
    print('down')

    que = Queue()
    for i in subset:
        que.put(i)
    processes = []
    for i in range(5):
        processes.append(Process(target=threadSpider.threadSpider,args=(que,i)))
    for i in processes:
        i.start()
    for i in processes:
        i.join()
        
if __name__ == '__main__':
    getExcept(505694)