# -*- coding: utf-8 -*-

import wx
import wx.grid as gridlib
import tools
from calcInvest import CalcInvestData
from investGridBase import InvestGridBase

class CalcInvestGrid(InvestGridBase):
    ROW_SIZE = 30
    ROW_MAX_NUMBER = 50

    def initConst(self):
        self.COLUMN = tools._constBase()
        self.COLUMN.NAME = 0
        self.COLUMN.REMAINING_AMOUNT = 1
        self.COLUMN.REMAINING_ORIGINAL_PRICE = 2
        self.COLUMN.CURRENT_PRICE = 3
        self.COLUMN.MONEY_TYPE = 4
        self.COLUMN.REMAINING_TOTAL_PRICE_RMB = 5
        self.COLUMN.REMAINING_TOTAL_PRICE = 6
        self.COLUMN.TOTAL_SELL_MONEY = 7
        self.COLUMN.TOTAL_COST = 8
        self.COLUMN.TOTAL_PROFIT = 9
        self.COLUMN.TOTAL_PROFIT_RMB = 10
        self.COLUMN.NOTE = 11


        self.Columns = dict()
        self.Columns[self.COLUMN.NAME] = "产品"
        self.Columns[self.COLUMN.REMAINING_AMOUNT] = "剩余数量"
        self.Columns[self.COLUMN.REMAINING_ORIGINAL_PRICE] = "剩余成本价"
        self.Columns[self.COLUMN.CURRENT_PRICE] = "当前价格"
        self.Columns[self.COLUMN.MONEY_TYPE] = "单位"
        self.Columns[self.COLUMN.REMAINING_TOTAL_PRICE_RMB] = "剩余总价值(RMB)(万)"
        self.Columns[self.COLUMN.REMAINING_TOTAL_PRICE] = "剩余总价值"
        self.Columns[self.COLUMN.TOTAL_SELL_MONEY] = "卖出收入"
        self.Columns[self.COLUMN.TOTAL_COST] = "总成本"
        self.Columns[self.COLUMN.TOTAL_PROFIT] = "总利润"
        self.Columns[self.COLUMN.TOTAL_PROFIT_RMB] = "总利润(RMB)"
        self.Columns[self.COLUMN.NOTE] = "说明"

    def __init__(self, parent):
        InvestGridBase.__init__(self, parent)
        self.initConst()

        self.CreateGrid(self.ROW_MAX_NUMBER, len(self.Columns))

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])

    def updateSomeData(self, dataList, startRow, remaingAmountIs0):
        remainingTotalPriceRMB = 0
        totalProfitRMB = 0

        data : CalcInvestData = None
        for data in dataList:
            if (remaingAmountIs0 is False and int(data.remainingAmount) == 0):
                continue
            if (remaingAmountIs0 and int(data.remainingAmount) != 0):
                continue

            self.SetCellValue(startRow, 0, data.productName)
            self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_AMOUNT, data.remainingAmount / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_ORIGINAL_PRICE, data.remainingCost)
            self.SetCellValue(startRow, self.COLUMN.MONEY_TYPE, data.moneyType)
            self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_TOTAL_PRICE_RMB, int(data.totalCost) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_TOTAL_PRICE, int(data.remainingTotalPrice) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_TOTAL_PRICE_RMB, int(data.remainingTotalPriceRMB) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_SELL_MONEY, int(data.totalSellMoney) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_COST, int(data.totalCost) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_PROFIT, int(data.totalProfit) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_PROFIT_RMB, int(data.totalProfitRMB) / 10000)
            self.SetCellNumberAndColor(startRow, self.COLUMN.CURRENT_PRICE, data.currentPrice)
            self.SetCellValue(startRow, self.COLUMN.NOTE, data.comment)

            self.setGridFormat.setFormat(startRow)

            remainingTotalPriceRMB += data.remainingTotalPriceRMB
            if (data.productName != "小米0"):
                # NOT include xiaomi stock
                totalProfitRMB += data.totalProfitRMB
            startRow += 1
        return remainingTotalPriceRMB, totalProfitRMB, startRow;

    def updateInvestData(self, dataList):
        self.ClearGrid()

        (remainingTotalPriceRMB, totalProfitRMB, startRow) = self.updateSomeData(dataList, 0, False)

        # insert: TOTAL
        self.SetCellValue(startRow, 0, "合计")
        self.setGridFormat.setFormat(startRow)
        self.SetCellBackgroundColour(startRow, self.COLUMN.REMAINING_TOTAL_PRICE_RMB, self.COLOR_LIGHT_YELLOW)
        self.SetCellNumberAndColor(startRow, self.COLUMN.REMAINING_TOTAL_PRICE_RMB, remainingTotalPriceRMB / 10000)
        self.SetCellBackgroundColour(startRow, self.COLUMN.TOTAL_PROFIT_RMB, self.COLOR_LIGHT_YELLOW)
        self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_PROFIT_RMB, totalProfitRMB / 10000)
        self.SetCellValue(startRow, self.COLUMN.NOTE, "贷款利润为0；总利润(RMB)不包含小米0")

        startRow += 1

        (remainingTotalPriceRMB, totalProfitRMB, startRow) = self.updateSomeData(dataList, startRow, True)
        # insert: TOTAL
        self.SetCellValue(startRow, 0, "合计")
        self.setGridFormat.setFormat(startRow)
        self.SetCellBackgroundColour(startRow, self.COLUMN.TOTAL_PROFIT_RMB, self.COLOR_LIGHT_YELLOW)
        self.SetCellNumberAndColor(startRow, self.COLUMN.TOTAL_PROFIT_RMB, totalProfitRMB / 10000)
        self.SetCellValue(startRow, self.COLUMN.NOTE, "总利润(RMB)包含小米")

        self.setGridFormat.finishUpdate()
