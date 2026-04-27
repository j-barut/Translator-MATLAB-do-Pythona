import ply.yacc as yacc
import pprint
from lexer import lexer
import parser as matlab_parser

class MatlabParserTester:
    def __init__(self):
        """
        Inicjalizacja testera. Budujemy parser na podstawie reguł 
        zdefiniowanych w module parser.py.
        """
        self.lexer = lexer
        self.parser = yacc.yacc(module=matlab_parser)

    def test_lexer(self, code, example_name=""):
        """
        Przepuszcza kod przez skaner (lexer) i wypisuje rozpoznane tokeny.
        Pozwala sprawdzić, czy wszystkie słowa kluczowe i operatory są dobrze cięte.
        """
        print(f"--- TEST SKANERA (LEXERA): {example_name} ---")
        self.lexer.input(code)
        for tok in self.lexer:
            print(f"Token: {tok.type:10} | Wartość: {tok.value:10} | Linia: {tok.lineno}")
        print("-" * 50 + "\n")

    def test_parser(self, code, example_name=""):
        """
        Przepuszcza kod przez parser i wypisuje wygenerowane 
        Drzewo Składni Abstrakcyjnej (AST).
        """
        print(f"--- TEST PARSERA (DRZEWO AST): {example_name} ---")
        result = self.parser.parse(code, lexer=self.lexer)
        
        pprint.pprint(result, width=80, depth=None)
        print("-" * 50 + "\n")

    def run_all_tests(self):
        """
        Główna metoda uruchamiająca zdefiniowane przykłady.
        """
        # PRZYKŁAD 1: Testowanie matematyki wektorowej i różnic w operatorach
        # Kluczowe dla translacji do numpy: rozróżnienie mnożenia macierzowego (*) 
        # od mnożenia tablicowego/element-wise (.*) oraz transpozycji (').
        example1 = '''
        A = [1, 2, 3; 4, 5, 6];
        B = [2, 2, 2; 3, 3, 3];
        C = A * B';
        D = A .* B;
        '''

        # PRZYKŁAD 2: Testowanie struktur sterujących i funkcji
        # Testuje budowę bloków IF-ELSEIF-ELSE, pętli FOR z zakresami (colon_expr) 
        # oraz poprawne parsowanie sygnatury funkcji MATLABa.
        example2 = '''
        function [res] = calculate_sum(n)
            res = 0;
            for i = 1:n
                if i < 5
                    res = res + i;
                elseif i == 5
                    res = res + 10;
                else
                    res = res - 1;
                end
            end
        end
        '''

        print("=== URUCHAMIANIE PRZYKŁADU 1 ===")
        print("KOD MATLAB:\n", example1.strip())
        self.test_lexer(example1, "Operacje Macierzowe")
        self.test_parser(example1, "Operacje Macierzowe")

        print("=== URUCHAMIANIE PRZYKŁADU 2 ===")
        print("KOD MATLAB:\n", example2.strip())
        self.test_lexer(example2, "Instrukcje i Funkcje")
        self.test_parser(example2, "Instrukcje i Funkcje")

if __name__ == "__main__":
    tester = MatlabParserTester()
    tester.run_all_tests()
