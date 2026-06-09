# Translator MATLAB → Python

## 1. Informacje ogólne

**Temat projektu:**  
Translator MATLAB do języka Python.

**Autorzy:**  
Justyna Barut  
Tomasz Chmielowski

**Kontakt:**  
jbarut@student.agh.edu.pl  
tchmielowski@student.agh.edu.pl

---

# 2. Założenia programu

## Cel projektu

Celem projektu jest stworzenie narzędzia umożliwiającego automatyczne tłumaczenie wybranej części języka MATLAB na równoważny kod w języku Python.

Translator pozwala na migrację prostych programów obliczeniowych, numerycznych oraz algorytmicznych z ekosystemu MATLAB do środowiska Python bez konieczności ręcznego przepisywania kodu.

Projekt obejmuje pełny proces kompilacji:

1. Analizę leksykalną (Lexer)
2. Analizę składniową (Parser)
3. Budowę drzewa AST
4. Analizę semantyczną
5. Generowanie kodu Python
7. Uruchomienia kodu Python

---

## Rodzaj translatora

Translator źródło–źródło (Source-to-Source Compiler, Transpiler).

Program nie wykonuje kodu MATLAB bezpośrednio.

Zamiast tego:

MATLAB

```matlab
A = [1,2;3,4];
B = A.^2;
disp(B);
```

jest tłumaczony do:

```python
import numpy as np

A = np.array([[1,2],[3,4]])
B = A ** 2
print(B)
```

---

## Planowany wynik działania programu

Wynikiem działania translatora jest:

- wygenerowany kod Python,
- automatyczne dodanie importu biblioteki NumPy,
- zachowanie semantyki operacji macierzowych MATLABa,
- możliwość natychmiastowego uruchomienia wygenerowanego kodu.

---

## Technologia implementacji

### Backend

- Python 3.14+
- PLY (Python Lex-Yacc)
- NumPy

### Frontend

- HTML5
- CSS3
- JavaScript
- CodeMirror 5

---

## Architektura programu

```
MATLAB Source Code
        │
        ▼
     Lexer
        │
        ▼
     Parser
        │
        ▼
       AST
        │
        ▼
Semantic Analyzer
        │
        ▼
Python Generator
        │
        ▼
 Python Source Code
```

---

# 3. Analiza leksykalna

Analizator leksykalny został zaimplementowany przy pomocy modułu `ply.lex`.

Jego zadaniem jest podział kodu źródłowego MATLAB na tokeny rozpoznawane przez parser.

---

## Tabela tokenów

| Kategoria | Token | RegEx / Symbol | Opis |
|------------|------------|------------|------------|
| Słowa kluczowe | FOR | for | pętla for |
| | WHILE | while | pętla while |
| | IF | if | instrukcja warunkowa |
| | ELSEIF | elseif | alternatywa warunkowa |
| | ELSE | else | blok else |
| | END | end | zakończenie bloku |
| | FUNCTION | function | deklaracja funkcji |
| | BREAK | break | przerwanie pętli |
| Identyfikatory | ID | [a-zA-Z][a-zA-Z0-9_]* | nazwy zmiennych |
| Literały | NUMBER | liczby całkowite i zmiennoprzecinkowe | liczby |
| | STRING | tekst w apostrofach lub cudzysłowie | ciągi znaków |
| Operatory | PLUS | + | dodawanie |
| | MINUS | - | odejmowanie |
| | MUL | * | mnożenie macierzowe |
| | DOTMUL | .* | mnożenie elementowe |
| | DIV | / | dzielenie |
| | DOTDIV | ./ | dzielenie elementowe |
| | POW | ^ | potęgowanie macierzowe |
| | DOTPOW | .^ | potęgowanie elementowe |
| | TRANSPOSE | ' | transpozycja |
| | ASSIGN | = | przypisanie |
| Relacyjne | EQ | == | równość |
| | NEQ | ~= | nierówność |
| | LT | < | mniejsze |
| | LE | <= | mniejsze lub równe |
| | GT | > | większe |
| | GE | >= | większe lub równe |
| Logiczne | AND | & | AND |
| | ANDAND | && | short-circuit AND |
| | OR | \| | OR |
| | OROR | \|\| | short-circuit OR |
| | NOT | ~ | negacja |
| Delimitery | LPAREN | ( | nawias |
| | RPAREN | ) | nawias |
| | LBRACKET | [ | nawias macierzy |
| | RBRACKET | ] | nawias macierzy |
| | COMMA | , | separator |
| | SEMI | ; lub nowa linia | koniec instrukcji |
| | COLON | : | zakres |
| Specjalne | CONTINUATION | ... | kontynuacja linii |

