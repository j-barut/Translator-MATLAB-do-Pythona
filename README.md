# Translator-MATLAB-do-Pythona

## 1. Informacje ogólne
Temat projektu: Kompilator źródło-źródło (translator) podzbioru języka MATLAB do języka Python.

Autorzy: Justyna Barut, Tomek Chmielowski

Dane kontaktowe: jbarut@student.agh.edu.pl, tchmielowski@student.agh.edu.pl

## 2. Założenia programu
Narzędzie to kompilator źródło-źródło, który analizuje podzbiór języka MATLAB (skupiający się na obliczeniach numerycznych i operacjach macierzowych), a następnie tłumaczy go na odpowiednie struktury i wywołania w języku Python.

Ogólne cele programu: Zapewnienie automatycznej konwersji skryptów MATLABa w celu ułatwienia migracji algorytmów naukowych do ekosystemu Pythona, bez konieczności ręcznego przepisywania całych bloków kodu.

Rodzaj translatora: Kompilator źródło-źródło (transpiler / konwerter).

Planowany wynik działania programu: Konwerter plików MATLABa (.m) do Pythona (.py). Wynikiem działania będzie wygenerowany, poprawny składniowo plik w języku Python, który automatycznie importuje bibliotekę numpy i wykorzystuje ją do realizacji zadeklarowanych wcześniej operacji macierzowych i tablicowych.

Planowany język implementacji: Python 3.12+.

Sposób realizacji skanera/parsera: Użycie generatora parserów PLY (Python Lex-Yacc), który bazuje na algorytmie LALR(1) i generuje tabele parsowania bezpośrednio w środowisku Pythona, bez konieczności używania zewnętrznych zależności.

## Tabela Tokenów (Analizator Leksykalny PLY)

Poniższa tabela przedstawia wszystkie tokeny obsługiwane przez lexer, wraz z odpowiadającymi im wyrażeniami regularnymi oraz krótkim opisem.

| Kategoria | Nazwa tokena | Znak / Wyrażenie regularne | Opis |
| :--- | :--- | :--- | :--- |
| **Słowa kluczowe** | `FOR` | `for` | Pętla *for* |
| | `WHILE` | `while` | Pętla *while* |
| | `IF` | `if` | Instrukcja warunkowa *if* |
| | `ELSEIF` | `elseif` | Alternatywa warunkowa *elseif* |
| | `ELSE` | `else` | Alternatywa *else* |
| | `END` | `end` | Zakończenie bloku instrukcji |
| **Identyfikatory** | `ID` | `[a-zA-Z][a-zA-Z0-9_]*` | Nazwy zmiennych (wymagana litera na początku) |
| **Literały** | `NUMBER` | `(?:\d+\.\d+\|\.\d+\|\d+\.\|\d+)` | Liczby całkowite i zmiennoprzecinkowe |
| | `STRING` | `("[^"]*")\|(\'(?:[^\']\|\'\')*\')` | Ciągi znaków z obsługą ucieczki `''` |
| **Operatory** | `PLUS` | `+` | Dodawanie |
| | `MINUS` | `-` | Odejmowanie |
| | `MUL` | `*` | Mnożenie |
| | `DOTMUL` | `.*` | Mnożenie tablicowe (element-wise) |
| | `DIV` | `/` | Dzielenie |
| | `DOTDIV` | `./` | Dzielenie tablicowe (element-wise) |
| | `POW` | `^` | Potęgowanie |
| | `DOTPOW` | `.^` | Potęgowanie tablicowe (element-wise) |
| | `TRANSPOSE` | `'` | Transpozycja |
| | `ASSIGN` | `=` | Przypisanie |
| **Relacje** | `EQ` | `==` | Równość |
| | `NEQ` | `~=` | Nierówność |
| | `LT` | `<` | Mniejsze |
| | `LE` | `<=` | Mniejsze lub równe |
| | `GT` | `>` | Większe |
| | `GE` | `>=` | Większe lub równe |
| **Delimitery** | `LPAREN` | `(` | Nawias okrągły otwierający |
| | `RPAREN` | `)` | Nawias okrągły zamykający |
| | `LBRACKET` | `[` | Nawias kwadratowy otwierający |
| | `RBRACKET` | `]` | Nawias kwadratowy zamykający |
| | `COMMA` | `,` | Przecinek (separator argumentów) |
| | `SEMI` | `;` (lub `\n`) | Średnik / Znak nowej linii (koniec instrukcji) |
| | `COLON` | `:` | Dwukropek (zakresy) |
| **Specjalne** | `CONTINUATION` | `\.\.\..*\n` | Trzy kropki ignorujące nową linię (kontynuacja kodu) |
