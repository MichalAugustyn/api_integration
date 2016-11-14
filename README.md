# Dokumentacja

## Numery indeksów członków grupy
* **Michał Augustyn** - 148989;
* **Radosław Zielonka** - 149064

## Użyte technologie / języki programowania

### Języki programowania
* **Python** - API dostawców, HUB API, skrypt tworzący strukturę baz danych i ładujący do niej dane;
* **SQL** - zapytania do baz danych

### Technologie
* **Flask** - (lekki framework do budowy aplikacji) - API dla dostawców, API integrujące;
* **MySQL** - bazy danych dostawców

### Biblioteki
* **json** - przetwarzanie danych w formacie JSON;
* **simplexml** - przetwarzanie danych w formacie XML;
* **datetime** - przetwarzanie dat (porównywanie, formatowanie, walidacja);
* **re** - wykorzystanie wyrażeń regularnych;
* **flask_restful** - rozszerzenie do framework'a Flask służące do budowania aplikacji API typu REST;
* **flask_mysql** - tworzenie połączenia z bazą danych MySQL;
* **request** - tworzenie zapytań HTTP

## Schemat
![alt tag](Diagram.png)

## Opis architektury systemu

1. dane zawarte są w logach w formacie plików tekstowych. Szczegóły poszczególnych logów zostaną opisane w kolejnym punkcie.
2. skrypt napisany w języku Python tworzy przygotowaną wcześniej strukturę baz danych dostawców, analizuje logi dzieląc je na odpowiednie kolumny, ładuje dane do baz
3. aplikacje typu API pobierają dane z baz i udostępniają je użytkownikowi dla zapytań typu GET. API obu dostawców zwracają wszystkie dane z poszczególnych baz pod adresem /notification. Różnice w strukturach baz oraz odpowiedzi API zostaną opisane poniżej.
4. aplikacja integrująca - API HUB - komunikuje się z aplikacjami obu dostawców poprzez protokół HTTP. Pobiera ona wszystkie wiersze z obu baz danych a następnie integruje je według jednego wzorca.
5. API HUB umożliwia zwrócenie wszystkich, jak również odfiltrowanej części wierszy z obu baz danych.

## Opis dostawców

### Różnice w logach dostawców

* Dostawca I
```
[2010-10-23T09:10:18Z] (135)635-1735 - RALPH WALLACE - 3495 Jenifer Way, New York - "PEDE MALESUADA IN IMPERDIET ET COMMODO VULPUTATE JUSTO IN BLANDIT"
```

* Dostawca II
```
[24-10-2010 03:13:52] 3rd Hill 325, Avalon - Cheryl Jacobs 263 8242123 [TURPIS ELEMENTUM LIGULA VEHICULA CONSEQUAT MORBI A IPSUM INTEGER A NIBH IN]
```

### Różnice w strukturze baz danych dostawców

### Tabela CALLER
#### Dostawca I
id | name | last_name | phone
------ | ---- | --------- | -------------
NYC000 | JOE | EDWARDS | (546)300-4812
#### Dostawca II
id | name | phone_prefix | phone_number
------ | ------------- | --------- | -------------
LAC000 | Alan Gonzales | 812 | 9302240
### Tabela NOTIFICATION
#### Dostawca I
id | date_time | address | city | caller_id | additional_information
------ | ------- | ----------------- | ------------- | -------------- | --------------------
NYN001 | 2010-10-23 09:10:18 | 3495 Jenifer Way | New York | NYC001 | PEDE MALESUADA INLIGUL
#### Dostawca II
id | date | street_number | street_name | city | caller_id | description
------ | ------------------- | ----------------------- | ------------- | -------------- | -------------------- | ----------------------
LAN007 | 2010-11-08 08:47:22 | 54 | Birchwood Crossing | Avalon | LAC007 | VITAE IPSUM NON


### Różnice w odpowiedzi obu API

* Dostawca I
```xml
<response>
  <items>
    <item>
      <date_time>2010-10-23 09:10:18</date_time>
      <last_name>WALLACE</last_name>
      <city>New York</city>
      <additional_information>PEDE MALESUADA IN IMPERDIET ET COMMODO VULPUTATE JUSTO IN BLANDIT</additional_information>
      <address>3495 Jenifer Way</address>
      <phone>(135)635-1735</phone>
      <id>NYN001</id>
      <caller_id>NYC001</caller_id>
      <name>RALPH</name>
    </item>
  </items>
  <items_count>1</items_count>
</response>
```
* Dostawca II
``` python
{
   "items":[
      {
         "caller_id":"LAC001",
         "city":"Avalon",
         "date":"2010-10-24 03:13:52",
         "description":"TURPIS ELEMENTUM LIGULA VEHICULA CONSEQUAT MORBI A IPSUM INTEGER A NIBH IN",
         "id":"LAN001",
         "name":"Cheryl Jacobs",
         "phone_number":8242123,
         "phone_prefix":263,
         "street_name":"3rd Hill",
         "street_number":325
      }
   ],
   "items_count":1
}
```
## Opis aplikacji API dla dostawców
API dostawców zwracają informacje jedynie dla zapytań typu GET. Poniżej znajduje się lista dostępnych lokalizacji dla każdej z nich. 

dostawca I | dostawca II
-------------- | -----------------
/notification | /notification
/notification/id | /notification/id
/notification/date_time | /notification/date
/notification/street | /notification/street
/notification/city | /notification/city
/notification/callerid | /notification/callerid
/notification/add_information | /notification/description
/caller/id | /caller/id
/caller/name | /caller/name
/caller/last_name | /caller/name
/caller/phone | /caller/phone_prefix
/caller/phone | /caller/phone_number

## Opis aplikacji HUB API

