# -*- coding: utf-8 -*-
import crawlData
from crawlData import InvestData
from InvestThreadBase import InvestThreadBase

class InvestThread(InvestThreadBase):
    def getThreadWorkerClass(self):
        return InvestThreadWorker

class InvestThreadWorker():
    def __init__(self):
        self.originData = crawlData.OriginData()
        self.crawlMainLandIndexPrice = crawlData.CrawlMainLandIndexPrice()
        self.crawlFundPrice = crawlData.CrawlFundPrice()
        self.crawlIndexPrice = crawlData.CrawlIndexPrice()
        self.crawlIndexForeignPrice = crawlData.CrawlIndexForeignPrice()
        self.crawlHongKongIndexPrice = crawlData.CrawlHongKongIndexPrice()

    def work(self):
        print("{} work starts".format(self.__class__.__name__))
        dataList = []
        stockDataList = self.crawlMainLandIndexPrice.crawlAll(self.originData)
        dataList += stockDataList
        stockDataList = self.crawlFundPrice.crawlAll(self.originData)
        dataList += stockDataList
        stockDataList = self.crawlIndexPrice.crawlAll(self.originData)
        dataList += stockDataList
        stockDataList = self.crawlHongKongIndexPrice.crawlAll(self.originData)
        dataList += stockDataList
        stockDataList = self.crawlIndexForeignPrice.crawlAll(self.originData)
        dataList += stockDataList

        indexData = crawlData.crawlYueGangAoIndex(self.originData.findItemByType(InvestData.INVEST.TYPE_YUEGANGAO_INDEX))
        dataList.append(indexData)

        print("{} work ends".format(self.__class__.__name__))
        return dataList
