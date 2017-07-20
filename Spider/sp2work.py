import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Spider import spider_distributed
from multiprocessing.managers import BaseManager

class QueueManage(BaseManager):
    pass

QueueManage.register('get_que1')
QueueManage.register('get_que2')
if __name__ == "__main__":
        manager = QueueManage(address=('192.168.0.114',5000),authkey=b'zgq')
        manager.connect()
        que1 = manager.get_que1()
        que2 =manager.get_que2()
        spider_distributed.spider2_start(que2,que1)