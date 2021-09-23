import sys
from tools import *
from calcInvest import CalcInvestThreadWorker
from crawlData import OriginDataHelper


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        print('sys.argv: ' + sys.argv[1])
        if (sys.argv[1] == 'rate'):
            GlobalTools.convertExchangeRate()
        elif (sys.argv[1] == 'calcInvest'):
            CalcInvestThreadWorker().work()
        elif (sys.argv[1] == 'writeOrigin'):
            OriginDataHelper().HelperWriteJson()
