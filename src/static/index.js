const form_ajout_film = document.getElementById('ajout_film');
if (form_ajout_film)
{
    form_ajout_film.addEventListener("submit", function(e) {
        ajouter_film(e, this);
    });
}

async function ajouter_film(e, form) {
    e.preventDefault();

    const submit = document.getElementById('submit_film');
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


    const response = await fetch("/ajout_film",
        { method: 'POST',
          headers: {'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonifyForm)
        });
    
    const data = await response.json();

    console.log(data);
    film_info = document.getElementById('afficher_film');
    film_id = document.getElementById('film_id');
    film_id.innerHTML = data['film'][0][0];
    film_id.value = data['film'][0][0];
    film_info.innerHTML = "<strong>" + data['film'][0][1] + "</strong> (" + data['film'][0][3] + ')';

    if (data['error'])
    {
        error_message = document.getElementById('error');
        error_message.innerHTML = data['error'];
    }
}