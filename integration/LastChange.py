import sqlite3
import codecs
def getURLINF(conn,n):
    uset = set()
    num = 0
    for i in range(1,n+1):
        abc = conn.execute('select URL,TITLE,TIME,CONT from URLS where ID = %s'%i).fetchone()
        if abc[0] in uset:
            continue
        uset.add(abc[0])
        num+=1
        with codecs.open('D:/TheUrlWeGot/%s.txt'%num,'w','utf-8') as f:
            f.write(abc[0]+'\r\n')
            f.write(abc[1]+'\r\n')
            f.write(abc[2]+'\r\n')
            f.write(abc[3])
        print('got %s'%i)

if __name__ == '__main__':
    conn = sqlite3.connect('D:/SearchData(0).db');
    getURLINF(conn,524593)