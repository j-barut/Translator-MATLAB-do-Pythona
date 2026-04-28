
import ply.yacc as yacc
from lexer import tokens
from lexer import lexer

precedence = (
    ('left', 'COLON'),
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

def p_block(p):
    'block : statement_list'
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression opt_semi'''
    p[0] = p[1]

def p_opt_semi(p):
    '''opt_semi : SEMI
                | empty'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI
                  | ID ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_statement_empty(p):
    '''statement : SEMI'''
    p[0] = ('empty_statement',)

# ---------------- IF ----------------

def p_if_statement(p):
    '''if_statement : IF expression block END
                    | IF expression block ELSE block END
                    | IF expression block elseif_list END
                    | IF expression block elseif_list ELSE block END'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[3], None, None)

    elif len(p) == 7:
        if p[4] == 'ELSE':
            p[0] = ('if', p[2], p[3], None, p[5])
        else:
            p[0] = ('if', p[2], p[3], p[4], None)

    elif len(p) == 8:
        p[0] = ('if', p[2], p[3], p[4], p[6])

def p_elseif_list(p):
    '''elseif_list : elseif_list elseif_clause
                   | elseif_clause'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_elseif_clause(p):
    '''elseif_clause : ELSEIF expression block'''
    p[0] = ('elseif', p[2], p[3])

# ---------------- LOOPS ----------------

def p_for_loop(p):
    '''for_loop : FOR ID ASSIGN expression block END'''
    p[0] = ('for', p[2], p[4], p[5])

# def p_range_expression(p):
#     '''range_expression : expression COLON expression
#                         | expression COLON expression COLON expression'''
#     if len(p) == 4:
#         # start : end
#         p[0] = ('range', p[1], None, p[3])
#     else:
#         # start : step : end
#         p[0] = ('range', p[1], p[3], p[5])


def p_while_loop(p):
    '''while_loop : WHILE expression block END'''
    p[0] = ('while', p[2], p[3])

# ---------------- FUNCTIONS ----------------

def p_function_declaration(p):
    '''function_declaration : FUNCTION return_vars ASSIGN ID LPAREN arg_list RPAREN block END
                            | FUNCTION ID LPAREN arg_list RPAREN block END'''
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

def p_expression(p):
    '''expression : colon_expr'''
    p[0] = p[1]


# ---------- RANGE (:) ----------

def p_colon_expr(p):
    '''colon_expr : colon_expr COLON colon_expr
                  | relation'''
    if len(p) == 4:
        p[0] = ('range', p[1], None, p[3])
    else:
        p[0] = p[1]


# ---------- RELATIONS ----------

def p_relation(p):
    '''relation : relation EQ relation
                | relation NEQ relation
                | relation LT relation
                | relation LE relation
                | relation GT relation
                | relation GE relation
                | additive'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# ---------- ADD / SUB ----------

def p_additive(p):
    '''additive : additive PLUS additive
                | additive MINUS additive
                | multiplicative'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# ---------- MUL / DIV ----------

def p_multiplicative(p):
    '''multiplicative : multiplicative MUL multiplicative
                      | multiplicative DOTMUL multiplicative
                      | multiplicative DIV multiplicative
                      | multiplicative DOTDIV multiplicative
                      | power'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# ---------- POW ----------

def p_power(p):
    '''power : power POW power
             | power DOTPOW power
             | unary'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


# ---------- UNARY ----------

def p_unary(p):
    '''unary : MINUS unary %prec UMINUS
             | postfix'''
    if len(p) == 3:
        p[0] = ('uminus', p[2])
    else:
        p[0] = p[1]


# ---------- TRANSPOSE ----------

def p_postfix(p):
    '''postfix : postfix TRANSPOSE
               | primary'''
    if len(p) == 3:
        p[0] = ('transpose', p[1])
    else:
        p[0] = p[1]


# ---------- PRIMARY ----------

def p_primary(p):
    '''primary : ID
               | NUMBER
               | STRING
               | LPAREN expression RPAREN
               | matrix'''
    if len(p) == 2:
        if isinstance(p[1], int) or isinstance(p[1], float):
            p[0] = ('number', p[1])
        elif isinstance(p[1], str) and p.slice[1].type == 'STRING':
            p[0] = ('string', p[1])
        elif isinstance(p[1], str):
            p[0] = ('id', p[1])
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]

# ---------------- MATRIX ----------------
def p_matrix(p):
    '''matrix : LBRACKET RBRACKET
              | LBRACKET row_list RBRACKET'''
    if len(p) == 3:
        p[0] = ('matrix', [])
    else:
        p[0] = ('matrix', p[2])


# def p_expression_matrix(p):
#     '''expression : matrix'''
#     p[0] = p[1]

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
        print(f"Syntax error at token '{p.value}' (type={p.type}) line={p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            text = input(">>> ")
        except EOFError:
            break

        if not text:
            continue
        result = parser.parse(text, lexer=lexer)
        print(result)