# -*- coding: utf-8 -*-
from enum import IntEnum
from tools import *

class CalcInvestConst:
    FILE_NAME = r"D:\other_cjwlaptop\install\python\data\invest\investTest.xlsx"
    SHEET_NAME = "投资历史"


class COLUMNS(IntEnum):
    #  ['日期', '类型', '产品', '币种', '价格', '数量', '总价', '总价（人民币）', '汇率', '说明', None, None, None, '汇率', None]
    Date = 0
    Type = 1
    ProductName = 2
    MoneyType = 3
    Price = 4
    Amount = 5
    TotalPrice = 6
    TotalRMB = 7
    ExchangeRate = 8
    Comment = 9
    CurrentPrice = 10
    alreadyRevenue = 11


class CalcInvestData():
    def __init__(self):
        self.productName = ""
        self.remainingAmount = 0
        self.moneyType = ""
        self.totalCost = 0
        self.remainingCost = 0
        self.remainingTotalPriceRMB = 0
        self.remainingTotalPrice = 0
        self.totalSellMoney = 0
        self.totalProfit = 0
        self.totalProfitRMB = 0 # RMB
        self.currentPrice = 0
        self.comment = ""
        self.alreadyRevenueRMB = 0

class Product:
    def __init__(self, oneRow):
        super().__init__()
        self.rows = []
        self.rows.append(oneRow)
        self.productName = oneRow[COLUMNS.ProductName]


    def getName(self):
        return self.productName

    def addOneRow(self, oneRow):
        self.rows.append(oneRow)

    def printRows(self):
        for row in self.rows:
            print(row)

    def isLoan(self):
        return self.rows[0][COLUMNS.Type] == "抵押贷款"
    '''    
        计算剩余股票成本价的公式为：
        1) 最后卖股票得到的钱
        2) 所有买股票花的钱
        3) 减去所有卖出成交金额，最后除以剩余股票数量
        就是剩余股票的成本价。
    '''
    def calc(self) -> CalcInvestData:
        data: CalcInvestData = CalcInvestData()
        data.productName = self.productName

        totalBuyAmount = 0
        totalBuyMoney = 0
        totalSellAmount = 0
        averageSellPrice = 0
        data.moneyType = self.rows[0][COLUMNS.MoneyType]
        exchangeRate = self.rows[0][COLUMNS.ExchangeRate]
        for row in self.rows:
            # print(row)
            data.currentPrice = row[COLUMNS.CurrentPrice]
            price = row[COLUMNS.Price]
            if (price > 0): # sell
                data.remainingAmount -= row[COLUMNS.Amount]
                totalSellAmount += row[COLUMNS.Amount]
                data.totalSellMoney += row[COLUMNS.TotalPrice]
            else: # buy
                data.remainingAmount += row[COLUMNS.Amount]
                totalBuyAmount += row[COLUMNS.Amount]
                totalBuyMoney += row[COLUMNS.TotalPrice]
            if (row[COLUMNS.alreadyRevenue] != None):
                data.alreadyRevenueRMB += row[COLUMNS.alreadyRevenue] * exchangeRate
            data.comment = row[COLUMNS.Comment]
            if (data.comment == None):
                data.comment = ""
        totalBuyMoney *= -1

        if (totalBuyAmount == 0):
            averageBuyPrice = 0
        else:
            averageBuyPrice = totalBuyMoney / totalBuyAmount
        if (totalSellAmount > 0):
            averageSellPrice = data.totalSellMoney / totalSellAmount
        data.remainingTotalPrice = data.remainingAmount * data.currentPrice
        if (data.remainingAmount > 0):
            data.remainingCost = (totalBuyMoney - data.totalSellMoney) / data.remainingAmount
        data.totalCost = totalBuyMoney
        if (self.isLoan()):
            data.totalProfit = 0
        else:
            data.totalProfit = data.remainingTotalPrice + data.totalSellMoney - data.totalCost

        # unit is 万
        data.remainingTotalPriceRMB = data.remainingTotalPrice * exchangeRate
        data.totalProfitRMB = data.totalProfit * exchangeRate

        # print("{0}: 平均买入成本: {1}; 平均卖出价格: {2}".format(self.getName(), averageBuyPrice, averageSellPrice))
        return data

class ProductMgr:
    def __init__(self):
        super().__init__()
        self.productList = []

    def addOneRow(self, oneRow):
        # if (oneRow[COLUMNS.ProductName] != "佳兆业"):
        #     return
        product = self.findProduct(oneRow[COLUMNS.ProductName])
        if product == None:
            product = Product(oneRow)
            self.productList.append(product)
        else:
            product.addOneRow(oneRow)

    @staticmethod
    def sortDataListKey(data : CalcInvestData):
        return data.remainingTotalPriceRMB

    def calc(self):
        dataList = []
        p : Product
        for p in self.productList:
            # if (p.getName() != "哔哩哔哩"):
            #     continue
            # p.printRows()
            data = p.calc()
            dataList. append(data)

        dataList.sort(key=self.sortDataListKey, reverse=True)

        return dataList

    def findProduct(self, name) -> Product:
        for p in self.productList:
            if p.getName() == name:
                return p
        return None


class excel:

    def __init__(self):
        super().__init__()
        self.FirstRow = []

    def readExcel(self, productMgr : ProductMgr):
        import openpyxl

        workbook = openpyxl.load_workbook(CalcInvestConst.FILE_NAME, data_only=True)

        worksheet = workbook[CalcInvestConst.SHEET_NAME]

        rowNumber = 0
        for row in list(worksheet.rows):
            oneRow = [item.value for item in row]
            if (oneRow[COLUMNS.Date] == None):
                break # first empty row
            # print(oneRow)
            if (rowNumber == 0):
                for col in range(len(oneRow)):
                    self.FirstRow.append(oneRow[col])
            else:
                productMgr.addOneRow(oneRow)
            rowNumber += 1

class CalcInvestThreadWorker():
    def __init__(self):
        pass

    def work(self):
        print("{} work starts".format(self.__class__.__name__))

        productMgr = ProductMgr()
        excel().readExcel(productMgr)
        dataList = productMgr.calc()

        print("{} work ends".format(self.__class__.__name__))
        return dataList
