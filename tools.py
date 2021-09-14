import sys


class _constBase:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

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

