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
import wx.grid as gridlib
from queue import Queue
import investThread
import tools
import crawlData

APP_TITLE = "Invest"
APP_ICON = "res/invest.ico"

class mainFrameSimple(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize(800, 600)
        self.Center()

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

class InvestGrid(gridlib.Grid):
    class Const:
        UPDOWN_FIELD_WIDTH = 2
        FONT_SIZE_SEPARATOR = 12
        FONT_SIZE_CONTENT = 14
        FONT_NAME = "微软雅黑"
        COLOR_LIGHT_YELLOW = wx.Colour(255, 255, 180)
        COLOR_BACKGROUND_LIGHT_GRAY = wx.Colour(245, 245, 245)
        COLOR_DARK_GREEN = wx.Colour(0, 128, 64)
        ROW_SIZE = 30
        ROW_MAX_NUMBER = 30

    def initConst(self):
        self.COLUMN = tools._constBase()
        self.COLUMN.NAME = 0
        self.COLUMN.CURRENT_PRICE = 1
        self.COLUMN.UPDOWN_PRICE = 2
        self.COLUMN.UPDOWN_PERCENT = 3
        self.COLUMN.ORIGIN_PRICE = 4
        self.COLUMN.ORIGIN_UPDOWN_PERCENT = 5

        self.Columns = dict()
        self.Columns[self.COLUMN.NAME] = "产品"
        self.Columns[self.COLUMN.CURRENT_PRICE] = "当前价格"
        self.Columns[self.COLUMN.UPDOWN_PRICE] = "涨跌额"
        self.Columns[self.COLUMN.UPDOWN_PERCENT] = "涨幅"
        self.Columns[self.COLUMN.ORIGIN_PRICE] = "原始价格"
        self.Columns[self.COLUMN.ORIGIN_UPDOWN_PERCENT] = "原始价格涨幅"

        self.SeparatorTitles = dict()
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_STOCK] = "股票列表"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_YUEGANGAO_INDEX] = "粤港澳大湾区指数"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_FUND] = "基金列表"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_INDEX] = "指数列表"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_FOREIGN_INDEX] = "指数列表"

    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.initConst()

        self.CreateGrid(self.Const.ROW_MAX_NUMBER, len(self.Columns))
        self.EnableEditing(False)
        self.setGridFormat = self.createSetGridFormat()

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.Const.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])

    def GetColorByUpDown(self, number):
        if (number > 0.0):
            return self.Const.COLOR_DARK_GREEN
        return wx.RED

    def SetCellNumberAndColor(self, row, col, argNumber, fieldWidth = -1):
        textNumber = ''
        floatNumber = 0.0
        if (type(argNumber) is str):
            textNumber = argNumber
            if (argNumber.find('%') != -1):
                argNumber = argNumber.strip('%')
            floatNumber = float(argNumber)
        else:
            textNumber = str(argNumber)
            floatNumber = argNumber

        if (fieldWidth != -1): # set field with
            textNumber = "{0:.{1}f}".format(floatNumber, fieldWidth)

        self.SetCellValue(row, col, textNumber)
        self.SetCellTextColour(row, col, self.GetColorByUpDown(floatNumber))

    def setCellFont(self, row, fontColor = wx.BLACK, fontSize = Const.FONT_SIZE_CONTENT, fontName = Const.FONT_NAME):
        # 设置字体格式
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(fontColor)
        font = wx.Font(fontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, fontName)
        attr.SetFont(font)
        self.SetRowAttr(row, attr)

    def checkSeparator(self, oldType, newType, row):
        if (oldType == newType):
            # reset as none-separator
            span = self.GetCellSize(row, 0)
            if (span[2] > 1):
                num_cols = len(self.Columns)
                for i in range(num_cols):
                    self.SetCellSize(row, i, 1, 1)
            return False

        num_cols = len(self.Columns)
        self.SetCellSize(row, 0, 1, num_cols)
        self.SetCellValue(row, 0, self.SeparatorTitles[newType])
        self.SetCellAlignment(row, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetCellBackgroundColour(row, 0, self.Const.COLOR_LIGHT_YELLOW)
        self.setCellFont(row, wx.BLACK, fontSize=self.Const.FONT_SIZE_SEPARATOR)

        return True

    # trick: return inner class via a function to pass the outer class instance
    def createSetGridFormat(self):
        gridObj = self
        class SetGridFormat():
            def __init__(self):
                self.firstUpdate = True
                self.toggleBackgroundColor = True

            def isFirstUpdate(self):
                return self.firstUpdate

            def finishUpdate(self):
                if not self.isFirstUpdate():
                    return False

                gridObj.AutoSizeColumns(setAsMin=True)

                # ignore performance; always update
                # self.firstUpdate = False
                self.toggleBackgroundColor = True

            def setFormat(self, row):
                if not self.isFirstUpdate():
                    return

                # 设置字体格式
                gridObj.setCellFont(row, wx.BLUE)

                for col in range(len(gridObj.Columns)):
                    horizAlign = wx.ALIGN_RIGHT
                    if (col == gridObj.COLUMN.NAME):
                        horizAlign = wx.ALIGN_LEFT
                    gridObj.SetCellAlignment(row, col, horizAlign, wx.ALIGN_CENTRE)

                backgroundColor = gridObj.GetDefaultCellBackgroundColour()
                if self.toggleBackgroundColor:
                    backgroundColor = gridObj.Const.COLOR_BACKGROUND_LIGHT_GRAY
                self.toggleBackgroundColor = not self.toggleBackgroundColor # toggle the background color

                for col in range(len(gridObj.Columns)):
                    gridObj.SetCellBackgroundColour(row, col, backgroundColor)



        return SetGridFormat()

    def updateInvestData(self, dataList):
        print("updateInvestData: {0}".format(len(dataList)))
        self.ClearGrid()

        lastType = None
        row = 0
        for data in dataList:
            if data == None:
                continue
            if (self.checkSeparator(lastType, data.originType, row)):
                row += 1
            lastType = data.originType

            self.SetCellValue(row, self.COLUMN.NAME, data.name)
            self.SetCellValue(row, self.COLUMN.CURRENT_PRICE, data.currentPrice)
            self.SetCellNumberAndColor(row, self.COLUMN.UPDOWN_PRICE, data.upDownPrice, fieldWidth = self.Const.UPDOWN_FIELD_WIDTH)
            self.SetCellNumberAndColor(row, self.COLUMN.UPDOWN_PERCENT, data.upDownPercent)
            self.SetCellValue(row, self.COLUMN.ORIGIN_PRICE, str(data.originPrice))

            originPercent = (float(data.currentPrice) - float(data.originPrice)) / float(data.originPrice) * 100.0
            self.SetCellNumberAndColor(row, self.COLUMN.ORIGIN_UPDOWN_PERCENT, "{:.2f}%".format(originPercent))

            self.setGridFormat.setFormat(row)

            row += 1

        self.setGridFormat.finishUpdate()

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
        if hasattr(self, 'investListCtrl'):
            self.investListCtrl.updateInvestData(dataList)
        if hasattr(self, 'investGrid'):
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


