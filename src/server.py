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
    return render_template("films.html", error="", Genres=modele.genre())


@app.route("/liste")
def go_to():
    return render_template('liste.html', jeux=modele.list())


@app.route("/type", methods=["POST"])
def add_type():
    type = request.form["type"]
    if (type == "" or len(type) > 20):
        return render_template('infos.html', error="Veuillez saisir un type avec moins de 20 caractêres")
    types = modele.type()

    for elem in types:
        if (elem[1] == type):
            return render_template('info.html', error="Ce type de jeux est déjà listé")
    modele.add_type(type)
    return general()


@app.route("/plateforme", methods=["POST"])
def add_plateforme():
    plateforme = request.form["plateforme"]
    if (plateforme == "" or len(plateforme) > 20):
        return render_template('infos.html', error="Veuillez saisir une plateforme avec moins de 20 caractêres")
    plateformes = modele.type()

    for elem in plateformes:
        if (elem[1] == plateforme):
            return render_template('info.html', error="Cette plateforme est déjà listée")
    modele.add_plateforme(plateforme)
    return general()


@app.route("/ajout_film", methods=["POST"])
def add_jeu():
    data = request.form

    #error handling
    if(data["nom"] == ""):
        return render_template('add_film.html', error="Veuillez saisir un nom", Genres=modele.genre())
    

    if (modele.ajout_film(data["nom"], data["resume"], int(data["annee_sortie"]), data.getlist("genres[]")) == 1):
        return render_template('add_film.html', error="Ce film est déjà dans la base de donnée", Genres=modele.genre())

    return render_template("add_film.html", error="", Genres=modele.genre())

@app.route("/ajouter_film", methods=["GET"])
def ajouter_film_form():
    return render_template("index.html", Genres=modele.genre(), current_year=datetime.now().year)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)