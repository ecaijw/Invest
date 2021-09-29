# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib
import tools
from calcInvest import CalcInvestData
from investGridBase import InvestGridBase

class CalcInvestGrid(InvestGridBase):
    ROW_SIZE = 30
    ROW_MAX_NUMBER = 30

    def initConst(self):
        self.COLUMN = tools._constBase()
        self.COLUMN.NAME = 0
        self.COLUMN.REMAINING_AMOUNT = 1
        self.COLUMN.REMAINING_TOTAL_COST = 2
        self.COLUMN.REMAINING_TOTAL_PRICE = 3
        self.COLUMN.REMAINING_PRICE = 4
        self.COLUMN.TOTAL_PROFIT = 5
        self.COLUMN.CURRENT_PRICE = 6


        self.Columns = dict()
        self.Columns[self.COLUMN.NAME] = "产品"
        self.Columns[self.COLUMN.REMAINING_AMOUNT] = "剩余数量"
        self.Columns[self.COLUMN.REMAINING_TOTAL_COST] = "剩余总成本"
        self.Columns[self.COLUMN.REMAINING_TOTAL_PRICE] = "剩余总价值"
        self.Columns[self.COLUMN.REMAINING_PRICE] = "剩余净价值"
        self.Columns[self.COLUMN.TOTAL_PROFIT] = "总利润"
        self.Columns[self.COLUMN.CURRENT_PRICE] = "当前价格"

    def __init__(self, parent):
        InvestGridBase.__init__(self, parent)
        self.initConst()

        self.CreateGrid(self.ROW_MAX_NUMBER, len(self.Columns))

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])

    def updateInvestData(self, dataList):
        self.ClearGrid()

        row = 0
        data : CalcInvestData = None
        for data in dataList:
            self.SetCellValue(row, 0, data.productName)
            self.SetCellNumberAndColor(row, self.COLUMN.REMAINING_AMOUNT, data.remainingAmount)
            self.SetCellNumberAndColor(row, self.COLUMN.REMAINING_TOTAL_COST, data.remainingTotalCost)
            self.SetCellNumberAndColor(row, self.COLUMN.REMAINING_TOTAL_PRICE, data.remainingTotalPrice)
            self.SetCellNumberAndColor(row, self.COLUMN.REMAINING_PRICE, data.remainingPrice)
            self.SetCellNumberAndColor(row, self.COLUMN.TOTAL_PROFIT, data.totalProfit)
            self.SetCellNumberAndColor(row, self.COLUMN.CURRENT_PRICE, data.currentPrice)

            self.setGridFormat.setFormat(row)

            row += 1

        self.setGridFormat.finishUpdate()
