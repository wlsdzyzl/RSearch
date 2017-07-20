from multiprocessing import process,Queue
from multiprocessing.managers import BaseManager

class QueueManage(BaseManager):
    pass

QueueManage.register('get_queue')
QueueManage.register('get_uset')

addr = '127.0.0.1'

m = QueueManage(address=(addr,5000),authkey=b'zgq')

m.connect()

tque = m.get_queue()
tset = m.get_uset()

while  tque.qsize()>5:
    n = tque.get(timeout = 1)
    if n % 2 == 0:
        tque.put(n)
    else :
        print(n)
while not tque.empty():
    n = tque.get(timeout = 1)
    print(n)
        #print(tset)
        #n.add(n+1)

