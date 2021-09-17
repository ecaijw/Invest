import sys


class _constBase:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


class GlobalConst:
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

class tools:
    @staticmethod
    def convertExchangeRate():
        # =VLOOKUP(D2, M2: N5, 2, 0)
        for i in range(2, 300):
            print("=VLOOKUP(D{0}, M2: N5, 2, 0)".format(i))



if __name__ == "__main__":
    if (len(sys.argv) > 1):
        print('sys.argv: ' + sys.argv[1])
        if (sys.argv[1] == 'rate'):
            tools.convertExchangeRate()

