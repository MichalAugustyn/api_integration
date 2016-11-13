# Dokumentacja

## Numery indeksów członków grupy
* **Michał Augustyn** - 148989;
* **Radosław Zielonka** - 149064;

## Użyte technologie / języki programowania

### Języki programowania
* **Python** - API dostawców, HUB API, skrypt tworzący strukturę baz danych i ładujący do niej dane;
* **SQL** - zapytania do baz danych;

### Technologie
* **Flask** - (lekki framework do budowy aplikacji) - API dla dostawców, API integrujące;
* **MySQL** - bazy danych dostawców;

### Biblioteki
* **json** - przetwarzanie danych w formacie JSON;
* **simplexml** - przetwarzanie danych w formacie XML
* **datetime** - przetwarzanie dat (porównywanie, formatowanie, walidacja);
* **re** - wykorzystanie wyrażeń regularnych;
* **flask_restful** - rozszerzenie do framework'a Flask służące do budowania aplikacji API typu REST;
* **flask_mysql** - tworzenie połączenia z bazą danych MySQL;
* **request** - tworzenie zapytań HTTP;

## Schemat
![alt tag](Diagram.png)

## Opis architektury systemu

1. dane zawarte są w logach w formacie plików tekstowych. Szczegóły poszczególnych logów zostaną opisane w kolejnym punkcie;
2. skrypt napisany w języku Python tworzy przygotowaną wcześniej strukturę baz danych dostawców, analizuje logi dzieląc je na odpowiednie kolumny, ładuje dane do baz
3. aplikacje typu API pobierają dane z baz i udostępniają je użytkownikowi dla zapytań typu GET. API obu dostawców zwracają wszystkie dane z poszczególnych baz pod adresem /notification. Różnice w strukturach baz oraz odpowiedzi API zostaną opisane poniżej.
4. aplikacja integrująca - API HUB - komunikuje się z aplikacjami obu dostawców poprzez protokół HTTP. Pobiera ona wszystkie wiersze z obu baz danych a następnie integruje je według jednego wzorca.
5. API HUB umożliwia zwrócenie wszystkich, jak również odfiltrowanej części wierszy z obu baz danych.


•opis dostawców, struktura encji;
•opis huba, przebieg integracji encji, struktura wynikowa encji;

## Napotkane problemy
* 

## Adres do repozytorium
http://github.com/MichalAugustyn/api_integration.git

## Podział pracy w grupie

### **Michał Augustyn:**
* programowanie w języku Python;
* projektowanie i implementacja rozwiązań

### **Radosław Zielonka:**
* przygotowanie danych;
* tworzenie struktury bazy danych; 
* tworzenie zapytań w języku SQL;
* testowanie aplikacji

## Co byśmy zmienili gdybyśmy robili ten projekt jeszcze raz?
