# EVOX

API do tworzenia, modyfikowania oraz wyświetlania wiadomości wraz z ich licznikiem wyświetleń.

## Instalacja i uruchomienie

### Instalacja

 

``` shell
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

Wersja alternatywna, wykorzystująca pipenv:

``` shell
cd app
pipenv installl --dev
```

### Uruchomienie

Lokalne uruchomienie na [localhost:8000](http://localhost:8000/)

``` shell
python3 manage.py runserver
```

## API

### Lista endpointów

| Metoda HTTP   | Wymaga uwierzytelnienia   | URL                       | Funkcjonalność            |
| ------------- | -------------             | -------------             | -------------             |
| POST          | TAK                       | `/api/messages/`          | Dodanie nowej wiadomości  |
| PUT           | TAK                       | `/api/messages/<int:id>`  | Modyfikacja wiadomości    |
| DELETE        | TAK                       | `/api/messages/<int:id>`  | Usunięcie wiadomości      |
| GET           | NIE                       | `/api/messagess/<int:id>` | Odczyt wiadomości         |

### Format zapytań i odpowiedzi

Zapytania modyfikujące wiadomość (widok utworzenia, edycji i usunięcia wiadomości) muszą zawierać wiadomość umieszczoną w BODY w formacie json: 

``` json
{
    "content": "Treść wiadomości"
}
```

Każde poprawne zapytanie zwraca odpowiedź w formacie json zawierającą następujące pola:

``` json
{
    "id": 1,
    "content": "Treść wiadomości",
    "view_count": 0
}
```

### Uwierzytelnienie

Aby korzystać z modyfikujących wiadomości widoków należy posiadać `API key` . Należy zamieścić go w headerze w następujący sposób:

``` json
{
    "Authorization": "Api-Key <API_KEY>"
}
```

`API key` są generowane z panelu administratora, może ich być wiele, oraz można każdemu przypisać czas wygaśnięcia.

## Deployment

Serwer produkcyjny dla tej aplikacji znajduje się pod adresem [ianczyko-evox.herokuapp.com](https://ianczyko-evox.herokuapp.com/ )

> Uwaga, serwer jest usypiany po 30 minutowej bezczynności, dlatego pierwsze zapytanie może potrwać chwilę dłużej.

### CI/CD

Deployment jest ustawiony na automatyczny, po wypchnięciu zmian na to repozytorium zdalne i po pomyślnym przejściu testów jednostkowych w CI GitHub Actions, Heroku buduje aplikację i podmienia z aktualnie działającą (pozostawiając bazę danych nienaruszoną).

### Bezpieczeństwo

Aplikacja przechodzi wszystkie testy bezpieczeństwa dotyczące deploymentu ( [Deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/ ))

``` shell
~/app $ python3 manage.py check --deploy
System check identified no issues (0 silenced).
```

## Przykłady użycia API

Przykłady będą wykorzystywać serwer produkcyjny.

### Odczyt wiadomości

TBD

### Utworzenie wiadomości

TBD

### Modyfikacja wiadomości

TBD

### Usunięcie wiadomości

TBD
