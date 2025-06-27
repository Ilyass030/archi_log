# Lesserboxd
## Introduction
### Decription du projet
Le but est de reproduire le site de notation de films letterboxd.
Notre version aura une liste de films avec les personnes qui ont travaillé dessus, ses genres, l'année de sortie, ainsi que la note moyenne des utilisateurs et d'autres informations sur le film vis à vis des utilisateurs.
Les utilisateurs peuvent se suivre entre eux, dire s'ils ont vu ou aimer un film, le noter et en faire une critique.
### Organisation
Chaque personne dans l'équipe est responsable d'une partie :
- Loïc:  Flask coté serveur
- Louiza: Flask coté front et interaction avec le back-end 
- Ilyass:  Base de donnée (sqlite & python)

Cela, bien sûr, n’empêche pas de travailler ensemble sur certaines parties : l’entraide est une force.

### MCD
![MCD non affichable](MCD.png)


## 🎯 Le schéma de la base de données
Table : liste_genres
---------------------
id             INTEGER PRIMARY KEY AUTOINCREMENT  
nom            TEXT UNIQUE  


Table : liste_films
---------------------
id                  INTEGER PRIMARY KEY AUTOINCREMENT  
nom                 TEXT UNIQUE NOT NULL  
resume              TEXT  
annee_sortie        INTEGER UNIQUE  
nb_visionnage       INTEGER DEFAULT 0  
nb_notes            INTEGER DEFAULT 0  
note_moyenne        REAL DEFAULT 0.0  
genre_id            INTEGER FOREIGN KEY vers liste_genres(id)  
professionnel_id    INTEGER FOREIGN KEY vers professionnel(id)  


Table : utilisateur
---------------------
id                   INTEGER PRIMARY KEY AUTOINCREMENT  
nom                  TEXT NOT NULL  
nb_visionnage        INTEGER DEFAULT 0  
nb_notes             INTEGER DEFAULT 0  
nb_likes             INTEGER DEFAULT 0  
film_id              INTEGER FOREIGN KEY vers liste_films(id)  
utilisateur_id       INTEGER FOREIGN KEY vers utilisateur(id)  


Table : professionnel
---------------------
id                   INTEGER PRIMARY KEY AUTOINCREMENT  
nom                  TEXT NOT NULL   
prenom               TEXT  
date_naissance       TEXT   
date_deces           TEXT  
metier_id            INTEGER FOREIGN KEY vers metier(id)  


Table : metier
---------------------
id                   INTEGER PRIMARY KEY AUTOINCREMENT  
nom                  TEXT NOT NULL    



## 🌐 Liste des Endpoints

| Méthode       | URL               | Description  |
| :------------- |:-------------:| -----|
| GET           | `/`               | Page principale. Initialise la base de données si besoin et affiche les genres.  |
| GET           | `/ajouter_film`   | Recherche un film selon le nom, l'année ou les genres. |
| POST          | `/ajout_film`     | Ajoute un film à la base (JSON attendu avec nom, résumé, année, genres, note). |
| POST          | `/search_film`    | Recherche un film selon le nom, l'année ou les genres. | 
| POST          | `/film_detail`    | Affiche les détails d’un film sélectionné (form data avec `film_id`). |
| POST          | `/delete_film`    | Supprime un film par son `film_id`. |
| POST          | `/add_professionnel` | Ajoute un professionnel (acteur, réalisateur…) à un film donné. | 
| POST          | `/delete_professionnel` | Supprime un professionnel d’un film (via `film_id`, `professionnel_id`, `metier`). |



Exemple commande JSON
<details>
    POST /ajout_film
    Content-Type: application/json

    {
    "nom": "Inception",
    "resume": "Un voleur entre dans les rêves.",
    "annee_sortie": 2010,
    "genres": [{"genre": "Action"}, {"genre": "Science-Fiction"}],
    "note": 4.5
    }
</details>
