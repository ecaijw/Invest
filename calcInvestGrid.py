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

        self.Columns = dict()
        self.Columns[self.COLUMN.NAME] = "产品"
        self.Columns[self.COLUMN.REMAINING_AMOUNT] = "剩余数量"

    def __init__(self, parent):
        InvestGridBase.__init__(self, parent)
        self.initConst()

        self.CreateGrid(self.ROW_MAX_NUMBER, len(self.Columns))

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])

    # print("剩余:\n"
    #       "  数量：{0:,}；\n "
    #       "  价值[{1:,}, {2:,.2f}] 成本[{3:,.2f}, {4:,.2f}]; \n"
    #       "利润: \n"
    #       "  剩余利润：{5:,.2f}; \n"
    #       "  已卖出利润：{6:,.2f}; \n"
    #       "  预计总利润：{7:,.2f}; \n"
    #       "平均买入价：{8:,.2f}；平均卖出价：{9:,.2f}".format(
    #     self.remainingAmount,
    #     self.remainingPrice,
    #     self.remainingTotalPrice,
    #     self.remainingCost,
    #     self.remainingTotalCost,
    #
    #     self.remainingTotalPrice - self.remainingTotalCost,
    #     self.totalProfit,
    #     (self.remainingTotalPrice - self.remainingTotalCost) + self.totalProfit,
    #
    #     averageBuyPrice,
    #     averageSellPrice
    # ))
    # if (data.remainingAmount > 0):
    #     print("{0:,.2f}".format((data.remainingTotalPrice - data.remainingTotalCost) * exchangeRate))
        # print("{0}".format(self.productName))
        # print("{0}: 剩余利润：{1:,.2f}, 剩余股数：{2:,.2f}".format(self.productName, self.remainingTotalPrice - self.remainingTotalCost, self.remainingAmount))


    def updateInvestData(self, dataList):
        self.ClearGrid()
        # self.rows.append(oneRow)
        # self.productName = oneRow[COLUMNS.ProductName]
        # self.remainingAmount = 0
        # self.remainingTotalCost = 0
        # self.remainingCost = 0
        # self.remainingTotalPrice = 0
        # self.remainingPrice = 0
        # self.totalProfit = 0 # RMB
        # self.currentPrice = 0
        row = 0
        data : CalcInvestData = None
        for data in dataList:
            self.SetCellValue(row, 0, data.productName)
            self.SetCellNumberAndColor(row, 1, data.remainingAmount)
            row += 1

