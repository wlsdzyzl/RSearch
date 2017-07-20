def IsDisplay(data):
    """return data.find('javascript') != -1 or data.find("webmail")!=-1 or data.find("apk") != -1 or data.find("zip")!= -1 or data.find("jpg")!= -1 \
           or data.find("forum") == -1 or data.find("mobile")!= -1 or data.find("goto=lastpost#lastpost")!= -1 or data.find("mod=attachment")!= -1 or data.find("pid=")!=-1\
    or data.find("searchsubmit=yes")!=-1"""
    return data.find('mod=forumdisplay') != -1 and data.find('filter=') == -1 and data.find('forumdefstyle=')==-1
def IsView(data):
    return data.find('mod=viewthread')!=-1
def IsNeed(data):
    return  IsDisplay(data) or IsView(data)


def Stand(data):
    if data.find('http://bbs.rs.xidian.me/') == -1:
        data = 'http://bbs.rs.xidian.me/'+data
    if IsView(data) :
        p = data.find('&extra=')
        if p!= -1:
            data = data[:p]
    if data.find('mobile=2') == -1:
        data += '&mobile=2'
    return data
def IsPage(data):
    a = data.find('page=')
    num = ''
    if  a != -1:
        for i in data[a+5:]:
            if str.isdigit(i):
                num += i
            else:
                break
        if num != '':
            return int(num)
        else:
            return -1
    else :
        return -1