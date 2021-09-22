import datetime
import copy
from urllib.request import *
from bs4 import BeautifulSoup
import re

import tools
from tools import *


def crawlYueGangAoIndex(originData):
    url = r"https://www.bocigroup.com/web/Inner/Inner/309"

    try:
        print("start: " + url)
        response = urlopen(url, timeout = 30)
        print("done: urlopen")
        html = response.read()
        print("done: read")
    except Exception as e:
        print(e)
        return None

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table')
    netIndex = 0
    if len(tables) >= 1:
        table = tables[0]
        rows = table.find_all('tr')
        if len(rows) >= 1:
            row = rows[1]
            cols = row.find_all('td')
            if len(cols) >= 1:
                col = cols[2]
                spans = col.find_all('span')
                if len(spans) >= 1:
                    span = spans[1]
                    content = span.contents[0]
                    netIndex = float(content)
    print(netIndex)
    investData = copy.deepcopy(originData)
    investData.name = "粤港澳大湾区指数"
    investData.currentPrice = str(netIndex)
    upDownPrice = netIndex - investData.originPrice
    investData.upDownPrice = "{:.2f}".format(upDownPrice)
    investData.upDownPercent = "{:.2f}%".format(upDownPrice / investData.originPrice * 100.0)

    return investData

class InvestData():
    isDeprecated: bool

    class InvestType(tools._constBase): pass
    INVEST = InvestType()
    INVEST.TYPE_STOCK = 1
    INVEST.TYPE_YUEGANGAO_INDEX = 2
    INVEST.TYPE_FUND = 3
    INVEST.TYPE_INDEX = 4
    INVEST.TYPE_FOREIGN_INDEX = 5

    def __init__(self):

        self.crawlPriceTime = re.compile("([^.]*).(\d+)").match("{0}".format(datetime.datetime.now())).group(1)
        self.originType = ""
        self.originId = "" # 股票的id
        self.originPrice = ""
        self.name = ""
        self.currentPrice = 0.0
        self.upDownPrice = 0.0
        self.upDownPercent = 0.0
        self.isDeprecated = False

class InvestDataIndex(InvestData):
    def __init__(self):
        super().__init__()

class InvestDataStock(InvestData):
    def __init__(self):
        super().__init__()

class InvestDataFund(InvestData):
    def __init__(self):
        super().__init__()

class InvestForeignDataIndex(InvestData):
    def __init__(self):
        super().__init__()

class CrawlPriceSina():
    def __init__(self):
        pass

    def crawlAll(self, originData, dataType):
        dataList = []

        url = r"https://hq.sinajs.cn/?list="
        idList = None
        for item in originData.getOriginDataList():
            if item.originType != dataType:
                continue
            originId = item.originId
            if (idList == None):
                idList = originId
            else:
                idList = idList + "," + originId
        url += idList

        try:
            print("start: " + url)
            response = urlopen(url, timeout = 30)
            print("done: urlopen")
            responseStr = str(response.read(), encoding="gb2312")
            print(responseStr)
        except Exception as e:
            print(e)
            return dataList

        strList = responseStr.split('\n')
        for item in strList:
            if len(item) == 0:
                continue
            investData = self.crawlOnePrice(item, originData)
            dataList.append(investData)

        print("done: read")
        return dataList

    def getPercentString(str):
        return re.compile("([^.]*.[\d+]{0,2}).*").match(str).group(1) + '%'

    def crawlOnePrice(self, str, originData):
        pass

