# -*- coding: utf-8 -*-
import threading
import wx
from queue import Queue


class InvestThreadBase():
    def __init__(self, grid, afterUpdateInvestListReceiver = None):
        self.grid = grid
        self.afterUpdateInvestListReceiver = afterUpdateInvestListReceiver
        self.investDataQueue = Queue(maxsize=10)
        self.investDataThreadEvent = threading.Event()

        self.threadInvest = threading.Thread(target=self.investDataThread, args=(
        self.investDataQueue, self.investDataThreadEvent, self.updateInvestList))
        self.threadInvest.setDaemon(True)
        self.threadInvest.start()

    def investDataThread(self, investDataQueue, event, callBack):
        thread = self.getThreadWorkerClass()()
        while True:
            event.wait()

            dataList = thread.work()
            if (len(dataList) > 0):
                investDataQueue.put(dataList)

            event.clear() # clear the event

            # notify main thread
            wx.CallAfter(callBack)

            print("thread: will wait")

    def updateInvestList(self):
        dataList = self.investDataQueue.get()
        self.grid.updateInvestData(dataList)
        if (self.afterUpdateInvestListReceiver != None):
            self.afterUpdateInvestListReceiver.afterUpdateInvestList()

    def setEvent(self):
        self.investDataThreadEvent.set()
