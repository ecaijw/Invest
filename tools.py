import os
import json

class _constBase:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

class GlobalConst:
    FILE_NAME_ORIGIN_DATA_HELPER_JSON = r"..\data\invest\OriginDataHelper.json"
    FILE_NAME_ORIGIN_DATA_JSON = r"..\data\invest\OriginData.json"

    @staticmethod
    def currentDirFileName(fileName):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        return currentDir + '\\' + fileName

    # FCN, 股票, 指数, 公募基金, 私募基金, 私募股权, 债券, 借款, 固收类, 其它
    CALC_INVEST_TYPE_FCN = 1
    CALC_INVEST_TYPE_STOCK = 2
    CALC_INVEST_TYPE_INDEX = 3
    CALC_INVEST_TYPE_PUBLIC_FUND = 4
    CALC_INVEST_TYPE_PRIVATE_FUND = 5
    CALC_INVEST_TYPE_PRIVATE_EQUITY = 6
    CALC_INVEST_TYPE_BOND = 7
    CALC_INVEST_TYPE_LOAN = 8
    CALC_INVEST_TYPE_FIXED_INCOME = 9
    CALC_INVEST_TYPE_OTHER = 10
    CalcInvestType = {
        CALC_INVEST_TYPE_FCN : "FCN",
        CALC_INVEST_TYPE_STOCK : "股票",
        CALC_INVEST_TYPE_INDEX : "指数",
        CALC_INVEST_TYPE_PUBLIC_FUND : "公募基金",
        CALC_INVEST_TYPE_PRIVATE_FUND : "私募基金",
        CALC_INVEST_TYPE_PRIVATE_EQUITY : "私募股权",
        CALC_INVEST_TYPE_BOND : "债券",
        CALC_INVEST_TYPE_LOAN : "借款",
        CALC_INVEST_TYPE_FIXED_INCOME : "固收类",
        CALC_INVEST_TYPE_OTHER : "其它",
    }

class GlobalTools:
    @staticmethod
    def convertExchangeRate():
        # =VLOOKUP(D2, M2: N5, 2, 0)
        for i in range(2, 300):
            print("=VLOOKUP(D{0}, M2: N5, 2, 0)".format(i))

class JsonTools:
    @staticmethod
    def dictGetDataByKey(dictData, key):
        if JsonTools.hasKey(dictData, key):
            return dictData[key]
        return None

    @staticmethod
    def hasKey(dictData, key):
        for k in dictData:
            if k == key:
                return True
        return False

    @staticmethod
    def writeJson(filename, jsonData, mode = "w"):
        print("Writing Json:" + filename)

        with open(filename, mode,  encoding = 'utf-8') as file_obj:
            json.dump(jsonData, file_obj, ensure_ascii=False)
        print("Finish Writing!")

    @staticmethod
    def readAsJson(filename):
        with open(filename, 'r',  encoding = 'utf-8') as file_obj:
            jsonData = json.load(file_obj)
        return jsonData
