import ply.lex as lex

tokens = (
    'NUM',
    'ID',
    'PLUS',
    'MINUS',
    'MUL',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQ',
    'LT',
    'ST',
    'LE',
    'SE',
    'AND',
    'OR'
)

# Regular expression rules for simple tokens
t_AND = r'\&'
t_OR = r'\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQ = r'='
t_LT = r'>'
t_ST = r'<'
t_LE = r'(>=|=>)'
t_SE = r'(<=|=<)'


# A regular expression rule with some action code
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.value = str(t.value)
    return t


lexer = lex.lex()


# if __name__ == '__main__':
#     test = MyLexer()
#     test.input("sdfs & 1")
#     while True:
#         token = test.token()
#         if not token:
#             break
#         print(token)
