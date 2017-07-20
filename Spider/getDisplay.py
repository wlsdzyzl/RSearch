import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Spider import TheParser,FormatUrl
import Queue
import codecs
import pickle


def getDisplay():
    que = Queue.Queue()
    uset = set()
    #uset.add('http://rs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=106')
    #return uset
    # Uset = set()
    """login = [("Parameter","Value"),("username","qq19961001"),("cookietime","2592000"),("password","qq19961001"),
             ("quickforward","yes"),("handlekey","Is")]

    re = requests.post("http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",
                  data=login  )

    print(re.text)

    time.sleep(4)

    print(re.text)"""
    # get cookies
    cookie = 'Q8qA_2132_saltkey=gg5583Ag; Q8qA_2132_lastvisit=1491742682' \
             '; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
             '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
    weNeed = {}
    for i in cookie.split(';'):
        key, value = i.split('=', 1)
        weNeed[key] = value

    que.put('http://bbs.rs.xidian.me/forum.php?forumlist=1&mobile=2')
    # que.put('http://rs.xidian.edu.cn/forum.php?mod=attachment&aid=NzY3NTAxfDljYWIwYjQyfDE0NDM0MzMyOTB8Mjg0MTE1fDc3NTA3NQ%3D%3D')
    num = 0
    #uset.add('http://rs.xidian.edu.cn/forum.php')
    now = ''

    try:
        while not que.empty():
            now = que.get()
            print(str(que.qsize()) + ' urls are waiting...')
            print('now we are try to get the data of ' + now)
            
            # print(top.URL)
            if FormatUrl.IsDisplay(now) and FormatUrl.IsPage(now) == -1 or now == 'http://bbs.rs.xidian.me/forum.php?forumlist=1&mobile=2':
                top = TheParser.TheParser(now, weNeed)
                curUrl = top.getURL()

                if curUrl:                
                    for i in curUrl.links:

                        if i in uset:
                            pass
                        elif FormatUrl.IsDisplay(i):
                            num+=1
                            # print(i)
                            que.put(i)
                            uset.add(i)
                else:
                    with open('D:/except.txt','a') as f:
                        f.write(now+'\r\n')
                            # print(i)
    except Exception as e:
        pass
    finally:
        print(num)
        return uset,num
if __name__ == "__main__":
    with open('D:/mobileDisplay.txt','w') as f:
        #f.write('abc')
        for i in getDisplay()[0]:
            f.write(i+'\r\n')

