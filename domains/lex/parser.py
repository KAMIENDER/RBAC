import logging
from ply import yacc as yacc
from domains.lex.my_token import tokens

"""
    前后的顺序对解析而言是有影响的，
    越往下的优先级越高，
    （前一token不同）优先转换，
    （前一toekn相同）优先级看precedence
"""


def p_expression_and(p):
    'expr : expr AND expr'
    print(f'and: {p}')
    # p[0] = p[1] and p[3]


def p_expression_or(p):
    'expr : expr OR expr'
    print(f'or: {p}')
    # p[0] = p[1] or p[3]


def p_expression_le(p):
    'expr : term LE term'
    print(f'le: {p}')
    # p[0] = p[1] >= p[3]


def p_expression_lt(p):
    'expr : term LT term'
    print(f'lt: {p}')
    # p[0] = p[0] > p[3]


def p_expression_se(p):
    'expr : term SE term'
    print(f'se: {p}')
    # p[0] = p[1] <= p[3]


def p_expression_st(p):
    'expr : term ST term'
    print(f'st: {p}')
    # p[0] = p[1] < p[3]


def p_expression_eq(p):
    'expr : term EQ term'
    print(f'eq: {p[1], p[2], p[3]}')
    pass


# operate
def p_term_plus(p):
    'term : term PLUS term'
    print(f'plus: {p}')
    # p[0] = p[1] + p[3]


def p_term_minus(p):
    'term : term MINUS term'
    print(f'minus: {p}')
    # p[0] = p[1] - p[3]


def p_term_mul(p):
    'term : term MUL term'
    print(f'mul: {p}')
    # p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE term'
    print(f'divide: {p}')
    # p[0] = p[1] / p[3]


# expression combine
def p_paren(p):
    '''
    expr : LPAREN expr RPAREN
    term : LPAREN term RPAREN
    '''
    print(f'expr: {p}')
    # p[0] = p[2]


def p_term_num(p):
    'term : NUM'
    print(f'NUM: {p[1]}')
    p[0] = p[1]


def p_term_id(p):
    'term : ID'
    print(f'ID: {p[1]}')
    p[0] = p[1]


# error
def p_error(p):
    print(f"{p} Syntax error in input!")


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
    def __init__(self, debug: bool = False, level: int = logging.DEBUG, filename: str = "parse_log.txt"):
        self.debug = debug
        if debug:
            logging.basicConfig(
                level=level,
                filename=filename,
                filemode="w",
                format="%(filename)10s:%(lineno)4d:%(message)s"
            )
            self.logger = logging.getLogger()
            self.__parser = yacc.yacc(debug=True)
        else:
            self.__parser = yacc.yacc()

    def parse(self, in_str: str):
        if self.debug:
            self.__parser.parse(in_str, debug=self.logger)
            return
        self.__parser.parse(in_str)
        return

