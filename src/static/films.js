const form_search_film = document.getElementById('search_film');
if (form_search_film)
{
    form_search_film.addEventListener("submit", function(e) {
        search_film(e, this);
    });
}

async function search_film(e, form) {
    e.preventDefault();

    const submit = document.getElementById('submit_search');
    submit.disabled = true;
    setTimeout(() => submit.disabled = false, 2000);

    jsonifyForm = {genres : []};
    const readable_form = new FormData(form)
    for (const pair of readable_form) {
        if ((pair[0]) != "genres[]")
            jsonifyForm[pair[0]] = pair[1];
        else
            jsonifyForm.genres.push({"genre": pair[1]});
    }


    const response = await fetch("/search_film",
        { method: 'POST',
          headers: {'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonifyForm)
        });
    
    const data = await response.json();

    liste_films = document.getElementById("film_detail");
    liste_films.innerHTML = "";
    for (film in data["films"])
    {
        div = document.createElement('div');
        div.class = "onefilm";
        div.onclick = "document.getElementById('film_detail').submit();";

        li = document.createElement("li");
        film_info.innerHTML = "<strong>" + film[1] + "</strong> (" + film[3] + ')';

        input = document.createElement("input");
        input.type = "hidden";
        input.name = "film_id";
        input.value = film[0];

        div.appendChild(li);
        div.appendChild(input);
    }
}