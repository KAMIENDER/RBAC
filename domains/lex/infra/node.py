from enum import Enum


class NodeKind(Enum):
    Base = 'base'
    Num = 'Num'
    Id = 'Id'
    Str = 'Str'
    Operation = 'Operation'


class OperationCategory(Enum):
    Mul = 'Mul'
    Divide = 'Divide'
    Minus = 'Minus'
    Plus = 'Plus'
    Or = 'Or'
    And = 'And'
    Eq = 'Eq'
    St = 'St'
    Se = 'Se'
    Lt = 'Lt'
    Le = 'Le'


ExpressionOperations = [
    OperationCategory.Or.value, OperationCategory.And.value
]


TermOperations = [
    OperationCategory.St.value, OperationCategory.Se.value, OperationCategory.Lt.value, OperationCategory.Le.value,
    OperationCategory.Eq.value, OperationCategory
]

NumOperations = [
    OperationCategory.Mul.value, OperationCategory.Plus.value, OperationCategory.Minus.value,
    OperationCategory.Divide.value
]


class BaseNode(object):

    def __init__(self, value):
        self._kind = 'base'
        self._value = value
        self._extra = dict()

    @property
    def value(self):
        return self._value

    @property
    def kind(self):
        return self._kind

    def set_value(self, value):
        self._value = value

    def __str__(self):
        return f"kind: {self.kind}, value: {self.value}"

    def set_extra(self, key: str, value):
        self._extra[key] = value

    def get_extra(self, key: str):
        return self._extra.get(key, None)

    @property
    def extra(self):
        return self.extra


class Num(BaseNode):
    def __init__(self, value):
        super(Num, self).__init__(value)
        self._kind = 'Num'


class Id(BaseNode):

    def __init__(self, name: str):
        super(Id, self).__init__(None)
        self._kind = 'Id'
        self._name = name

    @property
    def name(self):
        return self._name


class Str(BaseNode):
    def __init__(self, value):
        super(Str, self).__init__(value)
        self._kind = 'Str'


class Operation(BaseNode):

    def __init__(self, category: str, left: BaseNode, right: BaseNode, value=None):
        super(Operation, self).__init__(None)
        self._kind = 'Operation'
        self._category = category
        self._left = left
        self._right = right
        if value:
            self._value = value

    @property
    def category(self):
        return self._category

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right
