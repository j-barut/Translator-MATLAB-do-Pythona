import ply.lex as lex
import ply.yacc as yacc
import pprint
import textwrap
import lexer as matlab_lexer
import parser as matlab_parser

class MatlabParserTester:
    """
    Statyczna klasa testująca dla parsera języka MATLAB.
    Inicjalizuje lexer i parser tylko raz i udostępnia metody do testów.
    """
    
    _lexer = lex.lex(module=matlab_lexer)
    _parser = yacc.yacc(module=matlab_parser)

    @classmethod
    def run_test(cls, nazwa_testu: str, kod_matlab: str):
        """
        Wspólna metoda uruchamiająca skaner i parser dla podanego kodu.
        """
        kod_czysty = textwrap.dedent(kod_matlab).strip()
        
        print(f"\n{'='*60}")
        print(f"=== TEST: {nazwa_testu.upper()} ===")
        print(f"{'='*60}")
        print("KOD MATLAB:\n")
        print(kod_czysty)
        print("-" * 60)
        
        try:
            print("--- TOKENY (LEXER) ---")
            cls._lexer.input(kod_czysty)
            for tok in cls._lexer:
                print(f"Token: {tok.type:10} | Wartość: {tok.value:10} | Linia: {tok.lineno}")
            
            print("\n--- DRZEWO AST (PARSER) ---")
            result = cls._parser.parse(kod_czysty, lexer=cls._lexer)
            pprint.pprint(result, width=80, depth=None)
            
        except Exception as e:
            print(f"\n[BŁĄD] Wystąpił błąd podczas analizy składniowej: {e}")

    @staticmethod
    def test_operacje_macierzowe():
        """
        Test nr 1: Sprawdzenie poprawności parsowania definicji macierzy
        oraz rozróżnienia operatorów macierzowych (*) i tablicowych (.*).
        """
        kod = """
        A = [1, 2, 3; 4, 5, 6];
        B = [2, 2, 2; 3, 3, 3];
        C = A * B';
        D = A .* B;
        """
        MatlabParserTester.run_test("Operacje macierzowe", kod)

    @staticmethod
    def test_instrukcje_sterujace():
        """
        Test nr 2: Sprawdzenie poprawności konstrukcji bloku IF-ELSEIF-ELSE,
        pętli FOR z wykorzystaniem zakresu (tzw. colon expression) oraz bloków funkcji.
        """
        kod = """
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
        """
        MatlabParserTester.run_test("Struktury kontrolne i funkcje", kod)

    @classmethod
    def uruchom_wszystkie(cls):
        """
        Główna metoda uruchamiająca wszystkie testy po kolei.
        """
        cls.test_operacje_macierzowe()
        cls.test_instrukcje_sterujace()


if __name__ == "__main__":
    MatlabParserTester.uruchom_wszystkie()
