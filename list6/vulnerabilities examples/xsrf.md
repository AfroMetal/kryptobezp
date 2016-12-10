# XSRF(Cross Site Request Forgery) wykorzystujący wyłączone zabezpieczenie CSRF w serwerze.

## Scenariusz użycia:
Administrator może zatwierdzić wszystkie przelewy wchodząc na stronę `http://localhost:8000/bank/admin/confirm_all/`. Jeśli jest on zalogowany na konto administratora, wystarczy, aby podłożyć mu link do tej strony, który się automatycznie wykona, żeby wszystkie przelewy zostały zatwierdzone bez jego wiedzy.

## Przykład:

1. Tagiem HTML, który umożliwia automatyczne wywołanie linków jest `img`, który próbując załadować obrazek wystosuje za nas zapytanie GET pod adres podany jako parametr `src`. Może to być nawet lokalnie otwarty plik, z zawartością:
```
<img src="http://localhost:8000/bank/admin/confirm_all/"/>
```
