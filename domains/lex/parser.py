import logging
from ply import yacc as yacc
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
    # p[0] = p[1] >= p[3]


def p_expression_lt(p: yacc.YaccProduction):
    'expr : term LT term'
    print(f'lt: {p}')
    # p[0] = p[0] > p[3]


def p_expression_se(p: yacc.YaccProduction):
    'expr : term SE term'
    print(f'se: {p}')
    # p[0] = p[1] <= p[3]


def p_expression_st(p: yacc.YaccProduction):
    'expr : term ST term'
    print(f'st: {p}')
    # p[0] = p[1] < p[3]


def p_expression_eq(p: yacc.YaccProduction):
    'expr : term EQ term'
    print(f'eq: {p[1], p[2], p[3]}')
    pass


def p_expression_and(p: yacc.YaccProduction):
    'expr : expr AND expr'
    print(f'and: {p}')
    # p[0] = p[1] and p[3]


def p_expression_or(p: yacc.YaccProduction):
    'expr : expr OR expr'
    print(f'or: {p}')
    # p[0] = p[1] or p[3]


def p_term_plus(p: yacc.YaccProduction):
    '''
    term : term PLUS term
    '''
    print(f'plus: {p}')
    # p[0] = p[1] + p[3]


def p_term_mul(p: yacc.YaccProduction):
    '''
    term : term MUL term
    '''
    print(f'mul: {p}')
    # p[0] = p[1] * p[3]


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
    print(f"STR: {p}")
    p[0] = p[1]


def p_term_div(p: yacc.YaccProduction):
    'num : num DIVIDE num'
    print(f'divide: {p}')
    # p[0] = p[1] / p[3]


def p_term_minus(p: yacc.YaccProduction):
    'num : num MINUS num'
    print(f'minus: {p}')
    # p[0] = p[1] - p[3]


def p_num_num(p: yacc.YaccProduction):
    'num : NUM'
    print(f'NUM: {p[1]}')
    p[0] = p[1]


def p_term_id(p: yacc.YaccProduction):
    'num : ID'
    print(f'ID: {p}')
    p[0] = p[1]


# error
def p_error(p: yacc.YaccProduction):
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
            self.__parser.parse(in_str, debug=self.logger)
            return
        self.__parser.parse(in_str)
        return


if __name__ == '__main__':
    test = YaccAnalyzer(debug=True)
    test.parse('"sdfsdf"')
