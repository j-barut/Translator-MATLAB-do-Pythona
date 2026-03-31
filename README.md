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
