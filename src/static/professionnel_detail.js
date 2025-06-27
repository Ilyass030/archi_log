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
      const response = await fetch('/add_crew', {
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
});