from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS
from enum import Enum
from datetime import datetime

import modele

app = Flask(__name__)
CORS(app)

@app.route("/")
def general():
    modele.create_list()
    return render_template("films.html", Genres=modele.genre())


@app.route("/ajout_film", methods=["POST"])
def add_film():
    data = request.json
    return_value = {} #type : dict

    #error handling
    if(data["nom"] == ""):
        return_value["error"] = "Veuillez saisir un nom"
        return jsonify(return_value)

    genres = []
    for pair in data["genres"]:
        genres.append(pair["genre"])

    annee = int(data["annee_sortie"])
    if (annee == 0):
        annee = None
    
    film_id = modele.add_film(data["nom"], data["resume"], annee, genres)
    if (film_id < 0):
        film_id *= -1
        return_value["error"] = "Ce film est déjà dans la base de donnée"
    return_value["film"] = modele.get_film(film_id)
        # return render_template('index.html', error="Ce film est déjà dans la base de donnée", Genres=modele.genre())
    return jsonify(return_value)


@app.route("/ajouter_film", methods=["GET"])
def ajouter_film_form():
    return render_template("index.html", error="", Genres=modele.genre())


@app.route("/search_film", methods=["POST"])
def search_film():
    data = request.form

    annee = int(data["annee_sortie"])
    nom = data["nom"]
    # genres = []
    # for pair in data["genres"]:
    #     genres.append(pair["genre"])
    if (annee == 0):
        annee = None

    if nom=="":
        nom = None


    
    return render_template("films.html", Genres=modele.genre(), films=modele.search_film(data.get("name", None), data.getlist("genres[]", None), annee))


@app.route("/film_detail", methods=["POST"])
def film_detail():
    film_id = request.form["film_id"]
    return render_template("film_detail.html", Film=modele.get_film(film_id), Genres=modele.film_genres(film_id))

@app.route("/delete_film", methods=["POST"])
def delete_film_route():
    film_id = request.form["film_id"]
    if modele.delete_film(film_id):
        return render_template("films.html", Genres=modele.genre(), films=modele.search_film())
    else:
        return render_template("film_detail.html", Film=modele.get_film(film_id), Genres=modele.film_genres(film_id), error="Erreur lors de la suppression")
    
# @app.route("/update_film", methods=["POST"])
# def update_film():
  


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

