# -*- coding: utf-8 -*-

import wx
import tools
import crawlData
from investGridBase import InvestGridBase

class InvestGrid(InvestGridBase):
    UPDOWN_FIELD_WIDTH = 2
    ROW_SIZE = 30
    ROW_MAX_NUMBER = 40
    SEPARATOR_TITLES_DEPRECATED = "过时的投资"

    def initConst(self):
        self.COLUMN = tools._constBase()
        self.COLUMN.NAME = 0
        self.COLUMN.CURRENT_PRICE = 1
        self.COLUMN.UPDOWN_PRICE = 2
        self.COLUMN.UPDOWN_PERCENT = 3
        self.COLUMN.ORIGIN_PRICE = 4
        self.COLUMN.ORIGIN_UPDOWN_PERCENT = 5
        self.COLUMN.DEPRECTAED = 6

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
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_MAINLAND_INDEX] = "大陆指数列表"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_FOREIGN_INDEX] = "国外指数列表"
        self.SeparatorTitles[crawlData.InvestData.INVEST.TYPE_HONGKONG_INDEX] = "香港指数列表"

    def __init__(self, parent):
        InvestGridBase.__init__(self, parent)
        self.initConst()

        self.CreateGrid(self.ROW_MAX_NUMBER, len(self.Columns))

        for row in range(self.GetNumberRows()):
            self.SetRowSize(row, self.ROW_SIZE)
        for col in range(len(self.Columns)):
            self.SetColLabelValue(col, self.Columns[col])

    def checkSeparator(self, data, lastData, row):
        newType = data.originType
        if (lastData != None) and (lastData.originType == newType):
            # reset as none-separator
            span = self.GetCellSize(row, 0)
            if (span[2] > 1):
                num_cols = len(self.Columns)
                for i in range(num_cols):
                    self.SetCellSize(row, i, 1, 1)
            return False

        if (lastData != None) and (lastData.isDeprecated == True):
            return False

        num_cols = len(self.Columns)
        self.SetCellSize(row, 0, 1, num_cols)
        if (data.isDeprecated == True):
            self.SetCellValue(row, 0, self.SEPARATOR_TITLES_DEPRECATED)
        else:
            self.SetCellValue(row, 0, self.SeparatorTitles[newType])

        self.SetCellAlignment(row, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetCellBackgroundColour(row, 0, self.COLOR_LIGHT_YELLOW)
        self.setCellFont(row, wx.BLACK, fontSize=self.FONT_SIZE_SEPARATOR)

        return True


    def updateInvestData(self, dataList):
        # move deprecated data to this list
        deprecatedDataList = []
        i = 0
        while i < len(dataList):
            data = dataList[i]
            if data.isDeprecated == True:
                deprecatedDataList.append(data)
                del dataList[i]
            else:
                i += 1

        self.ClearGrid()
        # update current data
        row = self.updateOneDataList(dataList, 0)
        # then update deprecated data
        self.updateOneDataList(deprecatedDataList, row)


    def updateOneDataList(self, dataList, startRow):
        print("updateOneDataList: {0}".format(len(dataList)))

        lastData = None
        row = startRow
        for data in dataList:
            if data == None:
                continue
            if (self.checkSeparator(data, lastData, row)):
                row += 1
            lastData = data

            self.SetCellValue(row, self.COLUMN.NAME, data.name)
            self.SetCellValue(row, self.COLUMN.CURRENT_PRICE, data.currentPrice)
            self.SetCellNumberAndColor(row, self.COLUMN.UPDOWN_PRICE, data.upDownPrice, fieldWidth = self.UPDOWN_FIELD_WIDTH)
            self.SetCellNumberAndColor(row, self.COLUMN.UPDOWN_PERCENT, data.upDownPercent)
            self.SetCellValue(row, self.COLUMN.ORIGIN_PRICE, str(data.originPrice))

            originPercent = (float(data.currentPrice) - float(data.originPrice)) / float(data.originPrice) * 100.0
            self.SetCellNumberAndColor(row, self.COLUMN.ORIGIN_UPDOWN_PERCENT, "{:.2f}%".format(originPercent))

            self.setGridFormat.setFormat(row)

            row += 1

        self.setGridFormat.finishUpdate()
        return row

