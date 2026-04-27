import ply.lex as lex

reserved = {
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'elseif': 'ELSEIF',
    'else': 'ELSE',
    'end': 'END',
    'function': 'FUNCTION'
}

tokens = [
    'ID', 'NUMBER', 'STRING', 'TRANSPOSE',
    'PLUS', 'MINUS', 'MUL', 'DOTMUL', 'DIV', 'DOTDIV', 'POW', 'DOTPOW',
    'ASSIGN', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMI', 'COLON'
] + list(reserved.values())

t_DOTMUL   = r'\.\*'
t_DOTDIV   = r'\./'
t_DOTPOW   = r'\.\^'
t_EQ       = r'=='
t_NEQ      = r'~='
t_LE       = r'<='
t_GE       = r'>='

t_PLUS     = r'\+'
t_MINUS    = r'-'
t_MUL      = r'\*'
t_DIV      = r'/'
t_POW      = r'\^'
t_TRANSPOSE= r"'"
t_ASSIGN   = r'='
t_LT       = r'<'
t_GT       = r'>'

t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA    = r','
t_SEMI     = r';'
t_COLON    = r':'

t_ignore = ' \t'

def t_STRING(t):
    r'("[^"]*")|(\'(?:[^\']|\'\')*\')'
    return t

def t_NUMBER(t):
    r'(?:\d+\.\d+|\.\d+|\d+\.|\d+)'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CONTINUATION(t):
    r'\.\.\..*\n'
    t.lexer.lineno += 1

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'SEMI'
    return t

def t_error(t):
    print(f"Błąd leksykalny: nierozpoznany znak '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
