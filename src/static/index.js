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



    console.log(jsonifyForm);
    const response = await fetch("/ajout_film",
        { method: 'POST',
          headers: {'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
          },
          body: JSON.stringify(jsonifyForm)
        });
    
    console.log("test");
    const data = await response.json();

    error_message = document.getElementById('error');
    error_message.innerHTML = data['error'];
}