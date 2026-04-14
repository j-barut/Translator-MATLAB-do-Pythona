
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
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | for_loop
                 | while_loop
                 | function_declaration
                 | expression_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression opt_semi'''
    p[0] = p[1]

def p_opt_semi(p):
    '''opt_semi : SEMI
                | empty'''
    pass

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI
                  | ID ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_empty(p):
    'empty :'
    pass

# ---------------- IF ----------------

def p_if_statement(p):
    '''if_statement : IF expression statement_list END
                    | IF expression statement_list ELSE statement_list END
                    | IF expression statement_list elseif_list END
                    | IF expression statement_list elseif_list ELSE statement_list END'''
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
    '''elseif_list : elseif_list elseif_clause
                   | elseif_clause'''
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

# ---------------- FUNCTIONS ----------------

def p_function_declaration(p):
    '''function_declaration : FUNCTION return_vars ASSIGN ID LPAREN arg_list RPAREN statement_list END
                            | FUNCTION ID LPAREN arg_list RPAREN statement_list END'''
    if len(p) == 10:
        # FUNCTION return_vars = ID(args) body END
        p[0] = ('function', p[4], p[6], p[8], p[2])
    else:
        # FUNCTION ID(args) body END
        p[0] = ('function', p[2], p[4], p[6], None)

def p_return_vars(p):
    '''return_vars : ID
                   | LBRACKET id_list RBRACKET'''
    if len(p) == 2:
        p[0] = [p[1]]   # zawsze lista
    else:
        p[0] = p[2]

def p_id_list(p):
    '''id_list : ID
               | id_list COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_arg_list(p):
    '''arg_list :
                | arguments'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]


def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# ---------------- EXPRESSIONS ----------------

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DOTMUL expression
                  | expression DIV expression
                  | expression DOTDIV expression
                  | expression POW expression
                  | expression DOTPOW expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression'''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = ('uminus', p[2])


def p_expression_transpose(p):
    '''expression : expression TRANSPOSE'''
    p[0] = ('transpose', p[1])


def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_id(p):
    '''expression : ID'''
    p[0] = ('id', p[1])


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])


def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ('string', p[1])

def p_expression_range(p):
    '''expression : range_expression'''
    p[0] = p[1]

# ---------------- FUNCTION CALL ----------------
def p_function_call(p):
    '''function_call : ID LPAREN arg_list RPAREN'''
    p[0] = ('call', p[1], p[3])


def p_expression_function_call(p):
    '''expression : function_call'''
    p[0] = p[1]

# ---------------- MATRIX ----------------
def p_matrix(p):
    '''matrix : LBRACKET RBRACKET
              | LBRACKET row_list RBRACKET'''
    if len(p) == 3:
        p[0] = ('matrix', [])
    else:
        p[0] = ('matrix', p[2])


def p_expression_matrix(p):
    '''expression : matrix'''
    p[0] = p[1]

def p_row_list(p):
    '''row_list : row
                | row_list SEMI row'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_row(p):
    '''row : expression_list'''
    p[0] = p[1]


def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# ---------------- ERROR ----------------

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")