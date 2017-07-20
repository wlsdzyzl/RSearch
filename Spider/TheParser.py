# -*- coding: utf-8 -*-
#from urllib import request

from HTMLParser import HTMLParser
import requests
import re
from Spider import URL,FormatUrl
import time

class TheParser(HTMLParser):
    #this class extends HTMLParser
    def __init__(self,Url,cookie):
        HTMLParser.__init__(self)
        self.cookies = cookie
        self.link = []
        self.text = []
        self.URL = Url
        self.top = False
        self.first = False
        self.layer = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name,value) in attrs:
                if name == 'href':
                    self.link.append(value)
        elif tag == 'div':
            if self.layer:
                self.layer+=1
            for (name,value) in attrs:
                #print(value)
                if self.first == False and name =='class'and value=='message':
                    #self.first = True
                    #print('yes')
                    self.top = True
                    self.layer+=1#层数
    def handle_endtag(self, tag):
        if tag == 'div' and self.layer:
            self.layer-=1
            if self.layer==0:
                self.top = False
                self.first=True

    def handle_data(self, data):
        if self.top:
            self.text.append(data)
            #self.top = False
    def getContent(self):
        try:

            req = requests.get(self.URL,cookies=self.cookies )
            #print('get method')
            #req.encoding = 'gb2312'
        except Exception as e:

            return ''
        else:
            if(req.status_code == 200):
                req.encoding = 'utf-8'
                return req.text
            else:
                return ''
        """with request.urlopen(req) as f:
            data = f.read()
            f.close()
            return gzip.decompress(data).decode()"""

    def getURL(self):
        #print('wocao')
        data =self.getContent()
        if data == '':
            return []
        re_space = re.compile('\\s+',re.DOTALL)
        data = re_space.sub(' ',data)
        def getTitle(data):
            i = data.find('<title>')
            j = data.find('</title>')
            if i == -1 or j == -1:
                i = data.find('<TITLE>')
                j = data.find('</TITLE>')
            data = data[i+7:j]
            #print(type(data))
            return data[:data.find(u' - 西电睿思BBS - 手机版 - Powered by Discuz!')]
        def getTime(data):
            """t = re.compile(r'(\d+)-(\d+)-(\d+)(\s+)(\d+):(\d+):(\d+)')
            target = t.search(data)

            if target:
                return target.group()
            else:"""
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            """recently = 2017*410+3*31+26
            record = (2017,3,26)
            if not target:
                return record
            else:
                for year,month,day in target:
                    if int(year)*410 + int(month)*31 + int(day) < recently:
                        recently ,record = int(year) + int(month) + int(day) ,(int(year),int(month),int(day))
                return record"""
        #def getFirstFloor(data):
            #t = re.compile(r'<td id=.*')
        if FormatUrl.IsView(self.URL):
            title = getTitle(data)
            ttime = getTime(data)
        else :
            title = ""
            ttime = ""

        """for char in self.getContent():
            adder = ' ' if char == '\n' else char
            #print(adder)
            data+=adder"""



        """re_comment = re.compile('<!--[^>]*-->', re.DOTALL)  # HTML注释
        data = re_comment.sub('', data)"""
        #re_javascript = re.compile('<[.]*javascript[.]*>',re.DOTALL)
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.DOTALL)  # 匹配CDATA
        re_script = re.compile('<script.*?/script>', re.DOTALL)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.DOTALL)  # style
        re_style_upper = re.compile('<\s*STYLE[^>]*>[^<]*<\s*/\s*STYLE\s*>', re.DOTALL)  # upper
        re_br = re.compile('<br\s*?/?>',re.DOTALL)  # 处理换行
        #re_h = re.compile('</?\w+[^>]*>',re.DOTALL)  # HTML标签
        re_comment = re.compile('<!--[^>]*-->',re.DOTALL)  # HTML注释
        #re_img = re.compile('<img(.)*>',re.DOTALL)
        #re_space = re.compile('\\s+',re.DOTALL)
        #data = re_space.sub('',data)
        #data = re_javascript.sub('',data)
        data = re_cdata.sub('',data)
        data = re_script.sub('',data)
        data = re_style.sub('',data)
        data = re_style_upper.sub('',data)
        data = re_br.sub('\n',data)
        #data = re_h.sub('',data)
        data = re_comment.sub('',data)
        #data = re_img.sub('',data)

        try:
            self.feed(data)
        except Exception as e:
            return []
        else :
            links = []
            last = 1
            searchpage = 1
            for link in self.link:

                link = link.encode('utf-8')
                if not FormatUrl.IsNeed(link):

                    pass
                else:
                    #print(link)
                    if FormatUrl.IsDisplay(link):
                        page = FormatUrl.IsPage(link)
                        if page == -1:
                            links.append(FormatUrl.Stand(link))
                        elif page == 1:
                            searchpage = 0
                        elif searchpage == 1:
                            if page == last+1:
                                links.append(FormatUrl.Stand(link))
                            else:
                                segment = link[:link.find('page='+str(page))]
                                for i in range(last+1,page+1):
                                    links.append(FormatUrl.Stand(segment+'page='+str(i)))

                    else:
                        if FormatUrl.IsPage(link) == -1:
                            links.append(FormatUrl.Stand(link))



            #for i in links:
                #print(i)
            return URL.URL(self.URL,title,ttime,links,self.text)


cookie = 'UM_distinctid=15aec513b3d1-02deb1f6362632-47534330-100200-15aec513b3fc2; Q8qA_2132' \
         '_sid=Q19ZKw; Q8qA_2132_saltkey=LEWqQ3Ws; Q8qA_2132_lastvisit=1490101864; Q8qA_2132_lastact=1490105496%09misc.php%09patch; Q8qA_2132_ulastactivity=4ccbu45GSdHaOTLgb3NFBmxQF%2FCGzkNlw7zmxkY0oNsCD5wstpW%2F; Q8qA_2132_auth=8997tPHhopfkewDm9uINGEJqy4uj2HKO1Ohm1oBypWmHT14%2F4YEZFkwpA%2B3Oj%2Fh2YreGlWUgHLbi8e%2BWOyqoSJJxMiQ; Q8qA_2132_lastcheckfeed=2' \
         '97526%7C1490105491; Q8qA_2132_lip=10.183.121.43%2C1490105215; Q8qA_2132_myrepeat_rr=R0; Q8qA_2132_nofavfid=1'
weNeed = {}
for i in cookie.split(';'):

     key,value =  i.split('=',1)
     weNeed[key] = value

if __name__ == "__main__":
    aTest = TheParser('http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=856683',weNeed)
    a = aTest.getURL()
    """for i in aTest.link:
        print(i)
    for i in aTest.text:
        print(i)"""
    print(a.title)

