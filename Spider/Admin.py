import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from multiprocessing import Queue
from multiprocessing.managers import BaseManager
#from multiprocessing import freeze_support

class QueueManager(BaseManager):
    pass

que1 = Queue()
que2 = Queue()

def get_q1():
    return que1
def get_q2():
    return que2

QueueManager.register('get_que1',callable=get_q1)
QueueManager.register('get_que2',callable=get_q2)

if __name__ == '__main__':

    #print(len('http://rs.xidian.edu.cn/forum.php'))
    manager = QueueManager(address=('192.168.0.114',5000),authkey=b'zgq')
    manager.start()
    queue1 = manager.get_que1()
    queue2 = manager.get_que2()
    queue1.put('http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=377353&extra=')
    while True:
        if not queue1.qsize() and not queue2.qsize():
            print('down')

