class BaseNode(object):
    kind = 'base'

    def __init__(self, value):
        self.__value = value

    def value(self):
        return self.__value


class Number(BaseNode):
    kind = 'Num'


class Id(BaseNode):
    kind = 'Id'


class Str(BaseNode):
    kind = 'Str'


class Operation(BaseNode):
    kind = 'Operation'

    def __init__(self, category: str, left: BaseNode, right: BaseNode, value = None):
        self.__category = category
        self.__left = left
        self.__right = right
        if value:
            self.__value = value

    def category(self):
        return self.__category

    def left(self):
        return self.__left

    def right(self):
        return self.__right