'''
# https://vlqyus11b5.feishu.cn/docs/doccneDI00VlQ2a6NXSUg30wJwe#
# var hq_str_rt_hk01810 = "XIAOMI-W,小米集团－Ｗ,
# 29.600,30.000,30.450,29.600,30.000,0.000,0.000,30.000,30.050,4361075432.840,
# 145087985,29.835,0.000,35.900,12.300,2021/06/04,15:07:32,30|3,N|Y|Y,0.000|0.000|0.000,0|||0.000|0.000|0.000, |0,Y";
# 1. 股价：https://hq.sinajs.cn/?list=rt_hk01810 //可以同时查多个，港美股返回格式不太一样，rt表示实时，美股是gb_xxxx
https://hq.sinajs.cn/?list=rt_hk01810
var hq_str_rt_hk01810="XIAOMI-W,小米集团－Ｗ,27.000,26.700,27.100,26.250,26.650,-0.050,-0.187,26.600,26.650,3303365994.160,124458041,26.471,0.000,35.900,14.420,2021/07/12,15:55:57,30|3,N|Y|Y,0.000|0.000|0.000,0|||0.000|0.000|0.000, |0,Y";

港股的格式
- var hq_str_rt_hk01810="
- XIAOMI-W,
1: 小米集团－Ｗ,
2: 今日开盘价
3: 昨日收盘价
4: 今日最高价
5: 今日最低价
6: 当前价格
7: 涨跌幅
8: 涨跌百分比

美股的格式
var hq_str_gb_bili="
1：哔哩哔哩,
2：106.9800, 当前价格
2：0.22,     涨跌百分比
3：2021-07-13 09:30:14,  价格时间
4：0.2400,   涨跌幅
5：107.3400, 今日开盘价
108.3400,    今日最高价
104.4600,   今日最低价
157.6600,  52周最高
38.5400,   52周最低
2363779,4403082,41119081849,-1.35,--,0.00,0.00,0.00,0.00,384362328,0,107.3000,0.30,0.32,Jul 12 07:59PM EDT,Jul 12 04:00PM EDT,106.7400,55994,1,2021,251405483.0000,108.3443,106.7300,6016591.4515,106.9800";

'''
class CrawlStockPrice(CrawlPriceSina):
    class PriceIndex(tools._constBase): pass
    # init constants
    HK_STOCK = PriceIndex()
    HK_STOCK.ID = 1
    HK_STOCK.NAME = 2
    HK_STOCK.CURRENT_PRICE = 7
    HK_STOCK.UPDOWN_PRICE = 8
    HK_STOCK.UPDOWN_PERCENT = 9
    HK_STOCK.TODAY_OPEN = 3
    HK_STOCK.LAST_CLOSE = 4
    HK_STOCK.TODAY_HIGH = 5
    HK_STOCK.TODAY_LOW = 6

    US_STOCK = PriceIndex()
    US_STOCK.ID = 1
    US_STOCK.NAME = 2
    US_STOCK.CURRENT_PRICE = 3
    US_STOCK.PRICE_TIME = 5
    US_STOCK.UPDOWN_PRICE = 6
    US_STOCK.UPDOWN_PERCENT = 4
    US_STOCK.TODAY_OPEN = 7
    US_STOCK.LAST_CLOSE = 23  # should modify reg expression
    US_STOCK.TODAY_HIGH = 8
    US_STOCK.TODAY_LOW = 9

    def __init__(self):
        pass

    def crawlAll(self, originData):
        return CrawlPriceSina.crawlAll(self, originData, InvestData.INVEST.TYPE_STOCK)

    def crawlOnePrice(self, str, originData):
        investData : InvestData = None
        # 尝试：港股的股票格式
        m = re.compile('var hq_str_(.*)="[^,]*,([^,]*),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),(\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),.*').match(str)
        if (m == None or m.group(0) == None):
            # 尝试：美股的股票格式
            m = re.compile('var hq_str_(.*).*="([^,]*),(\d+.\d+),([-]?\d+.\d+),([^,]*),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),.*').match(str)
            if (m == None or m.group(0) == None):
                print("Error when parse: {0}".format(str))
                return None
            print("{0}, 实时价格[{1}] 涨跌幅[{2}] 涨跌百分比[{3}]".format(m.group(CrawlStockPrice.US_STOCK.NAME),
                                                              m.group(CrawlStockPrice.US_STOCK.CURRENT_PRICE),
                                                              m.group(CrawlStockPrice.US_STOCK.UPDOWN_PRICE),
                                                              m.group(CrawlStockPrice.US_STOCK.UPDOWN_PERCENT)))
            stockId = m.group(CrawlStockPrice.US_STOCK.ID)
            investData = copy.deepcopy(originData.findItemById(stockId))

            investData.name = m.group(CrawlStockPrice.US_STOCK.NAME)
            investData.currentPrice = m.group(CrawlStockPrice.US_STOCK.CURRENT_PRICE)
            investData.upDownPrice = m.group(CrawlStockPrice.US_STOCK.UPDOWN_PRICE)
            investData.upDownPercent = CrawlStockPrice.getPercentString(m.group(CrawlStockPrice.US_STOCK.UPDOWN_PERCENT))
        else:
            print("{0}, 实时价格[{1}] 涨跌幅[{2}] 涨跌百分比[{3}]".format(m.group(CrawlStockPrice.HK_STOCK.NAME),
                                                              m.group(CrawlStockPrice.HK_STOCK.CURRENT_PRICE),
                                                              m.group(CrawlStockPrice.HK_STOCK.UPDOWN_PRICE),
                                                              m.group(CrawlStockPrice.HK_STOCK.UPDOWN_PERCENT)))
            stockId = m.group(CrawlStockPrice.HK_STOCK.ID)
            investData = copy.deepcopy(originData.findItemById(stockId))

            investData.name = m.group(CrawlStockPrice.HK_STOCK.NAME)
            investData.currentPrice = m.group(CrawlStockPrice.HK_STOCK.CURRENT_PRICE)
            investData.upDownPrice = m.group(CrawlStockPrice.HK_STOCK.UPDOWN_PRICE)
            investData.upDownPercent = CrawlStockPrice.getPercentString(m.group(CrawlStockPrice.HK_STOCK.UPDOWN_PERCENT))
        return investData

