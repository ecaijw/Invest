# -*- coding: utf-8 -*-
from enum import IntEnum

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

class Product:
    def __init__(self, oneRow):
        super().__init__()
        self.rows = []
        self.rows.append(oneRow)
        self.remainingAmount = 0
        self.remainingTotalCost = 0
        self.remainingCost = 0
        self.remainingTotalPrice = 0
        self.remainingPrice = 0
        self.totalProfit = 0 # RMB
        self.currentPrice = 29

    def getName(self):
        return self.rows[0][COLUMNS.ProductName]

    def addOneRow(self, oneRow):
        self.rows.append(oneRow)

    '''    
        计算剩余股票成本价的公式为：
        1) 最后卖股票得到的钱
        2) 所有买股票花的钱
        3) 减去所有卖出成交金额，最后除以剩余股票数量
        就是剩余股票的成本价。
    '''
    def calc(self):
        self.remainingAmount = 0
        self.remainingTotalPrice = 0
        self.totalProfit = 0 # RMB
        totalBuyAmount = 0
        totalBuyMoney = 0
        totalSellAmount = 0
        totalSellMoney = 0
        averageSellPrice = 0
        for row in self.rows:
            print(row)
            price = row[COLUMNS.Price]
            if (price > 0): # sell
                self.remainingAmount -= row[COLUMNS.Amount]
                totalSellAmount += row[COLUMNS.Amount]
                totalSellMoney += row[COLUMNS.TotalPrice]
            else: # buy
                self.remainingAmount += row[COLUMNS.Amount]
                totalBuyAmount += row[COLUMNS.Amount]
                totalBuyMoney += row[COLUMNS.TotalPrice]
        totalBuyMoney *= -1

        averageBuyPrice = totalBuyMoney / totalBuyAmount
        if (totalSellAmount > 0):
            averageSellPrice = totalSellMoney / totalSellAmount
            self.totalProfit = totalSellAmount * (averageSellPrice - averageBuyPrice)
        self.remainingPrice = self.currentPrice
        self.remainingTotalPrice = self.remainingAmount * self.remainingPrice
        self.remainingCost = averageBuyPrice
        self.remainingTotalCost = self.remainingAmount * self.remainingCost
        print("剩余:\n"
              "  数量：{0:,}；\n "
              "  价值[{1:,}, {2:,.2f}] 成本[{3:,.2f}, {4:,.2f}]; \n"
              "利润: \n"
              "  剩余利润：{5:,.2f}; \n"
              "  已卖出利润：{6:,.2f}; \n"
              "  预计总利润：{7:,.2f}; \n"
              "平均买入价：{8:,.2f}；平均卖出价：{9:,.2f}".format(
            self.remainingAmount,
            self.remainingPrice,
            self.remainingTotalPrice,
            self.remainingCost,
            self.remainingTotalCost,

            self.remainingTotalPrice - self.remainingTotalCost,
            self.totalProfit,
            (self.remainingTotalPrice - self.remainingTotalCost) + self.totalProfit,

            averageBuyPrice,
            averageSellPrice
        ))

class ProductMgr:
    def __init__(self):
        super().__init__()
        self.productList = []

    def addOneRow(self, oneRow):
        product = self.findProduct(oneRow[COLUMNS.ProductName])
        if product == None:
            product = Product(oneRow)
            self.productList.append(product)
        else:
            product.addOneRow(oneRow)

    def calc(self):
        p : Product
        for p in self.productList:
            p.calc()
            # if p.getName() == "新纽":
            #     p.calc()

    def findProduct(self, name) -> Product:
        for p in self.productList:
            if p.getName() == name:
                return p
        return None


class excel:
    class Const:
        FILE_NAME = r"D:\other_cjwlaptop\install\python\data\invest\test.xlsx"
        SHEET_NAME = "投资历史"

    def __init__(self):
        super().__init__()
        self.FirstRow = []

    def readExcel(self, productMgr):
        import openpyxl

        workbook = openpyxl.load_workbook(self.Const.FILE_NAME, data_only=True)

        worksheet = workbook[self.Const.SHEET_NAME]

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

class calcInvest():
    def __init__(self):
        self.productMgr = ProductMgr()

    def run(self):
        print("run start")

        excel().readExcel(self.productMgr)

        self.productMgr.calc()

        print("run done")
        pass

if __name__ == "__main__":
    calcInvest().run()