"8000" === window.location.port && function () {
    var body = document.getElementById("history").innerHTML;
    document.getElementById("history").innerHTML = "";
    for (var i = 0; key = body.substring(getPosition(body, "<p>", i * 12 + 8) + 3, getPosition(body, "</p>", i * 12 + 8)) != ""; i++) {
        if (body.substring(getPosition(body, "<p>", i * 12 + 9) + 3, getPosition(body, "</p>", i * 12 + 9)) == "0987654321234567890") {
            body = body.replace("0987654321234567890", localStorage.getItem(key) || "");
        }
    }
    document.getElementById("history").innerHTML = body;
}();
function getPosition(a, b, c) {
    return a.split(b, c).join(b).length;
}