import logging
from ply import yacc as yacc
from domains.lex.node import *
from domains.lex.my_token import tokens

'''
    前后的顺序对解析而言是有影响的，
    越往下的优先级越高，
    （前一token不同）优先转换，
    （前一toekn相同）优先级看precedence
'''


def p_expression_le(p: yacc.YaccProduction):
    'expr : term LE term'
    print(f'le: {p}')
    p[0] = Operation(category='Le', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value >= p[3].value:
            p[0].set_value(True)


def p_expression_lt(p: yacc.YaccProduction):
    'expr : term LT term'
    print(f'lt: {p}')
    p[0] = Operation(category='Lt', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value > p[3].value:
            p[0].set_value(True)


def p_expression_se(p: yacc.YaccProduction):
    'expr : term SE term'
    print(f'se: {p}')
    p[0] = Operation(category='Se', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value <= p[3].value:
            p[0].set_value(True)


def p_expression_st(p: yacc.YaccProduction):
    'expr : term ST term'
    print(f'st: {p}')
    p[0] = Operation(category='St', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value < p[3].value:
            p[0].set_value(True)


def p_expression_eq(p: yacc.YaccProduction):
    'expr : term EQ term'
    print(f'eq: {p[1], p[2], p[3]}')
    p[0] = Operation(category='Eq', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value == p[3].value:
            p[0].set_value(True)


def p_expression_and(p: yacc.YaccProduction):
    'expr : expr AND expr'
    print(f'and: {p}')
    p[0] = Operation(category='And', left=p[1], right=p[3])
    if p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)
        if p[1].value is True and p[3].value is True:
            p[0].set_value(True)


def p_expression_or(p: yacc.YaccProduction):
    'expr : expr OR expr'
    print(f'or: {p}')
    p[0] = Operation(category='Or', left=p[1], right=p[3], value=False)
    if any([p[1].value is not None and p[1].value is True,
            p[3].value is not None and p[3].value is True]):
        p[0].set_value(True)
    elif p[1].value is not None and p[3].value is not None:
        p[0].set_value(False)


def p_term_plus(p: yacc.YaccProduction):
    '''
    term : term PLUS term
    '''
    print(f'plus: {p}')
    p[0] = Operation(category='Plus', left=p[1], right=p[3])
    if p[1].kind != 'Id' and p[3].kind != 'Id':
        if p[1].kind == p[3].kind:
            p[0].set_value(p[1].value + p[3].value)
        else:
            raise ValueError(f"different kind of inputs which can not be added: {p[1]}, {p[3]}")


# expression combine
def p_paren(p: yacc.YaccProduction):
    '''
    term : LPAREN term RPAREN
    expr : LPAREN expr RPAREN
    '''
    print(f'expr: {p}')
    p[0] = p[2]


def p_term_num(p: yacc.YaccProduction):
    'term : num'
    print(f'num: {p[1]}')
    p[0] = p[1]


def p_string_str(p: yacc.YaccProduction):
    'term : STR'
    print(f"STR: {p[1]}")
    p[0] = Str(p[1])


def p_term_mul(p: yacc.YaccProduction):
    '''
    num : num MUL num
    '''
    print(f'mul: {p}')
    p[0] = Operation(category='Mul', left=p[1], right=p[3])
    if p[1].kind != 'Id' and p[3].kind != 'Id':
        p[0].set_value(p[1].value * p[3].value)


def p_term_div(p: yacc.YaccProduction):
    'num : num DIVIDE num'
    print(f'divide: {p}')
    p[0] = Operation(category='Divide', left=p[1], right=p[3])
    if p[1].kind != 'Id' and p[3].kind != 'Id':
        p[0].set_value(p[1].value / p[3].value)


def p_term_minus(p: yacc.YaccProduction):
    'num : num MINUS num'
    print(f'minus: {p}')
    p[0] = Operation(category='Minus', left=p[1], right=p[3])
    if p[1].kind != 'Id' and p[3].kind != 'Id':
        p[0].set_value(p[1].value - p[3].value)


def p_num_num(p: yacc.YaccProduction):
    'num : NUM'
    print(f'NUM: {p[1]}')
    p[0] = Num(p[1])


def p_term_id(p: yacc.YaccProduction):
    'num : ID'
    print(f'ID: {p[1]}')
    p[0] = Id(p[1])


# error
def p_error(p: yacc.YaccProduction):
    raise SyntaxError(f"analyze tree fail: {p} Syntax error in input!")


'''
    越下优先级越高
    同一层同等优先级
'''
precedence = (
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIVIDE'),
)


class YaccAnalyzer():
    def __init__(self, debug: bool = False, level: int = logging.DEBUG, filename: str = "parse_log.txt",
                 filemode: str = 'w', format: str = "%(filename)10s:%(lineno)4d:%(message)s"):
        self.debug = debug
        if debug:
            logging.basicConfig(
                level=level,
                filename=filename,
                filemode=filemode,
                format=format
            )
            self.logger = logging.getLogger()
            self.__parser = yacc.yacc(debug=True)
        else:
            self.__parser = yacc.yacc()

    def parse(self, in_str: str):
        if self.debug:
            return self.__parser.parse(in_str, debug=self.logger)
        return self.__parser.parse(in_str)

    def ast_tree(self, in_str) -> BaseNode:
        return self.parse(in_str)


if __name__ == '__main__':

    test = YaccAnalyzer(debug=True).parse('a = "fsdf" + 1')
