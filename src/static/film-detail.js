document.addEventListener('DOMContentLoaded', function() {
  const showBtn = document.getElementById('show-add-pro');
  const formDiv = document.getElementById('add-pro-form');
  if (showBtn && formDiv) {
    showBtn.addEventListener('click', () => {
      formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';
    });
  }

  const addProForm = document.getElementById('form-add-pro');
  if (addProForm) {
    addProForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      const formData = new FormData(addProForm);
      const response = await fetch('/add_professionnel', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      if (data.success) {
        const proList = document.getElementById('pro-list');
        const li = document.createElement('li');
        li.className = 'pro-item';
        li.setAttribute('data-pro-id', data.pro.id);
        li.setAttribute('data-metier', data.pro.metier);

        // Croix
        const btn = document.createElement('button');
        btn.className = 'delete-pro';
        btn.type = 'button';
        btn.title = 'Supprimer';
        li.appendChild(btn);

        // Infos
        const infos = document.createElement('div');
        infos.className = 'pro-infos';
        let txt = `${data.pro.nom || ''} ${data.pro.prenom || ''}`;
        if (data.pro.nationalite) txt += ` (${data.pro.nationalite})`;
        if (data.pro.date_naissance) txt += `, né(e) le ${data.pro.date_naissance}`;
        if (data.pro.date_deces) txt += `, décédé(e) le ${data.pro.date_deces}`;
        txt += ` — ${data.pro.metier}`;
        infos.textContent = txt;
        li.appendChild(infos);

        proList.appendChild(li);
        addProForm.reset();
        formDiv.style.display = 'none';
      } else if (data.error) {
        alert(data.error);
      }
    });
  }

  // Suppression dyyyyynamique d'un professionnel
  document.getElementById('pro-list').addEventListener('click', async function(e) {
    if (e.target.classList.contains('delete-pro')) {
      const li = e.target.closest('li');
      const professionnel_id = li.getAttribute('data-pro-id');
      const metier = li.getAttribute('data-metier');
      const film_id = document.querySelector('input[name="film_id"]').value;
      if (confirm("Supprimer ce professionnel de ce film ?")) {
        const formData = new FormData();
        formData.append("film_id", film_id);
        formData.append("professionnel_id", professionnel_id);
        formData.append("metier", metier);
        const response = await fetch('/delete_professionnel', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        if (data.success) {
          li.remove();
        } else {
          alert("Erreur lors de la suppression.");
        }
      }
    }
  });
});