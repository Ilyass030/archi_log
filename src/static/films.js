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
    setTimeout(() => submit.disabled = false, 1000);

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
    console.log(data);

    for (key in Object.keys(data))
    {
        film = data[key];
        film_form = document.createElement('form');
        input = document.createElement("input");
        li = document.createElement("li");

        film_form.appendChild(li);
        film_form.appendChild(input);
        liste_films.appendChild(film_form);

        film_form.className += "onefilm";
        film_form.setAttribute("method","post");
        film_form.setAttribute("action","/film_detail");

        li.innerHTML = "<strong>" + film[1] + "</strong> (" + film[3] + ')';
        li.setAttribute("onclick", "this.parentNode.submit();");

        input.type = "hidden";
        input.name = "film_id";
        input.value = film[0];

    }
}