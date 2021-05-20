# EVOX

API do tworzenia, modyfikowania oraz wyświetlania wiadomości wraz z ich licznikiem wyświetleń.

## Instalacja i uruchomienie

### Instalacja

``` shell
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

Istnieje również możliwość instalacji za pomocą pipenv (w katalogu app: `pipenv install --dev`)

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

Zapytania modyfikujące wiadomość (widok utworzenia i edycji wiadomości) muszą zawierać wiadomość umieszczoną w BODY w formacie json: 

``` json
{
    "content": "Message content"
}
```

Każde poprawne zapytanie zwraca odpowiedź w formacie json zawierającą następujące pola:

``` json
{
    "id": 1,
    "content": "Message content",
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

Deployment jest ustawiony na automatyczny, po wypchnięciu zmian na to repozytorium zdalne i po pomyślnym przejściu testów jednostkowych w CI GitHub Actions, Heroku buduje aplikację i podmienia z aktualnie działającą (dane w bazie danych są zachowywane pomiędzy deploymentami).

### Bezpieczeństwo

Aplikacja przechodzi wszystkie testy bezpieczeństwa dotyczące deploymentu ([Deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/ ))

``` shell
~/app $ python3 manage.py check --deploy
System check identified no issues (0 silenced).
```

### Ustawienia

Aplikacja wykorzystuje następujące zmienne środowiskowe:

* SECRET_KEY - wykorzystywany wewnętrznie przez Django do operacji kryptograficznych klucz prywatny ([SECRET_KEY](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY ))
* IS_DEPLOYMENT - ustawienie zmiennej powoduje konfigurację produkcyjną tj. spełniającą reguły bezpieczeństwa opisane w [Deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/ )
* DEPLOYMENT_HEROKU - ustawienie zmiennej powoduje dodatkową konfigurację specyficzną dla Heroku 

## Przykłady użycia API

Przykłady będą wykorzystywać serwer produkcyjny.

> W przykładach należy uzupełnić pola `API_KEY` oraz `MESSAGE_ID`

### Utworzenie wiadomości

``` shell
curl --location --request POST 'https://ianczyko-evox.herokuapp.com/api/messages/' \
--header 'Authorization: Api-Key <API_KEY>' \
--header 'Content-Type: application/json' \
--data-raw '{"content": "New Message"}'
```

### Modyfikacja wiadomości

``` shell
curl --location --request PUT 'https://ianczyko-evox.herokuapp.com/api/messages/<MESSAGE_ID>' \
--header 'Authorization: Api-Key <API_KEY>' \
--header 'Content-Type: application/json' \
--data-raw '{"content": "Updated Message"}'
```

### Usunięcie wiadomości

``` shell
curl --location --request DELETE 'https://ianczyko-evox.herokuapp.com/api/messages/<MESSAGE_ID>' \
--header 'Authorization: Api-Key <API_KEY>'
```

### Odczyt wiadomości

```shell
curl --location --request GET 'https://ianczyko-evox.herokuapp.com/api/messages/<MESSAGE_ID>'
```