'''
http://hq.sinajs.cn/list=f_161903,f_450009,f_519736
var hq_str_f_161903="万家行业优选混合(LOF),2.3947,6.1884,2.3357,2021-08-04,79.0294";
var hq_str_f_450009="国富中小盘股票,2.684,3.698,2.676,2021-08-04,22.3521";
var hq_str_f_519736="交银新成长混合,4.41,4.81,4.41,2021-08-04,35.5226";

（今天）单位净值（元）,累计净值（元）,（昨天）单位净值（元），日期，基金总份额(亿份)
'''
class CrawlFundPrice(CrawlPriceSina):
    class PriceIndex(tools._constBase): pass
    # init constants
    FUND = PriceIndex()
    FUND.ID = 1
    FUND.NAME = 2
    FUND.CURRENT_PRICE = 3
    FUND.ACCUM_VALUE = 4
    FUND.LAST_CLOSE = 5
    FUND.DATE = 6
    FUND.TOTAL_SHRE = 7

    def __init__(self):
        pass

    def crawlAll(self, originData):
        return CrawlPriceSina.crawlAll(self, originData, InvestData.INVEST.TYPE_FUND)

    def crawlOnePrice(self, str, originData):
        investData : InvestData = None
        # var hq_str_f_161903="万家行业优选混合(LOF),2.3947,6.1884,2.3357,2021-08-04,79.0294";
        m = re.compile('var hq_str_(.*)="([^,]*),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),([^,]*),([-]?\d+.\d+).*').match(str)
        if (m != None and m.group(0) != None):
            stockId = m.group(CrawlFundPrice.FUND.ID)
            investData = copy.deepcopy(originData.findItemById(stockId))

            investData.name = m.group(CrawlFundPrice.FUND.NAME)
            investData.currentPrice = m.group(CrawlFundPrice.FUND.CURRENT_PRICE)
            lastClose = m.group(CrawlFundPrice.FUND.LAST_CLOSE)
            investData.upDownPrice = (float)(investData.currentPrice) - float(lastClose)
            investData.upDownPercent = "{:.2f}%".format(investData.upDownPrice / float(investData.currentPrice) * 100.0)
        return investData

