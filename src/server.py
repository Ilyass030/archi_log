from flask import Flask, request, render_template, jsonify, abort, session, redirect, url_for
from flask_cors import CORS
from enum import Enum
from datetime import datetime

import modele

app = Flask(__name__)
app.secret_key = "votre_cle_secrete"  # Ajoute une clé secrète pour la session
CORS(app)

@app.route("/")
def general():
    modele.create_list()
    nom_utilisateur = session.get("utilisateur")
    return render_template("films.html", Genres=modele.genre(), nom_utilisateur=nom_utilisateur)


@app.route("/ajout_film", methods=["POST"])
def add_film():
    data = request.json
    return_value = {}

    if(data["nom"] == ""):
        return_value["error"] = "Veuillez saisir un nom"
        return jsonify(return_value)

    genres = []
    for pair in data["genres"]:
        genres.append(pair["genre"])

    annee = int(data["annee_sortie"])
    if (annee == 0):
        annee = None

    # Récupère la note
    note = data.get("note")
    note = float(note) if note else None

    film_id = modele.add_film(data["nom"], data["resume"], annee, genres, note)
    if (film_id < 0):
        film_id *= -1
        return_value["error"] = "Ce film est déjà dans la base de donnée"
    return_value["film"] = modele.get_film(film_id)
    return jsonify(return_value)


@app.route("/ajouter_film", methods=["GET"])
def ajouter_film_form():
    return render_template("index.html", error="", Genres=modele.genre())


@app.route("/modify_film", methods=["POST"])
def modifier_film_form():
    film_id = request.form["film_id"]
    return render_template("modify_film.html", Film=modele.get_film(film_id), Genres=modele.genre(), filmGenres=modele.film_genres(film_id))


@app.route("/modifier_film", methods=["POST"])
def modifier_film():
    data=request.form
    modele.modify_film(data["film_id"], data.get("resume", None), int(data["annee_sortie"]), data.getlist("genres[]", None))
    return render_template("film_detail.html", Film=modele.get_film(data["film_id"]), Genres=modele.film_genres(data["film_id"]))

@app.route("/search_film", methods=["POST"])
def search_film():
    data = request.json

    annee = int(data["annee_sortie"])
    nom = data["nom"]
    genres = []
    for pair in data["genres"]:
        genres.append(pair["genre"])

    if (annee == 0):
        annee = None

    if nom=="":
        nom = None

    return_value = modele.search_film(nom, genres, annee)
    return jsonify(return_value)

@app.route("/film_detail", methods=["POST"])
def film_detail():
    film_id = request.form["film_id"]
    return render_template(
        "film_detail.html",
        Film=modele.get_film(film_id),
        Genres=modele.film_genres(film_id),
        Crew=modele.get_professionnels_film(film_id),
        Professionnel= modele.all_professionnel(),
        Metiers=modele.metier()
    )

@app.route("/ajouter_professionnel", methods=["GET"])
def ajouter_professionnel():
    return render_template(
        "ajouter_professionnel.html",
        Metiers=modele.metier(),
    )

@app.route("/professionnel_detail", methods=["POST"])
def professionnel_detail():
    prof_id = request.form["prof_id"]
    return render_template(
        "professionnel_detail.html",
        Prof=modele.get_professionnel(prof_id),
        Films=modele.get_films_professionnel(prof_id)  # <-- AJOUTE CET ARGUMENT
    )

@app.route("/delete_film", methods=["POST"])
def delete_film_route():
    film_id = request.form["film_id"]
    if modele.delete_film(film_id):
        return render_template("films.html", Genres=modele.genre(), films=modele.search_film())
    else:
        return render_template("film_detail.html", Film=modele.get_film(film_id), Genres=modele.film_genres(film_id), error="Erreur lors de la suppression")
    
@app.route("/add_professionnel", methods=["POST"])
def add_professionnel():
    nom = request.form["nom"]
    return_value = {}
    prenom = request.form.get("prenom")
    date_naissance = request.form.get("date_naissance")
    date_deces = request.form.get("date_deces")

    # Ajoute le professionnel (fonction existante)
    prof_id = modele.add_professionnel_no_metier(nom, prenom, date_naissance, date_deces)
    if (prof_id < 0):
        prof_id *= -1
        return_value["error"] = "Ce professionnel est déjà dans la base de donnée"
    return_value["prof"] = modele.get_professionnel(prof_id)
    return jsonify(return_value)


@app.route("/add_crew", methods=["POST"])
def add_professionnel_route():
    film_id = request.form["film_id"]
    prof_id = request.form["prof_id"]
    metier_id = request.form["metier_id"]

    # Ajoute le professionnel (fonction existante)
    modele.add_professionnel_metier_film(prof_id, metier_id, film_id)
    return render_template(
        "film_detail.html",
        Film=modele.get_film(film_id),
        Genres=modele.film_genres(film_id),
        Crew=modele.get_professionnels_film(film_id),
        Professionnel= modele.all_professionnel(),
        Metiers=modele.metier()
    )

@app.route("/delete_professionnel", methods=["POST"])
def delete_professionnel_route():
    film_id = request.form["film_id"]
    professionnel_id = request.form["professionnel_id"]
    metier_id = request.form["metier_id"]
    modele.delete_professionnel_metier_film(professionnel_id, metier_id, film_id)
    return jsonify({"success": True})

@app.route("/ajouter_utilisateur", methods=["GET"])
def ajouter_utilisateur_form():
    return render_template("add.utilisateur.html")

@app.route("/ajout_utilisateur", methods=["POST"])
def ajout_utilisateur():
    identifiant = request.form["identifiant"]
    mot_de_passe = request.form["mot_de_passe"]
    # Utilise identifiant comme nom si tu ne veux que pseudo/mot de passe
    nom = identifiant
    prenom = None
    email = None
    modele.add_utilisateur_complet(identifiant, mot_de_passe, nom, prenom, email)
    return render_template("films.html", Genres=modele.genre())

@app.route("/connexion", methods=["GET"])
def connexion_form():
    return render_template("connexion.html")

@app.route("/connexion", methods=["POST"])
def connexion():
    identifiant = request.form["identifiant"]
    mot_de_passe = request.form["mot_de_passe"]
    utilisateur = modele.check_connexion(identifiant, mot_de_passe)
    if utilisateur:
        session["utilisateur"] = utilisateur[1]  # nom
        session["identifiant"] = utilisateur[3]  # identifiant
        return redirect(url_for("general"))
    else:
        return render_template("connexion.html", error="Identifiant ou mot de passe incorrect")

@app.route("/deconnexion")
def deconnexion():
    session.clear()  # Vide toute la session
    return redirect(url_for("general"))

# @app.route("/update_film", methods=["POST"])
# def update_film():
  


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

