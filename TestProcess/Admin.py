from multiprocessing import process,Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
class QueueManager(BaseManager):
    pass

queue = Queue()
uset = []
def get_q():
    return queue
def get_s():
    return uset
QueueManager.register('get_queue',callable = get_q)
QueueManager.register('get_uset',callable = get_s)
if __name__ == '__main__':
    freeze_support()

    manage = QueueManager(address=('127.0.0.1',5000),authkey=b'zgq')

    manage.start()



    tque= manage.get_queue()
    tset = manage.get_uset()

    for i in range (10):
        tque.put(i)
        if i%2 == 0:
            tset.append(i)
    print("task put down")
    while(True):
        for i in set():
            print(i)

