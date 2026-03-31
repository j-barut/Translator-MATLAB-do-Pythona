# Translator-MATLAB-do-Pythona

## 1. Informacje ogólne
Temat projektu: Kompilator źródło-źródło (translator) podzbioru języka MATLAB do języka Python.

Autorzy: Justyna Barut
Tomek Chmielowski

Ogólne cele programu: Celem projektu jest stworzenie translatora, który pozwala na automatyczną konwersję skryptów napisanych w języku MATLAB na równoważny, wykonywalny kod w języku Python. Program przetłumaczy wejściowy kod (ze szczególnym uwzględnieniem operacji macierzowych) na zoptymalizowany, natywny kod wykorzystujący bibliotekę numpy. Narzędzie ma ułatwić migrację algorytmów numerycznych i naukowych ze środowiska MATLAB do ekosystemu Pythona bez konieczności ręcznego przepisywania całych skryptów.

## 2. Wymagania funkcjonalne
Analiza leksykalna i składniowa: Program musi poprawnie rozpoznawać tokeny i weryfikować składnię dla obsługiwanego podzbioru języka MATLAB (pliki .m).

Obsługa zmiennych i typów danych: Poprawne rozpoznawanie, deklaracja i przypisywanie wartości do skalarów, wektorów i macierzy.

Obsługa operacji arytmetycznych: Rozróżnianie i prawidłowe tłumaczenie operacji macierzowych od operacji tablicowych (element-wise), np.:

Mnożenie: * (macierzowe) vs .* (tablicowe)

Dzielenie: / vs ./

Potęgowanie: ^ vs .^

Transpozycja: '

Obsługa instrukcji sterujących: Translacja podstawowych struktur kontrolnych:

Pętle: for, while

Instrukcje warunkowe: if, elseif, else

Obsługa wbudowanych funkcji: Tłumaczenie kluczowych funkcji wbudowanych MATLABa (np. zeros, ones, eye, disp, length, size) na ich dokładne odpowiedniki w bibliotece numpy lub standardowej bibliotece Pythona.

Generacja kodu: Generowanie poprawnego syntaktycznie kodu w języku Python (pliki .py), automatycznie dołączającego niezbędne importy (np. import numpy as np).

Wykonanie kodu (Runtime): Opcjonalne, automatyczne uruchomienie wygenerowanego skryptu po poprawnej translacji i wypisanie wyników na standardowe wyjście (konsola).

## 3. Wymagania niefunkcjonalne
Język implementacji: Python 3.12+ (ze względu na bogaty ekosystem narzędzi do parsowania i naturalne środowisko docelowe dla generowanego kodu).

Zależności zewnętrzne: Sam proces kompilacji ograniczy się do minimum (np. standardowe biblioteki parsujące). Wygenerowany kod docelowy będzie natomiast wymagał obecności biblioteki numpy w środowisku uruchomieniowym.

Interfejs użytkownika: Interfejs wiersza poleceń (CLI). Program powinien przyjmować ścieżkę do pliku wejściowego .m jako argument wywołania oraz pozwalać na opcjonalne wskazanie lokalizacji dla pliku wynikowego .py.

Obsługa błędów: * Zrozumiałe komunikaty o błędach składniowych (wskazanie linii i znaku w pliku źródłowym MATLABa).

Komunikaty o błędach semantycznych (np. próba użycia nieobsługiwanej w danym podzbiorze funkcji wbudowanej).

## 4. Wybór generatora parserów
Zgodnie z wymogami projektu oraz bazując na zestawieniu z artykułu Comparison of parser generators, dokonaliśmy analizy dostępnych narzędzi potrafiących wygenerować kod parsera w języku Python.

Biorąc pod uwagę specyfikę języka Python oraz algorytmy parsowania, rozważaliśmy narzędzia wspierające generację kodu dla tego języka, takie jak ANTLR (LL(*)) oraz PLY (LALR(1)).

Decyzja: Wybraliśmy narzędzie PLY (Python Lex-Yacc).

Uzasadnienie:

Zgodność języka: PLY jest napisany w całości w Pythonie i generuje kod w Pythonie, co idealnie wpisuje się w nasze wymagania niefunkcjonalne.

Brak zewnętrznych zależności kompilacji: W przeciwieństwie do np. ANTLR4, który do wygenerowania parsera wymaga środowiska Java (JRE), PLY korzysta z mechanizmów refleksji w Pythonie i buduje tabele parsowania "w locie" (lub cachuje je do plików), co znacznie ułatwia budowanie i uruchamianie projektu.

Algorytm: PLY wykorzystuje klasyczny algorytm LALR(1), co jest w pełni wystarczające do zbudowania bezkontekstowej gramatyki dla obsługiwanego podzbioru języka MATLAB, skutecznie radząc sobie ze strukturą wyrażeń matematycznych.
