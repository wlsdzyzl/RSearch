import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from multiprocessing import Process,Queue,Manager,Lock
from Spider import TheParser,FormatUrl
#import queue
import codecs
import pickle
import time
import threading

cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
         '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
         '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
weNeed = {}
for i in cookie.split(';'):

     key,value =  i.split('=',1)
     weNeed[key] = value
lock = threading.Lock()
def spider_start(que,pid):
    num = 0
    while not que.empty():
        lock.acquire()
        url = que.get()
        lock.release()
        print(str(pid)+'-'+threading.current_thread().name +' got one,%s remained'%que.qsize())
        curUrl = TheParser.TheParser(url, weNeed).getURL()
        if curUrl:
            
            with codecs.open('D:/TheUrlWeGot(0)/a (' +str(pid)+'-' +threading.current_thread().name + '-' + str(num) + '.txt', 'w',
                         'utf-8') as f:
                f.write(curUrl.url + '\r\n')
                f.write(curUrl.title + '\r\n')
                f.write(str(curUrl.time) + '\r\n')
                # print (curUrl.text)
                f.write(''.join(curUrl.text))
            num+=1
        else:
            lock.acquire()
            que.put(url)
            lock.release()

    """try:
        while not que.empty():
            lock.acquire()
            now = que.get()
            lock.release()
            #print(str(que.qsize()) + ' urls are waiting...')
            #print('now we are try to get the data of ' + now)
            top = TheParser.TheParser(now, weNeed)
            # print(top.URL)
            curUrl = top.getURL()

            if curUrl:

                # print(curUrl.url, curUrl.title, curUrl.time)
                if FormatUrl.IsView(now):

                    with codecs.open('D:/TheUrlWeGott/' + threading.current_thread().name+'-'+str(num) + '.txt', 'w', 'utf-8') as f:
                        f.write(curUrl.url + '\r\n')
                        f.write(curUrl.title + '\r\n')
                        f.write(str(curUrl.time) + '\r\n')

                        # print (curUrl.text)
                        f.write(''.join(curUrl.text))
                        # Uset.add(curUrl)
                        num += 1

                elif FormatUrl.IsDisplay(now) or now == 'http://rs.xidian.edu.cn/forum.php':

                    for i in curUrl.links:

                        if i in uset:
                            pass
                        else:

                            # print(i)
                            lock.acquire()
                            que.put(i)
                            uset.add(i)
                            lock.release()
                            # print(i)"""

def threadSpider(que,pid):

    #uset = set()

	
    print(que.qsize())
    #spider_start(que)

    threading.current_thread().setName('0')
    threads = []
    for i in range(0,20):
        threads.append(threading.Thread(target=spider_start,name=str(i),args = (que,pid)))

    #time.sleep(0.5)  # full the queue

    for i in threads:
        i.start()
    for i in threads:
        i.join()
    print('down')
if __name__ == "__main__":
    que = Queue()
    uset = set()
    with codecs.open('D:/urls.txt','r','utf-8') as f:
        data = f.readline()
        while data != '':
            uset.add(data[:-2])
            data = f.readline()
    with codecs.open('D:/urlss.txt','r','utf-8') as f:
        data = f.readline()
        while data != '':
            uset.add(data[:-2])
            data = f.readline()
    for i in uset:
        #print(i)
        que.put(i)
    processes = []
    for i in range():
        processes.append(Process(target=threadSpider,args=(que,i)))
    for i in processes:
        i.start()
    for i in processes:
        i.join()
        
		
