
import ply.yacc as yacc
from lexer import tokens
from lexer import lexer

precedence = (
    ('left', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DOTMUL',  'DIV', 'DOTDIV'),
    ('right', 'POW', 'DOTPOW'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE'),
)

def p_program(p) -> None:
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''
    statement : assignment
              | if_statement
              | for_loop
              | while_loop
              | function_declaration
              | expression_statement
    '''
    p[0] = p[1]

def p_expression_statement(p):
    '''
    expression_statement : expression opt_semi
    '''
    p[0] = p[1]

def p_opt_semi(p):
    '''
    opt_semi : SEMI
             | empty
    '''

def p_assignment(p):
    '''
    assignment : ID ASSIGN expression SEMI
               | ID ASSIGN expression
    '''
    p[0] = ('assign', p[1], p[3])

def p_empty(p):
    'empty :'
    pass

# ---------------- IF ----------------

def p_if_statement(p):
    '''
if_statement : IF expression statement_list END
             | IF expression statement_list ELSE statement_list END
             | IF expression statement_list elseif_list END
             | IF expression statement_list elseif_list ELSE statement_list END
    '''
    if len(p) == 5:
        # IF expr stmt_list END
        p[0] = ('if', p[2], p[3], None, None)

    elif len(p) == 7:
        if p[4] == 'ELSE':
            # IF expr stmt_list ELSE stmt_list END
            p[0] = ('if', p[2], p[3], None, p[5])
        else:
            # IF expr stmt_list elseif_list END
            p[0] = ('if', p[2], p[3], p[4], None)

    elif len(p) == 8:
        # IF expr stmt_list elseif_list ELSE stmt_list END
        p[0] = ('if', p[2], p[3], p[4], p[6])

def p_elseif_list(p):
    '''
    elseif_list : elseif_list elseif_clause
                | elseif_clause

    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_elseif_clause(p):
    '''elseif_clause : ELSEIF expression statement_list'''
    p[0] = ('elseif', p[2], p[3])

# ---------------- LOOPS ----------------

def p_for_loop(p):
    '''for_loop : FOR ID ASSIGN range_expression statement_list END'''
    p[0] = ('for', p[2], p[4], p[5])

def p_range_expression(p):
    '''range_expression : expression COLON expression
                        | expression COLON expression COLON expression'''
    if len(p) == 4:
        # start : end
        p[0] = ('range', p[1], None, p[3])
    else:
        # start : step : end
        p[0] = ('range', p[1], p[3], p[5])


def p_while_loop(p):
    '''while_loop : WHILE expression statement_list END'''
    p[0] = ('while', p[2], p[3])