### Integracja pierwszego dostawcy:
kod | działanie
------------------------------------------------------------------------------- | --------------------------------------
'id': x['id'], | pozostaje bez zmian
'date': x[**'date_time'**], | zmiana nazwy atrybutu
'name': x['name'].**capitalize()**, | zmiana wielkości liter (pierwsza wielka, reszta mała)
'last_name': x['last_name'].**capitalize()**, | jak wyżej
'phone_prefix': int(**re.findall('\((\d+)\)', x['phone'])[0]**), | wydobycie prefixu przy użyciu wyrażeń reg.
'phone_number': int("".join(**re.findall('(\d+)-(\d+)', x['phone'])[0])**), | wydobycie numeru przy użyciu wyrażeń reg.
'street_number': int(**re.findall('(\d+) (.+)', x['address'])[0][0]**), | wydobycie numeru ulicy przy użyciu wyrażeń reg.
'street_name': **re.findall('(\d+) (.+)', x['address'])[0][1]**, | jak wyżej - wydobycie nazwy ulicy
'city': x['city'], | pozostaje bez zmian
'description': x['additional_information'].**capitalize()** | zmiana wielkości liter

### Integracja drugiego dostawcy:
kod | działanie
------------------------------------------------------------------------------- | --------------------------------------
* 'id': x['id'], | pozostaje bez zmian
* 'date': x['date'], | pozostaje bez zmian
* 'name': x['name'].**split()[0]**, | wydobycie pierwszego członu z imienia i nazwiska
* 'last_name': x['name'].**split()[1].capitalize()**, | jak wyżej - wydobycie drugiego członu, zmiana wielkości  liter
* 'phone_prefix': x['phone_prefix'], | pozostaje bez zmian
* 'phone_number': x['phone_number'], | pozostaje bez zmian 
* 'street_number': x['street_number'], | pozostaje bez zmian
* 'street_name': x['street_name'], | pozostaje bez zmian
* 'city': x['city'], | pozostaje bez zmian
* 'description': x['description'].**capitalize()** | zmiana wielkości liter

## Struktura wynikowa encji

city | date | description | id | last_name | name | phone_number | phone_prefix | street_name | street_number
------------- | ------------------------------ | ----------------------------------- | ----------- | ----------- | ------------ | ------------ | ------------- | ------ | ------
"Buffalo" | "2013-10-06 12:10:47 | "Amet eler..." | "NYN500" | "Burke" | "Rebecca" | 7188468  | 653 | "Homewood Hill " | 1
"Los Angeles" | "2013-10-04 14:46:16" | "Aenean auc..." | "LAN500" | "Ruiz" | "Katherine" | 1839793 | 911 | "Pond Street" | 80  

## Dostęp do danych za pomocą metody GET

Aplikacja umożliwia dostęp do danych poprzez kilka lokalizacji. Szczegóły każdej z nich opisane są w poniższej tabeli

lokalizacja | szczegóły | przykład
--------------------- | ------------------------ | ----------------
/notification | zwraca wszystkie wiersze z obu baz danych
/notification/id | filtrowanie danych po ID zdarzenia (regexp match) | /notifcation/id/NAN\.\*55
/notification/date | filtrowanie danych po dacie (data poprzedzona znakiem ">" lub "<" | /notification/date/>2015-10-05 12:15
/notification/street | filtrowanie po nazwie ulicy (regexp match) | /notification/street/\.\*Avenue\.\* 
/notification/city | filtrowanie po nazwie miasta (regexp match) | /notification/city/\.\*Los\.\*
/notification/description | filtrowanie po opisie zdarzenia | /notification/description/\.\*lorem\.\*
/caller/name | filtrowanie po imieniu zgłaszającego | /caller/name/\.\*ath\.\*/\.\*
/caller/last_name | filtrowanie po nazwisku zgłaszającego | /caller/last_name/\.\*ed
/caller/phone_prefix | filtrowanie po prefiksie (regexp match) | /caller/phone_prefix/546
/caller/phone_number | filtrowanie po numerze telefonu (regexp match) | /caller/phone_number/\.\*555\.\*

## Dostęp do danych za pomocą metody POST

Wykorzystując zapytanie typu POST możemy wyciągnąć z baz danych wiersze, używając więcej niż jednego filtra. Dane przekazujemy w formacie JSON. Tabela przedstawia dostępne filtry oraz zakresy i wartości, które można przypisać każdej z nich.

atrybut | wartości
------------------- | ------------------------
id | regexp match
after | date
before | date
name | regexp match
last_name | regexp match
phone_prefix | regexp match
phone_number | regexp match
street_number | regexp match
street_name | regexp match
city | regexp match
description | regexp match

## Napotkane problemy

* hosting aplikacji przy użyciu publicznego adresu IP
problem nie został rozwiązany. Problem leży w odpowiedniej konfiguracji routera (przekierowywanie portów)

* kombinacja znaku % i cyfr (składnia wyrażeń regularnych MySQL) w adresie URL zostaje rozszyfrowywana jako konkretny znak.
rozwiązanie problemu - zamiana znaku zastępującego każdy znak z "%" na "*"

* jedno z API zwracało odpowiedź w formacie XML dla zapytań w przeglądarce, natomiast dla zapytań w skrypcie - JSON
rozwiązanie problemu - poprawa logiki sposobu zwracania odpowiedzi

* możliwość porównywania dat jedynie w przypadku podania daty w całości
rozwiązanie problemu - zastosowanie mechanizmu uzupełniania daty wartościami domyślnymi, jeżeli data jest niekompletna.

* konieczność definiowania wielkich i małych liter w wyrażeniach regularnych.
rozwiązanie problemu - zastosowanie funkcji re.IGNORECASE wbudowanej w module re

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
