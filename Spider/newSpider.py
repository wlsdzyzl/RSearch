import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Spider import getDisplay,getViewThread

if __name__ == '__main__':
    #getViewThread.getViewT(getDisplay.getDisplay())
    getViewThread.getEView()