class CrawlIndexPrice(CrawlPriceSina):
    class PriceIndex(tools._constBase): pass
    # init constants
    INDEX = PriceIndex()
    INDEX.ID = 1
    INDEX.NAME = 2
    INDEX.CURRENT_PRICE = 5
    INDEX.LAST_CLOSE = 4

    def __init__(self):
        pass

    def crawlAll(self, originData):
        return CrawlPriceSina.crawlAll(self, originData, InvestData.INVEST.TYPE_INDEX)

    def crawlOnePrice(self, str, originData):
        investData : InvestData = None
        # var hq_str_sh000001="上证指数,3465.4842（今开）,3466.5491（昨收）,3458.2277（收盘）,3466.3904（最高）,3436.9317（最低）,
        # 0,0,336824400,516406643136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2021-08-06,15:13:49,00,";
        m = re.compile('var hq_str_(.*)="([^,]*),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+),([^,]*),([-]?\d+.\d+).*').match(str)
        if (m != None and m.group(0) != None):
            stockId = m.group(CrawlIndexPrice.INDEX.ID)
            investData = copy.deepcopy(originData.findItemById(stockId))

            investData.name = m.group(CrawlIndexPrice.INDEX.NAME)
            investData.currentPrice = m.group(CrawlIndexPrice.INDEX.CURRENT_PRICE)
            lastClose = m.group(CrawlIndexPrice.INDEX.LAST_CLOSE)

            investData.upDownPrice = (float)(investData.currentPrice) - float(lastClose)
            if (float(investData.currentPrice) == 0.0):
                # sometimes returned data is illegal
                # example: var hq_str_sz399001="深证成指,0.000,14350.647,0.000,
                investData.upDownPercent = 0.0 # avoid devide-by-zero error
            else:
                investData.upDownPercent = "{:.2f}%".format(investData.upDownPrice / float(investData.currentPrice) * 100.0)
        return investData


class CrawlIndexForeignPrice(CrawlPriceSina):
    class INDEX:
        ID = 1
        NAME = 2
        CURRENT_PRICE = 3
        UPDOWN_PRICE = 4
        UPDOWN_PERCENT = 5

    def __init__(self):
        pass

    def crawlAll(self, originData):
        return CrawlPriceSina.crawlAll(self, originData, InvestData.INVEST.TYPE_FOREIGN_INDEX)

    def crawlOnePrice(self, str, originData):
        investData: InvestData = None
        # var hq_str_int_nasdaq="纳斯达克,14860.18,24.42,0.16
        m = re.compile(
            'var hq_str_(.*)="([^,]*),([-]?\d+.\d+),([-]?\d+.\d+),([-]?\d+.\d+).*').match(str)
        if (m != None and m.group(0) != None):
            stockId = m.group(self.INDEX.ID)
            investData = copy.deepcopy(originData.findItemById(stockId))

            investData.name = m.group(self.INDEX.NAME)
            investData.currentPrice = m.group(self.INDEX.CURRENT_PRICE)
            investData.upDownPrice = m.group(self.INDEX.UPDOWN_PRICE)
            investData.upDownPercent = m.group(self.INDEX.UPDOWN_PERCENT) + '%'
        return investData

