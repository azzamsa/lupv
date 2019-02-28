from collections import OrderedDict


class MyDict(OrderedDict):
    def __missing__(self, key):
        val = self[key] = MyDict()
        return val
