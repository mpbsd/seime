from .regx import REGX


class DATE:

    def __init__(self, dstr):
        self.str = dstr
        self.D = self.__d()
        self.M = self.__m()
        self.Y = self.__y()
        self.iso = self.__isofmt()

    def __exists(self):
        if REGX["date"].match(self.str):
            fmt = True
        else:
            fmt = False
        return fmt

    def __d(self):
        if self.__exists():
            D = int(REGX["date"].sub(r"\1", self.str))
        else:
            D = 0
        return D

    def __m(self):
        if self.__exists():
            M = int(REGX["date"].sub(r"\3", self.str))
        else:
            M = 0
        return M

    def __y(self):
        if self.__exists():
            Y = int(REGX["date"].sub(r"\4", self.str))
        else:
            Y = 0
        return Y

    def __isofmt(self):
        if self.__exists():
            ret = int(REGX["date"].sub(r"\4\3\1", self.str))
        else:
            ret = 0
        return ret

    def __repr__(self):
        return self.str
