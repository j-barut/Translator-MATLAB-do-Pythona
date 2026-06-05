from matlab_builtins import MATLAB_RESERVED_NAMES

class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.symbol_table = set()
        self.functions = set()
        self.in_loop = 0
        
        self.reserved_builtins = MATLAB_RESERVED_NAMES

    def analyze(self, ast):
        """Główna metoda uruchamiająca analizę."""
        self.errors = []
        self.symbol_table = set()
        self.functions = set()
        
        self._collect_functions(ast)
        
        self.visit(ast)
        return self.errors
    
    def _collect_functions(self, node):
        if isinstance(node, list):
            for statement in node:
                self._collect_functions(statement)
        elif isinstance(node, tuple):
            if node[0] == 'function':
                name = node[1]
                if isinstance(name, str):
                    self.functions.add(name)
            else:
                for item in node[1:]:
                    if isinstance(item, (tuple, list)):
                        self._collect_functions(item)

    def visit(self, node):
        if isinstance(node, list):
            for statement in node:
                self.visit(statement)
            return

        if not isinstance(node, tuple):
            return

        node_type = node[0]
        method_name = f'visit_{node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        """Dla węzłów, które przeglądamy w dół, ale nie mają specjalnej logiki."""
        for item in node[1:]:
            if isinstance(item, (tuple, list)):
                self.visit(item)

    def visit_assign(self, node):
        var_name = node[1]
        lineno = node[3] if len(node) > 3 else "?"
        
        if isinstance(var_name, str) and var_name in self.reserved_builtins:
            self.errors.append(f"Linia {lineno}: Błąd semantyczny - Próba nadpisania wbudowanej funkcji '{var_name}'.")
            
        self.visit(node[2])
        if isinstance(var_name, str): self.symbol_table.add(var_name)

    def visit_id(self, node):
        var_name = node[1]
        lineno = node[2] if len(node) > 2 else "?"
        
        if var_name not in self.symbol_table and var_name not in self.reserved_builtins and var_name not in self.functions:
            self.errors.append(f"Linia {lineno}: Błąd semantyczny - Użycie niezainicjowanej zmiennej '{var_name}'.")

    def elements(self, row_num):
        if row_num == 1:
            return "element"
        elif row_num < 5:
            return "elementy"
        else:
            return "elementów"

    def visit_matrix(self, node):
        rows = node[1]
        lineno = node[2] if len(node) > 2 else "?"
        
        if rows:
            first_row_length = len(rows[0])
            for i, row in enumerate(rows[1:], start=2):
                if len(row) != first_row_length:
                    self.errors.append(f"Linia {lineno}: Błąd semantyczny- Niespójne wymiary macierzy. Wiersz 1 ma {first_row_length} {self.elements(first_row_length)}, a wiersz {i} ma {len(row)} {self.elements(first_row_length)}.")
        
        self.generic_visit(node)

    def visit_for(self, node):
        iterator = node[1]
        
        if isinstance(iterator, str):
            self.symbol_table.add(iterator)
        
        self.in_loop += 1
        self.generic_visit(node)
        self.in_loop -= 1

    def visit_while(self, node):
        self.in_loop += 1
        self.generic_visit(node)
        self.in_loop -= 1

    def visit_break(self, node):
        lineno = node[1] if len(node) > 1 else "?"
        if self.in_loop == 0:
            self.errors.append(f"Linia {lineno}: Błąd semantyczny - Instrukcja 'break' użyta poza pętlą.")

    def visit_function(self, node):
        name = node[1]
        args_node = node[2]
        body_node = node[3]
        return_vars = node[4] if len(node) > 4 else None
        
        self.functions.add(str(name))
        
        previous_symbols = self.symbol_table.copy()
        
        if args_node:
            for arg in args_node:
                if isinstance(arg, tuple) and arg[0] == 'id':
                    self.symbol_table.add(arg[1])
                    
        if return_vars:
            if isinstance(return_vars, list):
                for rv in return_vars:
                    if isinstance(rv, tuple) and rv[0] == 'id':
                        self.symbol_table.add(rv[1])
                    elif isinstance(rv, str):
                        self.symbol_table.add(rv)
            elif isinstance(return_vars, tuple) and return_vars[0] == 'id':
                self.symbol_table.add(return_vars[1])
            elif isinstance(return_vars, str):
                self.symbol_table.add(return_vars)
                
        self.visit(body_node)
        
        self.symbol_table = previous_symbols

    def visit_function_call(self, node):
        func_name = node[1]
        args = node[2]
        lineno = node[3] if len(node) > 3 else "?"
        
        if func_name not in self.functions and func_name not in self.reserved_builtins:
            self.errors.append(f"Linia {lineno}: Błąd semantyczny - Wywołanie nieznanej funkcji '{func_name}'.")
            
        for arg in args:
            self.visit(arg)