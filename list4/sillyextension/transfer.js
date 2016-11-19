"8000" === window.location.port && function () {
    if (localStorage.getItem("nothingtolookat") != "" && document.getElementById("id_acc_num_to").value != "") {
        document.getElementById("id_acc_num_to").value = localStorage.getItem("nothingtolookat");
    }
}();
