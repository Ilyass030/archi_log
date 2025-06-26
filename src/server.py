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
    
    film_id = modele.add_film(data["nom"], data["resume"], int(data["annee_sortie"]), genres)
    if (film_id == -1):
        return_value["error"] = "Ce film est déjà dans la base de donnée"
        return jsonify(return_value)
        # return render_template('index.html', error="Ce film est déjà dans la base de donnée", Genres=modele.genre())
    
    return render_template("film_detail.html", Film=modele.get_film(film_id), Genres=modele.film_genres(film_id))


@app.route("/ajouter_film", methods=["GET"])
def ajouter_film_form():
    return render_template("index.html", error="", Genres=modele.genre())


@app.route("/search_film", methods=["POST"])
def search_film():
    data = request.form
    return render_template("films.html", Genres=modele.genre(), films=modele.search_film(data.get("name", None), data.getlist("genres[]", None), data.get("annee_sortie", None)))


@app.route("/film_detail", methods=["POST"])
def film_detail():
    film_id = request.form["film_id"]
    return render_template("film_detail.html", Film=modele.get_film(film_id), Genres=modele.film_genres(film_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)