"""
这个程序为分布式爬虫准备
利用python的分布式进程来实现
因为一台电脑再爬时候总是卡顿或者内存占用过大而停止，无法爬取所有数据
这个为在两台或者多台电脑上进行做准备

"""
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Spider import TheParser

import codecs
#import pickle

def spider1_start(que1,que2):
    #print("Start")
    num = 0
    uset = set()
    cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
             '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
             '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
    weNeed = {}
    for i in cookie.split(';'):
        key, value = i.split('=', 1)
        weNeed[key] = value
    print(que1.qsize(),que2.qsize())
    while not que1.empty() or not que2.empty():
        if que1.empty():
            continue
        curUrl = que1.get(timeout = 1)
        if ord(curUrl[-1]) %2 == 0:
            que2.put(curUrl)

        else:
            if curUrl in uset:
                continue
            try:
                par = TheParser.TheParser(curUrl,weNeed)
                links = par.getURL()
                if links:
                    uset.add(curUrl)
                    with codecs.open('D:/TheUrlWeGot1/1-' + str(num) + '.txt', 'w', 'utf-8') as f:
                        f.write(links.url + '\r\n')
                        f.write(links.title + '\r\n')
                        f.write(str(links.time) + '\r\n')

                # print (curUrl.text)
                        f.write(''.join(links.text))
                # Uset.add(curUrl)
                # print(num,curUrl.url,curUrl.title,curUrl.time)

                    num += 1

                    for i in links.links:

                        if i in uset:
                            pass
                        else:
                            #uset.add(i)
                    # print(i)
                            if ord(i[-1])%2 == 0:
                                que2.put(i)
                            else:
                                que1.put(i)

                    # print(i)
            except Exception as e:
                print(curUrl)


                """with open('D:/Now.pickle', 'w') as file:
                    pickle.dump(uset, file)
                with open('D:/Wait.pickle', 'w') as file:
                    pickle.dump(uset, file)
                with open('D:/Queue.pickle', 'w') as file:
                    pickle.dump(que1, file)
            """

def spider2_start(que2,que1):
    num = 0
    uset = set()
    cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
             '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
             '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
    weNeed = {}
    for i in cookie.split(';'):
        key, value = i.split('=', 1)
        weNeed[key] = value

    while not que2.empty() or not que1.empty():
        if que2.empty():
            continue
        curUrl = que2.get(timeout = 1)
        if ord(curUrl[-1]) % 2 != 0:
            que1.put(curUrl)
        else:
            if curUrl in uset:
                continue
            try:
                par = TheParser.TheParser(curUrl, weNeed)
                links = par.getURL()
                if links:
                    uset.add(curUrl)
                    with codecs.open('D:/TheUrlWeGot1/2-' + str(num) + '.txt', 'w', 'utf-8') as f:
                        f.write(links.url + '\r\n')
                        f.write(links.title + '\r\n')
                        f.write(str(links.time) + '\r\n')

                        # print (curUrl.text)
                        f.write(''.join(links.text))
                        # Uset.add(curUrl)
                        # print(num,curUrl.url,curUrl.title,curUrl.time)

                    num += 1

                    for i in links.links:

                        if i in uset:
                            pass
                        else:

                            # print(i)
                            if ord(i[-1])%2 !=0:
                                que1.put(i)
                            else:
                                que2.put(i)

                            # print(i)
            except Exception as e:
                print(curUrl)

                """with open('D:/Now.pickle', 'w') as file:
                    pickle.dump(uset, file)
                with open('D:/Wait.pickle', 'w') as file:
                    pickle.dump(uset, file)
                with open('D:/Queue.pickle', 'w') as file:
                    pickle.dump(que, file)"""

