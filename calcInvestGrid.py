# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib
import tools
import crawlData

class CalcInvestGrid(gridlib.Grid):
    class Const:
        ROW_SIZE = 30
        ROW_MAX_NUMBER = 30

    def initConst(self):
        self.COLUMN = tools._constBase()
        self.COLUMN.NAME = 0

        self.Columns = dict()
        self.Columns[self.COLUMN.NAME] = "产品"

    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        self.initConst()

        self.CreateGrid(self.Const.ROW_MAX_NUMBER, len(self.Columns))
        self.EnableEditing(False)

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.Const.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])


    def updateInvestData(self):
        self.ClearGrid()
        row = self.updateOneDataList()


    def updateOneDataList(self):
        row = 0
        for row in range(10):
            self.SetCellValue(row, 0, "name")

