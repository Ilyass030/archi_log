console.log("test");
var values = [];
var currentYear = new Date().getFullYear();

for (var annee = currentYear; annee > 1880; annee--)
{
    values.push(annee)
}

var select = document.createElement("select");
select.name = "genre";

for (const val of values)
{
    var option = document.createElement("option");
    option.value = val;
    option.text = val;
    select.appendChild(option);
}


document.getElementById("annee_sortie").after(select);