class OriginData():
    # type, id, price, deprecated, sell-price, sell-date
    DATA_TYPE = "类型"
    DATA_ID = "id"
    DATA_ORIGIN_PRICE = "原始价格"
    DATA_DEPRECATED = "过时的投资"

    ORIGIN_DATA_LIST = [
        [InvestData.INVEST.TYPE_STOCK, "rt_hk01810", 26.0],
        [InvestData.INVEST.TYPE_STOCK, "rt_hk03033", 8.26],
        [InvestData.INVEST.TYPE_STOCK, "rt_hk02369", 0.41],
        [InvestData.INVEST.TYPE_STOCK, "rt_hk09988", 225],
        [InvestData.INVEST.TYPE_STOCK, "rt_hk00700", 523],
        [InvestData.INVEST.TYPE_STOCK, "rt_hk02096", 13.0],
        [InvestData.INVEST.TYPE_STOCK, "gb_bili", 110.0],
        [InvestData.INVEST.TYPE_STOCK, "gb_tigr", 19.5],
        [InvestData.INVEST.TYPE_YUEGANGAO_INDEX, "粤港澳大湾区指数", 2300],
        [InvestData.INVEST.TYPE_YUEGANGAO_INDEX, "粤港澳大湾区指数", 1466],
        [InvestData.INVEST.TYPE_YUEGANGAO_INDEX, "粤港澳大湾区指数", 2100],
        [InvestData.INVEST.TYPE_FUND, "f_161903", 1.8974],  # 万家行业优选混合(LOF)
        [InvestData.INVEST.TYPE_FUND, "f_110007", 1.4159],  # 易方达稳健收益债券A
        [InvestData.INVEST.TYPE_FUND, "f_005664", 1.6115],  # 鹏扬景欣A
        [InvestData.INVEST.TYPE_INDEX, "sh000001", 3000],  # 上证指数
        [InvestData.INVEST.TYPE_INDEX, "sz399001", 14000],  # 深证成指
        [InvestData.INVEST.TYPE_FOREIGN_INDEX, "int_dji", 35000],  # 道琼斯
        [InvestData.INVEST.TYPE_FOREIGN_INDEX, "int_nasdaq", 14000],  # NASDAQ
        [InvestData.INVEST.TYPE_FOREIGN_INDEX, "int_sp500", 4400],  # SP500
        # deprecated investment
        [InvestData.INVEST.TYPE_FUND, "f_450009", 2.8584, True],  # 国富中小盘股票
        [InvestData.INVEST.TYPE_FUND, "f_519736", 4.0376, True],  # 交银新成长混合
    ]

    def __init__(self):
        super().__init__()
        self.originDataList = self.LoadOriginData()

    def LoadOriginData(self):
        jsonDataList = JsonTools.readAsJson(GlobalConst.currentDirFileName(GlobalConst.FILE_NAME_ORIGIN_DATA_JSON))
        originDataList = []
        for item in jsonDataList:
            originData = None
            dataType = item[OriginData.DATA_TYPE]
            if dataType == InvestData.INVEST.TYPE_STOCK:
                originData = InvestDataStock()
            elif dataType == InvestData.INVEST.TYPE_YUEGANGAO_INDEX:
                originData = InvestDataIndex()
            elif dataType == InvestData.INVEST.TYPE_FUND:
                originData = InvestDataFund()
            elif dataType == InvestData.INVEST.TYPE_INDEX:
                originData = InvestDataIndex()
            elif dataType == InvestData.INVEST.TYPE_FOREIGN_INDEX:
                originData = InvestForeignDataIndex()
            else:
                assert(False)
            originData.originType = dataType
            originData.originId = item[OriginData.DATA_ID]
            originData.originPrice = item[OriginData.DATA_ORIGIN_PRICE]
            originData.isDeprecated = (item[OriginData.DATA_DEPRECATED] == 'True')
            originDataList.append(originData)
        return originDataList

    def HelperLoadOriginData(self):
        originDataList = []
        for data in self.ORIGIN_DATA_LIST:
            originData = None
            if data[0] == InvestData.INVEST.TYPE_STOCK:
                originData = InvestDataStock()
            elif data[0] == InvestData.INVEST.TYPE_YUEGANGAO_INDEX:
                originData = InvestDataIndex()
            elif data[0] == InvestData.INVEST.TYPE_FUND:
                originData = InvestDataFund()
            elif data[0] == InvestData.INVEST.TYPE_INDEX:
                originData = InvestDataIndex()
            elif data[0] == InvestData.INVEST.TYPE_FOREIGN_INDEX:
                originData = InvestForeignDataIndex()
            else:
                assert (False)
            originData.originType = data[0]
            originData.originId = data[1]
            originData.originPrice = data[2]
            if (len(data) > 3):
                originData.isDeprecated = data[3]
            originDataList.append(originData)
        return originDataList

    # helper function to write json
    def HelperWriteJson(self):
        jsonData = []
        for data in self.ORIGIN_DATA_LIST:
            # type, id, price, deprecated, sell-price, sell-date
            oneData = dict()
            oneData[OriginData.DATA_TYPE] = data[0]
            oneData[OriginData.DATA_ID] = data[1]
            oneData[OriginData.DATA_ORIGIN_PRICE] = data[2]

            isDeprecated = False
            if (len(data) > 3):
                isDeprecated = data[3]
            oneData[OriginData.DATA_DEPRECATED] = str(isDeprecated)

            jsonData.append(oneData)
        JsonTools.writeJson(GlobalConst.currentDirFileName(GlobalConst.FILE_NAME_ORIGIN_DATA_JSON), jsonData)

    def getOriginDataList(self):
        return self.originDataList

    def findItemByType(self, type):
        for item in self.originDataList:
            if item.originType == type:
                return item
        return None

    def findItemById(self, id):
        for item in self.originDataList:
            if item.originId == id:
                return item
        return None

if __name__ == "__main__":
    OriginData().HelperWriteJson()
