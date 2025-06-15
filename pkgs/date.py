from .regx import REGX


class DATE:

    def __init__(self, dstr):
        self.str = dstr
        self.iso = self.__isofmt()

    def __exists(self):
        if REGX["date"].match(self.str):
            fmt = True
        else:
            fmt = False
        return fmt

    def __isofmt(self):
        if self.__exists():
            ret = int(REGX["date"].sub(r"\4\3\1", self.str))
        else:
            ret = 0
        return ret

    def __repr__(self):
        return self.str
