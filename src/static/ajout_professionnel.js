document.addEventListener('DOMContentLoaded', function() {
  const formDiv = document.getElementById('add-pro-form');

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

      console.log(data);

      const prof_info = document.getElementById('afficher_prof');
      const prof_id = document.getElementById('prof_id');
      prof_id.innerHTML = data['prof'][0][0];
      prof_id.value = data['prof'][0][0];
      prof_info.innerHTML = data['prof'][0][2] + "<strong> " + data['prof'][0][1] + "</strong>";
      document.getElementById("prof_detail").style.visibility = "visible";

      if (data['error']) {
          const error_message = document.getElementById('error');
          const success_message = document.getElementById('succes');
          error_message.innerHTML = data['error'];
          success_message.innerHTML = "";
      } else {
          const error_message = document.getElementById('error');
          const success_message = document.getElementById('succes');
          success_message.innerHTML = "Professionnel ajouté";
          error_message.innerHTML = "";
      }
    });
  }
})
