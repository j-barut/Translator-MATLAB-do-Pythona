from matlab_builtins import MATLAB_BUILTINS

class MatlabToPythonGenerator:
    def __init__(self):
        """
        Inicjalizacja generatora.
        indent_level śledzi aktualny poziom zagnieżdżenia kodu.
        """
        self.indent_level = 0
        self.function_translations = MATLAB_BUILTINS

    def get_indent(self):
        """Zwraca odpowiednią liczbę spacji dla obecnego poziomu wcięcia."""
        return "    " * self.indent_level

    def generate(self, ast):
        """
        Główna funkcja wejściowa. Na samej górze wygenerowanego pliku
        zawsze dodajemy import biblioteki numpy.
        """
        if not ast:
            return "# Błąd: Nie można wygenerować kodu Pythona z powodu błędów składniowych w MATLABie.\n"
        
        code = "import numpy as np\n\n"
        code += self.visit(ast)
        return code

    def visit(self, node):
        """
        Funkcja rekurencyjna, która sprawdza typ węzła i kieruje go
        do odpowiedniej metody obsługującej.
        """
        if isinstance(node, list):
            lines = []
            for statement in node:
                if statement == ('empty_statement',):
                    continue
                
                result = self.visit(statement)
                if result:
                    lines.append(result)
            return "\n".join(lines)

        if not isinstance(node, tuple):
            return str(node)

        node_type = node[0]

        method_name = f'visit_{node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Metoda wywoływana, gdy generator nie zna danego typu węzła."""
        return f"/* NIEZNANY WĘZEŁ: {node[0]} */"

    def visit_number(self, node):
        return str(node[1])

    def visit_id(self, node):
        return str(node[1])
    
    def visit_break(self, node):
        return f"{self.get_indent()}break"

    def visit_assign(self, node):
        var_name = node[1]
        if isinstance(var_name, tuple):
            var_name = self.visit(var_name)
            
        value = self.visit(node[2])
        return f"{self.get_indent()}{var_name} = {value}"

    def visit_binop(self, node):
        op = node[1]
        left = self.visit(node[2])
        right = self.visit(node[3])

        operators = {
            '.*': '*',
            '&&': 'and',
            '||': 'or',
            '~=': '!='
        }
        
        if op == '*':
            return f"np.dot({left}, {right})"
            
        elif op == '^':
            return f"np.linalg.matrix_power({left}, {right})"
            
        elif op == '.^':
            return f"({left} ** {right})"
            
        elif op in operators:
            return f"({left} {operators[op]} {right})"
            
        else:
            return f"({left} {op} {right})"

    def visit_unary(self, node):
        op = node[1]
        operand = self.visit(node[2])
        if op == '~':
            return f"np.logical_not({operand})"
        return f"({op}{operand})"

    def visit_transpose(self, node):
        operand = self.visit(node[1])
        return f"{operand}.T"

    def visit_matrix(self, node):
        rows = node[1]
        if not rows:
            return "np.array([])"
        
        python_rows = []
        for row in rows:
            elements = [self.visit(elem) for elem in row]
            python_rows.append("[" + ", ".join(elements) + "]")
            
        matrix_str = "[" + ", ".join(python_rows) + "]"
        return f"np.array({matrix_str})"

    def visit_for(self, node):
        iterator = node[1]
        range_node = node[2]
        body = node[3]

        start = self.visit(range_node[1])
        step = self.visit(range_node[2]) if range_node[2] else "1"
        stop = self.visit(range_node[3])

        loop_header = f"{self.get_indent()}for {iterator} in np.arange({start}, ({stop}) + ({step}), {step}):\n"
        
        self.indent_level += 1
        loop_body = self.visit(body)
        self.indent_level -= 1

        if not loop_body.strip():
            loop_body = f"{self.get_indent()}pass"

        return loop_header + loop_body

    def visit_function(self, node):
        name = node[1]
        args_node = node[2]
        body_node = node[3]
        
        return_vars = node[4] if len(node) > 4 else None
        
        args = [self.visit(arg) for arg in args_node] if args_node else []
        args_str = ", ".join(args)

        func_header = f"{self.get_indent()}def {name}({args_str}):\n"

        self.indent_level += 1
        func_body = self.visit(body_node)
        
        if return_vars:
            if isinstance(return_vars, list):
                ret_str = ", ".join([self.visit(r) if isinstance(r, tuple) else str(r) for r in return_vars])
                func_body += f"\n{self.get_indent()}return {ret_str}"
            else:
                ret_str = self.visit(return_vars) if isinstance(return_vars, tuple) else str(return_vars)
                func_body += f"\n{self.get_indent()}return {ret_str}"

        self.indent_level -= 1

        if not func_body.strip():
            func_body = f"{self.get_indent()}pass"

        return func_header + func_body

    def visit_function_call(self, node):
        func_name = node[1]
        args = node[2]

        args_str = ", ".join(
            self.visit(arg)
            for arg in args
        )

        translated_name = self.function_translations.get(
            func_name,
            func_name
        )

        return f"{translated_name}({args_str})"
    
    def visit_while(self, node):
        condition = self.visit(node[1])
        loop_header = f"{self.get_indent()}while {condition}:\n"
        
        self.indent_level += 1
        loop_body = self.visit(node[2])
        self.indent_level -= 1
        
        if not loop_body.strip():
            loop_body = f"{self.get_indent()}pass"
            
        return loop_header + loop_body

    def visit_if(self, node):
        condition = self.visit(node[1])
        code = f"{self.get_indent()}if {condition}:\n"
        
        self.indent_level += 1
        if_body = self.visit(node[2])
        if not if_body.strip():
            if_body = f"{self.get_indent()}pass"
        code += if_body + "\n"
        self.indent_level -= 1

        if len(node) > 3 and node[3]:
            for elseif_node in node[3]:
                elif_cond = self.visit(elseif_node[1])
                code += f"{self.get_indent()}elif {elif_cond}:\n"
                
                self.indent_level += 1
                elif_body = self.visit(elseif_node[2])
                if not elif_body.strip():
                    elif_body = f"{self.get_indent()}pass"
                code += elif_body + "\n"
                self.indent_level -= 1

        if len(node) > 4 and node[4]:
            code += f"{self.get_indent()}else:\n"
            
            self.indent_level += 1
            else_body = self.visit(node[4])
            if not else_body.strip():
                else_body = f"{self.get_indent()}pass"
            code += else_body + "\n"
            self.indent_level -= 1

        return code.rstrip()