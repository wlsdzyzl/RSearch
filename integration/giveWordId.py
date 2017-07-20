# -*- coding: utf-8 -*-
from Spider import URL
import jieba
import codecs
from multiprocessing import Process,Queue,Manager,Lock

#DATA_ = (data)


class wordListValue(object):
    def __init__(self):
        self.list = {}
    def addFileT(self,file,time):
        if file in self.list:
            self.list[file][0]+=1
        else:
            self.list[file]=[]
            self.list[file].append(1)
            self.list[file].append(0)
            self.list[file].append(time)
    def addFileC(self,file,time):
        if file in self.list:
            self.list[file][1] +=1
        else:
            self.list[file]=[]
            self.list[file].append(0)
            self.list[file].append(1)
            self.list[file].append(time)

    def getValue(self,s):
        self.list={}
        vs = s.split(' ')
        for i in vs:
            #print(i)
            i = i[1:-1]
            kv = i.split(':')
            self.list[int(kv[0])]=[int(kv[1]),int(kv[2]),int(kv[3])]
    def __str__(self):
        res = ''
        for i  in self.list:
            res+=('<%s:%s:%s:%s> '%(i,self.list[i][0],self.list[i][1],self.list[i][2]))

        return res[:-1]
class wordList(object):
    def __init__(self):
        self.dict = {}
        self.size = 0
    def addCWordFile(self,word,file,time):
        if word in self.dict:
            self.dict[word].addFileC(file,time)
        else :
            self.dict[word] = wordListValue()
            self.dict[word].addFileC(file,time)
            self.size+=1
    def addTWordFile(self,word,file,time):
        if word in self.dict:
            self.dict[word].addFileT(file,time)
        else :
            self.dict[word] = wordListValue()
            self.dict[word].addFileT(file,time)
            self.size+=1

        #print(word,self.dict[word])
    def __str__(self):
        return str(self.dict)
#def getfileId(file):
    #return int(file[15:].split('.',1)[0])
def UpdateList(file):
    #id = getfileId(file)
    #print(id)
    #data = ''
    with codecs.open(file,'r','utf-8') as f:
        f.readline()
        data = f.readline()
        if not data[:-2]:
            data = f.readline()
        tdata = data[:-2]
        time = f.readline()[:-2]
        time=time.encode('utf-8')
        cdata=f.read()
        #print('begin')
        tdata = tdata.replace('\n','')
        cdata = cdata.replace('\n','')
        cdata = cdata[:100]
        tdata = tdata.lower()
        cdata = cdata.lower()
        #print(cdata)
        #print(data)
        #print(file,time)
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

            abc = (abc[0]-2010)*31622400+abc[1]*2678400+abc[2]*86400+abc[3]*3600+abc[4]*60+abc[5]
        except Exception as e:
            print(file,time)
            return [],[],0
        #print DATA_
    title_words = jieba.cut_for_search(tdata)
    words = jieba.cut_for_search(cdata)

    #words = words.encode('utf-8')
    """for i in words:
        if i != ' ' and i != '\''and i !='\"':
            wordlist.addWordFile(i,id)"""

    return title_words,words,abc
def getURL(file):
    with codecs.open(file,'r','utf-8') as f:
        data = f.readline()
        return data
def task(que,listWeNeedt,listWeNeedc,urlID,urltime,lock):
        #listWeNeed = []#由list和id构成的列表
    #listWeNeed=[]
    while not que.empty():
        i = que.get()
        #print(i)

        filename = 'D:/TheUrlWeGot/' + str(i) + '.txt'
        #listWeNeed.append('1')
        l = UpdateList(filename)
        if l[0] or l[1]:
            lock.acquire()

            listWeNeedt.append(list(l[0]))
            listWeNeedc.append(list(l[1]))
            urlID.append(i)
            urltime.append(l[2])
            lock.release()
            #if i % 1000 == 0:
               # print(len(urlID))


        #print('%s remained' % que.qsize())
def makefile(begin,end):
    listweNeedt = Manager().list()
    listweNeedc = Manager().list()
    urlId = Manager().list()
    urltime = Manager().list()
    wordlist = wordList()
    lock = Lock()
    que = Queue()
    if begin + 1000<end:
        end = begin+1000
    for i in range(begin,end):
        que.put(i)

    processes = []
    for i in range(5):
        processes .append( Process(target=task,args=(que,listweNeedt,listweNeedc,urlId,urltime,lock)))

    #p = Pool(5)
    for i in range (5):
        processes[i].start()

    for i in range(5):
        processes[i].join()
    n = 0
    for i in listweNeedt:
        for j in i:
            #j = j.encode('utf-8')
            if j != u'\'' and j != u' ' and j != u'\"' and j != u'\\' and j!=u'\0':
                wordlist.addTWordFile(j,urlId[n],urltime[n])
        n+=1
    n = 0
    for i in listweNeedc:
        for j in i:
            #j = j.encode('utf-8')
            if j != u'\'' and j != u' ' and j !=u'\"' and j != u'\\' and j!=u'\0':
                wordlist.addCWordFile(j,urlId[n],urltime[n])
        n+=1
    return end,wordlist
        #result = p.apply_async(task,args=(que,listWeNeed))
    #p.close()
    #p.start()
    #p.join()
    #if result.successful():
     #   print('successful')
def make_list(begin,end):
    wordlist = wordList()
    if begin + 10 < end:#一次读取一万个文件 缓存区是够用的
        end = begin + 10
    for i in range(begin, end):
        #print(i)
        with codecs.open('D:/words/%s.txt'%i, 'r', 'utf-8') as f:
            abc = f.readlines()
            #print(i,abc)
            for j in abc:
                #print(j)
                j = j.encode('utf-8')
                j = j[:-1]
                if j != '\'' and j!=' ' and j!='\"'and j!='\\'and j != '\0':
                    wordlist.addWordFile(j, i)
    #print(wordlist.size)
    """j = 0
    for i in listWeNeed:
        #print(i)

        for word in i:
            #print(word)
            if word != ' ' and word != '\'' and word != '\"':
                wordlist.addWordFile(word, urlId[j])

        j+=1
        print('already add %s'%j)
    #print('what')"""
    return end,wordlist

if __name__ == '__main__':
    data = u'someThing'
    for i in jieba.cut(data):
        print(i)
    """wordlist = make_list(10000)
    while True:
        searchfor = input()
        realSearch = jieba.cut_for_search(searchfor)
        for i in realSearch:
            print(i)
            if i in wordlist.dict:
                for j in wordlist.dict[i].list:
                    print(getURL('D:/TheUrlWeGot/' + str(j) + '.txt') + ',occur ' + str(
                        wordlist.dict[i].list[j]) + 'times')"""