---

# 4. Gramatyka parsera

Parser został zaimplementowany przy użyciu `ply.yacc`.

program : statement_list

statement_list : statement
               | statement_list statement

statement : assignment
          | if_statement
          | for_loop
          | while_loop
          | function_declaration
          | expression_statement
          | BREAK SEMI
          | BREAK
          | SEMI

expression_statement : expression opt_semi

opt_semi : SEMI
         | empty

empty :

assignment : ID ASSIGN expression SEMI
           | ID ASSIGN expression

# ---------------- IF ----------------

if_statement : IF expression block END
             | IF expression block ELSE block END
             | IF expression block elseif_list END
             | IF expression block elseif_list ELSE block END

elseif_list : elseif_list elseif_clause
            | elseif_clause

elseif_clause : ELSEIF expression block

# ---------------- BLOCK ----------------

block : statement_list

# ---------------- LOOPS ----------------

for_loop : FOR ID ASSIGN expression block END

while_loop : WHILE expression block END

# ---------------- FUNCTIONS ----------------

function_declaration : FUNCTION return_vars ASSIGN ID LPAREN arg_list RPAREN block END
                     | FUNCTION ID LPAREN arg_list RPAREN block END

return_vars : ID
            | LBRACKET id_list RBRACKET

id_list : ID
        | id_list COMMA ID

arg_list :
         | arguments

arguments : expression
          | arguments COMMA expression

# ---------------- EXPRESSIONS ----------------

expression : colon_expr

# ---------- RANGE (:) ----------

colon_expr : colon_expr COLON colon_expr
           | short_or

# ---------- SHORT-CIRCUIT LOGICAL (&&, ||) ----------

short_or : short_or OROR short_and
         | short_and

short_and : short_and ANDAND logical_or
          | logical_or

# ---------- ELEMENT-WISE LOGICAL (&, |) ----------

logical_or : logical_or OR logical_and
           | logical_and

logical_and : logical_and AND relation
            | relation

# ---------- RELATIONS ----------

relation : relation EQ relation
         | relation NEQ relation
         | relation LT relation
         | relation LE relation
         | relation GT relation
         | relation GE relation
         | additive

# ---------- ADD / SUB ----------

additive : additive PLUS additive
         | additive MINUS additive
         | multiplicative

# ---------- MUL / DIV ----------

multiplicative : multiplicative MUL multiplicative
               | multiplicative DOTMUL multiplicative
               | multiplicative DIV multiplicative
               | multiplicative DOTDIV multiplicative
               | power

# ---------- POW ----------

power : power POW power
      | power DOTPOW power
      | unary

# ---------- UNARY ----------

unary : MINUS unary
      | NOT unary
      | postfix

# ---------- TRANSPOSE ----------

postfix : postfix TRANSPOSE
        | primary

# ---------- PRIMARY ----------

primary : ID
        | NUMBER
        | STRING
        | LPAREN expression RPAREN
        | matrix
        | ID LPAREN arg_list RPAREN

# ---------------- MATRIX ----------------

matrix : LBRACKET RBRACKET
       | LBRACKET row_list RBRACKET

row_list : row
         | row_list SEMI row

row : expression_list

expression_list : expression
                | expression_list COMMA expression
---

## Obsługiwane konstrukcje

### Instrukcje przypisania

```matlab
a = 10;
b = a + 5;
```

---

### Instrukcje warunkowe

```matlab
if x > 0
    a = 1;
elseif x == 0
    a = 0;
else
    a = -1;
end
```

---

### Pętle for

```matlab
for i = 1:n
    suma = suma + i;
end
```

---

### Pętle while

```matlab
while x < 100
    x = x + 1;
end
```

---

### Funkcje

```matlab
function [wynik] = silnia(n)
    wynik = 1;
end
```

---

### Wywołania funkcji

```matlab
disp(A)
sin(x)
silnia(5)
```

---

### Operacje macierzowe

```matlab
A * B
A .* B
A^2
A.^2
A'
```

---

# 5. Analiza semantyczna

Po poprawnym zbudowaniu AST uruchamiany jest analizator semantyczny.

Jego zadaniem jest wykrywanie błędów logicznych niemożliwych do wykrycia przez parser.

---

## Obsługiwane błędy semantyczne

### Użycie niezainicjalizowanej zmiennej

Kod:

```matlab
X = Y + 5;
```

Komunikat:

```text
Linia 3:
Błąd semantyczny - Użycie niezainicjalizowanej zmiennej 'Y'
```

---

### Nadpisanie funkcji wbudowanej

Kod:

```matlab
sin = 10;
```

Komunikat:

