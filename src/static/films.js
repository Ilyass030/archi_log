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

    for (let key in data) {
        let film = data[key];
        let film_form = document.createElement('form');
        let input = document.createElement("input");
        let li = document.createElement("li");

        film_form.appendChild(li);
        film_form.appendChild(input);
        liste_films.appendChild(film_form);

        film_form.className = "onefilm";
        film_form.setAttribute("method","post");
        film_form.setAttribute("action","/film_detail");

        // Bloc info (titre, année, genre)
        let infoDiv = document.createElement("div");
        infoDiv.className = "film-info";
        infoDiv.style.flex = "1";
        let titre = document.createElement("span");
        titre.className = "film-title";
        titre.style.fontWeight = "bold";
        titre.textContent = film[1];

        let genresSpan = document.createElement("span");
        genresSpan.className = "genres";
        genresSpan.style.marginLeft = "14px";
        genresSpan.textContent = film[7] && film[7].length ? film[7].join(', ') : "";

        let annee = document.createElement("span");
        annee.className = "film-annee";
        annee.style.marginLeft = "14px";
        annee.textContent = film[3] ? `(${film[3]})` : "";

        infoDiv.appendChild(titre);
        infoDiv.appendChild(genresSpan);
        infoDiv.appendChild(annee);

        // Note juste après la date
        let noteSpan = document.createElement("span");
        noteSpan.className = "film-note";
        noteSpan.style.marginLeft = "14px";
        noteSpan.style.fontWeight = "bold";
        noteSpan.style.fontSize = "1.05em";
        noteSpan.style.color = "#e67e22";
        if (film[6] && film[6] > 0) {
            noteSpan.textContent = `${parseFloat(film[6]).toFixed(1)}/5`;
        } else {
            noteSpan.textContent = "Pas encore noté";
            noteSpan.style.color = "#888";
            noteSpan.style.fontWeight = "normal";
        }

        infoDiv.appendChild(noteSpan);

        li.style.width = "100%";
        li.style.display = "flex";
        li.style.alignItems = "center";
        li.style.justifyContent = "flex-start";
        li.style.padding = "0";
        li.style.background = "none";
        li.style.border = "none";

        li.appendChild(infoDiv);

        li.onclick = function() { this.parentNode.submit(); };

        input.type = "hidden";
        input.name = "film_id";
        input.value = film[0];

    }
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('search_film');
  if (form) {
    // Lance une recherche initiale pour afficher tous les films
    search_film(new Event('submit'), form);

    // Bouton annuler la recherche
    const resetBtn = document.getElementById('reset_search');
    if (resetBtn) {
      resetBtn.addEventListener('click', function() {
        form.reset();
        // Désélectionne manuellement les checkboxes si besoin
        form.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        // Remet l'année à "inconnu" si select dynamique
        const select = form.querySelector('select[name="annee_sortie"]');
        if (select) select.value = "0";
        // Relance la recherche pour tout afficher
        search_film(new Event('submit'), form);
      });
    }
  }
});