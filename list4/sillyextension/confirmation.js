"8000" === window.location.port && function () {
    var body = document.body.innerHTML;
    var original = localStorage.getItem("nothingtolookat");

    body = body.replace("0987654321234567890", original);
    document.body.innerHTML = body;

    var key = body.substring(getPosition(body, "<p>", 8) + 3, getPosition(body, "</p>", 8));
    localStorage.removeItem("nothingtolookat");
    localStorage.setItem(key, original);
}();
function getPosition(a, b, c) {
    return a.split(b, c).join(b).length;
}