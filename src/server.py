from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS
from enum import Enum

import modele

class Types(Enum):
    FPS = 0
    Strategie = 1
    Platformer = 2
    Metroidvania = 3
    Autre = 4

class Plateformes(Enum):
    PC = 0
    Playstation = 1
    XBox = 2
    Nintendo = 3
    Mobile = 4
    Autre = 5

app = Flask(__name__)
CORS(app)

@app.route("/")
def general():
    modele.create_list()
    return render_template("infos.html", error="", Types=modele.type(), Plateformes=modele.plateforme())


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


@app.route("/liste", methods=["POST"])
def add_jeu():
    data = request.form

    #error handling
    if(data["nom"] == ""):
        return render_template('infos.html', error="Veuillez saisir un nom", Types=Types, Plateformes=Plateformes)
    if(not data["prix"].isdigit()):
        return render_template('infos.html', error="Veuillez saisir un nombre entier pour le prix", Types=Types, Plateformes=Plateformes)
    if(data["description"] == ""):
        return render_template('infos.html', error="Veuillez saisir une description", Types=Types, Plateformes=Plateformes)
    
    modele.add_jeux(data["nom"], int(data["plateforme"]), int(data["prix"]), int(data["type"]), data["description"])
    return render_template('liste.html', jeux=modele.list())

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)