```text
Linia 1:
Błąd semantyczny - Próba nadpisania funkcji wbudowanej 'sin'
```

---

### Niespójne wymiary macierzy

Kod:

```matlab
M = [1,2,3;
     4,5];
```

Komunikat:

```text
Linia 1:
Błąd semantyczny - Niespójne wymiary macierzy
```

---

### Break poza pętlą

Kod:

```matlab
break;
```

Komunikat:

```text
Linia 1:
Błąd semantyczny - Instrukcja break użyta poza pętlą
```

---

### Wywołanie nieznanej funkcji

Kod:

```matlab
abc(10);
```

Komunikat:

```text
Linia 1:
Błąd semantyczny - Wywołanie nieznanej funkcji 'abc'
```

---

# 6. Generowanie kodu Python

Generator AST tłumaczy konstrukcje MATLAB na odpowiadające im konstrukcje języka Python.

---

## Tłumaczenie operatorów

| MATLAB | Python |
|----------|----------|
| .* | * |
| ./ | / |
| .^ | ** |
| && | and |
| \|\| | or |
| ~= | != |
| ~ | np.logical_not() |

---

## Tłumaczenie macierzy

MATLAB

```matlab
A = [1,2;3,4];
```

Python

```python
A = np.array([[1,2],[3,4]])
```

---

## Tłumaczenie transpozycji

MATLAB

```matlab
A'
```

Python

```python
A.T
```

---

## Tłumaczenie disp

MATLAB

```matlab
disp("Hello")
```

Python

```python
print("Hello")
```

Realizowane jest przez centralny słownik tłumaczeń funkcji.

---

# 7. Słownik tłumaczeń funkcji

Translator wykorzystuje wspólny moduł zawierający mapowanie funkcji MATLAB → Python.

Przykładowe tłumaczenia:

| MATLAB | Python |
|----------|----------|
| disp | print |
| zeros | np.zeros |
| ones | np.ones |
| eye | np.eye |
| rand | np.random.rand |
| linspace | np.linspace |
| sin | np.sin |
| cos | np.cos |
| tan | np.tan |
| exp | np.exp |
| log | np.log |
| log10 | np.log10 |
| sqrt | np.sqrt |
| sum | np.sum |
| mean | np.mean |
| max | np.max |
| min | np.min |
| length | len |
| size | np.shape |

---

# 8. Interfejs użytkownika

Aplikacja udostępnia:

- edytor MATLAB
- edytor Python
- numerację linii
- podświetlanie składni
- ładowanie plików
- tłumaczenie kodu
- uruchamianie kodu Python
- prezentację błędów

Do realizacji edytora wykorzystano bibliotekę CodeMirror.

---

# 9. Scenariusze testowe

## Test błędu semantycznego

```matlab
sin = 10;

M = [1, 2, 3; 4, 5];

X = Y + 5;

Z = 1 + 1;
```

Oczekiwane błędy:

- nadpisanie funkcji sin
- niezgodne wymiary macierzy
- użycie niezainicjalizowanej zmiennej Y

---

## Test błędów składniowych i leksykalnych

```matlab
wartosc = 500 $ + 10 #;

100 = zmienna_a;

M = [1, 2, (3 + 4];

if == 5
    a = 1;
end

kalkulacja = 5 + / * 2;
```

Oczekiwane błędy:

- nieznane symbole
- błędne przypisanie
- niezamknięte nawiasy
- błędna składnia instrukcji if
- błędne wyrażenie arytmetyczne

---

## Test funkcji i pętli

```matlab
function [res] = skomplikowana_funkcja(n, m)
    res = 0;

    for i = 1:n
        if (i < m) && (i > 0)
            res = res + i;
        elseif i == m
            res = res + 100;
        else
            res = res - 1;
        end
    end

    while res < 200
        res = res + 10;

        if res == 150
            break;
        end
    end
end

disp(skomplikowana_funkcja(2,3))
```

---

## Test operacji macierzowych

```matlab
A = [1,2,3;4,5,6;7,8,9];
B = [9,8,7;6,5,4;3,2,1];

C = A * B';
D = A .* B;
E = A.^2;
F = A^2;

res1 = (C > 10) & (D < 50);
res2 = ~res1;

disp(C);
disp(D);
disp(res1);
disp(res2);
```

---

## Test funkcji użytkownika

```matlab
function [wynik] = silnia(n)

    if n < 0
        wynik = -1;

    elseif n == 0
        wynik = 1;

    else
        wynik = 1;

        for j = 1:n
            wynik = wynik * j;
        end

    end
end

a = 5;
b = silnia(a);

if b > 100
    disp('Wynik jest duży');
else
    disp('Wynik jest mały');
end
```
