# Modelowanie-Fizyczne

CEL PROJEKTU: 
Wyznaczanie własności pola prędkości oraz wykreślanie wykresów torów oraz linii prądu w danym przepływie płynu.

OPIS ZJAWISKA:
Pole prędkości określa prędkość przepływu płynu w każdym punkcie przestrzeni oraz posiada informacje o zmianach objętościowych ciała jak i zmianach zachodzących w danym polu.
Pole prędkości jest polem wektorowym co umożliwia nam przeprowadzenie na nim operacji różniczkowych takich jak:

Dywergencja-pole skalarne równe sumie pochodnych cząstkowych składowych wektora pola:

![dywergencja](https://user-images.githubusercontent.com/94971277/143764816-5860e487-4b99-4f40-a040-94452d7f1915.png)

Rotacja-tworzy pole wektorowe, które wskazuje wirowanie pola. Jeżeli rotacja jest równa 0 oznacza to że pole jest potencjalne. Wyznacza się ją przez wzór:

![rotacja](https://user-images.githubusercontent.com/94971277/143765056-2105b11a-d40c-4114-809a-b499d771cc4b.png)

Linie prądu to linie styczne w każdym punkcie pola w pewnej chwili czasu do wektora prędkości.

WYKORZYSTYWANE NARZEDZIA:
-NumPy

-SymPy

-MatPlotLib

-PySimpleGUI

OGÓLNY OPIS PROJEKTU I MOŻLIWE ALTERNATYWY:
Projekt ma na celu wyznaczenie pola prędkości i jego własności takich jak rotacja, dywergencja pola prędkości, za pomocą wprowadzonych przez użytkownika danych do okienka pobierania programu oraz wyświetlenie okna z wykreślonymi torami oraz liniami prądu w danym przepływie. Altermatywą może być wykreślenie torów w przestrzeni trójwymiarowej.

SPECYFICZNE WYMAGANIA:

Wymagania funkcjonalne:

Program ma:

-wyznaczać rotacje, dywergencje pola prędkości

-wykreślać tor oraz linie prądu danego przepływu

-sprawdzać czy dane pole prędkości istnieje

Wymagania niefunkcjonalne:

Program powinien:

-być dokładny

-szybko działać

-być niezawodny

-być przejrzysty

HARMONOGRAM PRAC:

7.12 - napisanie kodu odpowiedzialnego za pojawianie się okienka do którego użytkownik wprowadza dane oraz wykreślanie wykresów ma podstawie tych danych.

14.12 - część kodu odpowiedzialna za obliczanie linii pola prędkości, torów i ich wykreślanie.

21.12 - kod odpowiedzialny za określanie dywergencji, rotacji pola prędkości.

4.01 - dodanie progressbaru i wykresu rotacji

11.01 - obsługa wyjątków.

![Cython-logo svg](https://user-images.githubusercontent.com/47851742/143024239-0f85ac56-0081-4363-85c5-e1faa60692f4.png)
