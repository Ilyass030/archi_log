document.addEventListener('DOMContentLoaded', async function() {

    var values = [];
    var currentYear = new Date().getFullYear();

    for (var annee = currentYear; annee > 1880; annee--)
    {
        values.push(annee)
    }

    var select = document.createElement("select");
    select.name = "annee_sortie";

    var option = document.createElement("option");
    option.value = 0;
    option.text = "inconnu";
    select.appendChild(option);

    for (const val of values)
    {
        var option = document.createElement("option");
        option.value = val;
        option.text = val;
        select.appendChild(option);
    }

    document.getElementById("annee_sortie").after(select);
});