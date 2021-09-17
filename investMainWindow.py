# -*- coding: utf-8 -*-
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import threading
import time

import wx
import win32api
import sys
import wx.lib.agw.aui as aui
import wx.lib.mixins.listctrl
from queue import Queue
import investThread
from investGrid import InvestGrid

APP_TITLE = "Invest"
APP_ICON = "res/invest.ico"

class MainFrame(wx.Frame):
    def addPanes(self):
        self.panelLeft = wx.Panel(self, -1)
        self.panelRightFirst = wx.Panel(self, -1)
        self.panelRightSecond = wx.Panel(self, -1)
        self.panelBottom = wx.Panel(self, -1)

        btnRefresh = wx.Button(self.panelLeft, -1, u'刷新', pos=(30, 150), size=(150, 50))
        btnRefresh.Bind(wx.EVT_BUTTON, self.OnRefresh)

        # btnSwitch = wx.Button(self.panelLeft, -1, u'切换', pos=(30, 300), size=(100, -1))
        # btnSwitch.Bind(wx.EVT_BUTTON, self.OnSwitch)

        text1 = wx.StaticText(self.panelRightSecond, -1, u'我是第2页', pos=(40, 100), size=(200, -1), style=wx.ALIGN_LEFT)
        text2 = wx.StaticText(self.panelBottom, -1, u'我是bottom', pos=(40, 100), size=(200, -1), style=wx.ALIGN_LEFT)

        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._mgr.AddPane(self.panelLeft, aui.AuiPaneInfo().Name("LeftPanel").
                          Left().Layer(1).MinSize((200, -1)).Caption(u"操作区").MinimizeButton(True).MaximizeButton(True).CloseButton(True))

        self._mgr.AddPane(self.panelRightFirst, aui.AuiPaneInfo().Name("CenterPanel0").
                          CenterPane().Show())

        self._mgr.AddPane(self.panelRightSecond, aui.AuiPaneInfo().Name("CenterPanel1").
                          CenterPane().Hide())

        self._mgr.AddPane(self.panelBottom, aui.AuiPaneInfo().Name("BottomPanel").
                          Bottom().MinSize((-1, 100)).Caption(u"消息区").CaptionVisible(False).Resizable(True))
        self._mgr.Update()

    def updateInvestClock(self):
        t = time.localtime()
        self.clockInvest.SetLabel('%02d:%02d:%02d' % (t.tm_hour, t.tm_min, t.tm_sec))

    def OnInvestTimer(self, evt):
        self.investDataThreadEvent.set()

    def addInvestClock(self):

        font = wx.Font(30, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline = False, faceName = "Monaco")
        self.clockInvest = wx.StaticText(self.panelLeft, -1, u'00:00:00',pos=(0, 0), size = (200, 50), \
                                   style = wx.ALIGN_TOP | wx.TE_CENTER | wx.SUNKEN_BORDER)
        self.clockInvest.SetForegroundColour(wx.Colour(0, 224, 32))
        self.clockInvest.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.clockInvest.SetFont(font)

        self.investTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnInvestTimer, self.investTimer)
        self.investTimer.Start(10 * 1000)

    def addClock(self):
        font = wx.Font(16, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline = False, faceName = "Monaco")
        self.clock = wx.StaticText(self.panelLeft, -1, u'08:00:00',pos=(0, 600), size = (200, 30), \
                                   style = wx.ALIGN_BOTTOM | wx.TE_CENTER | wx.SUNKEN_BORDER)
        self.clock.SetForegroundColour(wx.Colour(0, 224, 32))
        self.clock.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.clock.SetFont(font)

        self.clockTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.clockTimer)
        self.clockTimer.Start(50)
        self.lastSecond = None # init last second

    def OnTimer(self, evt):
        t = time.localtime()
        if t.tm_sec != self.lastSecond:
            self.clock.SetLabel('%02d:%02d:%02d'%(t.tm_hour, t.tm_min, t.tm_sec))
            self.lastSecond = t.tm_sec

    def addInvestGrid(self):
        self.investGrid = InvestGrid(self.panelRightFirst)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.investGrid, 1, wx.EXPAND | wx.ALL, 5)
        self.panelRightFirst.SetSizer(box)
        self.investGrid.SetFocus()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(204, 223, 254))
        self.SetSizeHints((1200, 800))

        # set icon
        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.investDataQueue = Queue(maxsize=10)
        self.investDataThreadEvent = threading.Event()

        # add thread
        self.threadRunning = True
        self.threadInvest = threading.Thread(target=self.investDataThread, args=(self.investDataQueue, self.investDataThreadEvent, self.updateInvestList))
        self.threadInvest.setDaemon(True)
        self.threadInvest.start()

        # add panes, clock
        self.addPanes()
        self.addInvestGrid()
        self.addClock()
        self.addInvestClock()

        # bind key-down event
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panelLeft.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panelRightFirst.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panelRightSecond.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panelBottom.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        # last: trigger the timer
        self.OnInvestTimer(wx.EVT_TIMER)

    def updateInvestList(self):
        self.updateInvestClock()
        dataList = self.investDataQueue.get()
        print("main: {0}: get data".format(len(dataList)))
        self.investGrid.updateInvestData(dataList)

    def OnKeyDown(self, evt):
        keyCode = evt.GetKeyCode()
        # print(keyCode)
        if (evt.GetKeyCode() == wx.WXK_F5):
            print("main: notify the thread")
            self.investDataThreadEvent.set()
        if (evt.GetKeyCode() == wx.WXK_F9):
            self.showSummaryDialog()
        evt.Skip()

    def investDataThread(self, investDataQueue, event, callBack):
        thread = investThread.investThread()
        while self.threadRunning:
            event.wait()

            dataList = thread.work()
            investDataQueue.put(dataList)

            event.clear() # clear the event

            # notify main thread
            wx.CallAfter(callBack)

            print("thread: will wait")

    def OnRefresh(self, evt):
        # refresh the data
        print("main: notify the thread")
        self.investDataThreadEvent.set()

    def OnSwitch(self, evt):
        '''切换信息显示窗口'''

        p0 = self._mgr.GetPane('CenterPanel0')
        p1 = self._mgr.GetPane('CenterPanel1')

        p0.Show(not p0.IsShown())
        p1.Show(not p1.IsShown())

        self._mgr.Update()


class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame(None)
        self.Frame.Show()
        self.Frame.Maximize(maximize=True)
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()


