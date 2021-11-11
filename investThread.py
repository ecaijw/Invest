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
        self.crawlerList = []
        self.crawlerList.append(crawlData.CrawlMainLandIndexPrice())
        self.crawlerList.append(crawlData.CrawlFundPrice())
        self.crawlerList.append(crawlData.CrawlIndexPrice())
        self.crawlerList.append(crawlData.CrawlIndexForeignPrice())
        self.crawlerList.append(crawlData.CrawlHongKongIndexPrice())

    def work(self):
        print("{} work starts".format(self.__class__.__name__))
        dataList = []
        for crawler in self.crawlerList:
            stockDataList = crawler.crawlAll(self.originData)
            dataList += stockDataList

        indexData = crawlData.crawlYueGangAoIndex(self.originData.findItemByType(InvestData.INVEST.TYPE_YUEGANGAO_INDEX))
        dataList.append(indexData)

        print("{} work ends".format(self.__class__.__name__))
        return dataList
