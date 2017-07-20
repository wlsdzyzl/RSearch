import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Spider import TheParser,FormatUrl
import queue
import codecs
import pickle


que = queue.Queue()
uset = set()
#Uset = set()
"""login = [("Parameter","Value"),("username","qq19961001"),("cookietime","2592000"),("password","qq19961001"),
         ("quickforward","yes"),("handlekey","Is")]

re = requests.post("http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",
              data=login  )

print(re.text)

time.sleep(4)

print(re.text)"""
# get cookies
cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
         '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
         '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
weNeed = {}
for i in cookie.split(';'):

     key,value =  i.split('=',1)
     weNeed[key] = value


que.put('http://rs.xidian.edu.cn/forum.php')
#que.put('http://rs.xidian.edu.cn/forum.php?mod=attachment&aid=NzY3NTAxfDljYWIwYjQyfDE0NDM0MzMyOTB8Mjg0MTE1fDc3NTA3NQ%3D%3D')
num = 0
uset.add('http://rs.xidian.edu.cn/forum.php')
now = ''

try:
    while not que.empty():
        now = que.get()
        print(str(que.qsize())+' urls are waiting...')
        print('now we are try to get the data of '+now)
        top = TheParser.TheParser(now,weNeed)
    #print(top.URL)
        curUrl = top.getURL()


        if  curUrl:


            #print(curUrl.url, curUrl.title, curUrl.time)
            if FormatUrl.IsView(now):

                with codecs.open('D:/TheUrlWeGot/' + str(num) + '.txt', 'w','utf-8') as f:
                    f.write(curUrl.url+'\r\n')
                    f.write(curUrl.title+'\r\n')
                    f.write(str(curUrl.time)+'\r\n')

            #print (curUrl.text)
                    f.write(''.join(curUrl.text))
        #Uset.add(curUrl)
                    num += 1

            elif FormatUrl.IsDisplay(now) or now == 'http://rs.xidian.edu.cn/forum.php':

                for i in curUrl.links:

                    if i in uset:
                        pass
                    else:

                        #print(i)
                        que.put(i)
                        uset.add(i)
        #print(i)
except Exception as e:
    print(now)

    with open('D:/Now.pickle','w') as file:
        pickle.dump(uset,file)
    with open('D:/Wait.pickle','w') as file:
        pickle.dump(uset,file)
    with open('D:/Queue.pickle','w') as file:
        pickle.dump(que,file)
