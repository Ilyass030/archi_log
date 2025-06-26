import sqlite3

def create_list():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liste_genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE
        )
    ''')

    genres = [
        "Action", "Aventure", "Animation", "Comédie", "Crime", "Documentaire",
        "Drama", "Famille", "Fantasy", "Histoire", "Horreur", "Musique",
        "Mystère", "Romance", "Thriller", "Science-fiction", "Film télé", "Guerre", "Western"
    ]

    for genre in genres:
        cursor.execute("INSERT OR IGNORE INTO liste_genres (nom) VALUES (?)", (genre,))

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS liste_films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                resume TEXT,
                annee_sortie INTEGER,
                nb_visionnage INTEGER DEFAULT 0,
                nb_notes INTEGER DEFAULT 0,
                note_moyenne REAL DEFAULT 0.0,
                UNIQUE(nom, annee_sortie)
            )
        ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS film_genre (
        film_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (film_id, genre_id),
        FOREIGN KEY (film_id) REFERENCES liste_films(id),
        FOREIGN KEY (genre_id) REFERENCES liste_genres(id)
    )
''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        nb_visionnage INTEGER DEFAULT 0,
        nb_notes INTEGER DEFAULT 0,
        nb_likes INTEGER DEFAULT 0
    )
''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateur_film (
        utilisateur_id INTEGER,
        film_id INTEGER,
        visionnage INTEGER DEFAULT 0,
        like INTEGER DEFAULT 0,
        note INTEGER DEFAULT 0,
        PRIMARY KEY (film_id, utilisateur_id),
        FOREIGN KEY (film_id) REFERENCES liste_films(id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
    )
''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateur_utilisateur (
        utilisateur_id INTEGER,
        ami_id INTEGER,
        PRIMARY KEY (utilisateur_id, ami_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id),
        FOREIGN KEY (ami_id) REFERENCES utilisateur(id)
    )
''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS professionnel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT,
        nationalite TEXT,
        date_naissance TEXT,
        date_deces TEXT
    )
''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS metier (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL
    )
''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS professionnel_metier_film (
        professionnel_id INTEGER,
        metier_id INTEGER,
        film_id INTEGER,
        PRIMARY KEY (professionnel_id, metier_id, film_id),
        FOREIGN KEY (professionnel_id) REFERENCES professionnel(id),
        FOREIGN KEY (metier_id) REFERENCES metier(id)
        FOREIGN KEY (film_id) REFERENCES liste_films(id)
    )
''')

                   
    
    conn.commit()
    cursor.close()
    conn.close()

##__________________ Fonctions de gestion des films __________________##

def genre():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''select * from liste_genres''')
    genre = cursor.fetchall()
    cursor.close()
    conn.close()
    return(genre)

def get_film(film_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    film = cursor.execute('''SELECT * FROM liste_films f WHERE f.id=?''', (film_id,)).fetchall()
    cursor.close()
    conn.close()
    return(film)

def film_genres(film_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM liste_genres g 
                    JOIN film_genre fg ON g.id=fg.genre_id
                    WHERE ?=fg.film_id''', (film_id,))
    film_genres = cursor.fetchall()
    cursor.close()
    return(film_genres)

def add_film(nom, resume, annee_sortie, genre_ids):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    get_film_id = '''SELECT id FROM liste_films WHERE nom=?'''
    val_id=[nom]

    if annee_sortie:
        get_film_id += " AND annee_sortie=?"
        val_id.append(annee_sortie)
    
    exist = cursor.execute(get_film_id, val_id).fetchall()
    if (len(exist) != 0):
        return exist[0][0] * -1
    
    insert = '''INSERT OR IGNORE INTO liste_films (nom, resume, annee_sortie) VALUES (?, ?, ?)'''
    val = (nom, resume, annee_sortie)
    cursor.execute(insert, val)
    # Récupère l'id du film (même si déjà existant)
    cursor.execute(get_film_id, val_id)
    film_id = cursor.fetchone()[0]

    # Ajoute la liaison avec chaque genre
    for genre_id in genre_ids:
        cursor.execute('INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)', (film_id, genre_id))
    
    conn.commit()
    cursor.close()
    return film_id


def delete_film(id_film):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # cursor.execute('SELECT id FROM liste_films WHERE id=?', (id_film,))
    # film = cursor.fetchone()
    film = get_film((id_film,))
    if film is None:
        cursor.close()
        conn.close()
        return 0
    # film_id = film[0]

    cursor.execute('DELETE FROM film_genre WHERE film_id=?', (id_film,))


    cursor.execute('DELETE FROM liste_films WHERE id=?', (id_film,))

    conn.commit()
    cursor.close()
    conn.close()
    return 1

def modify_film(film_id, nom=None, resume=None, annee_sortie=None, genre_ids=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    updates = []
    params = []
    if nom is not None:
        updates.append("nom=?")
        params.append(nom)
    if resume is not None:
        updates.append("resume=?")
        params.append(resume)
    if annee_sortie is not None:
        updates.append("annee_sortie=?")
        params.append(annee_sortie)

    if updates:
        query = f"UPDATE liste_films SET {', '.join(updates)} WHERE id=?"
        params.append(film_id)
        cursor.execute(query, params)

    # Mettre à jour les genres si demandé
    if genre_ids is not None:
        cursor.execute('DELETE FROM film_genre WHERE film_id=?', (film_id,))
        for genre_id in genre_ids:
            cursor.execute('INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)', (film_id, genre_id))

    conn.commit()
    cursor.close()
    conn.close()
    return 0

# def search_film(nom,genre_id,annee):
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     cursor.execute('SELECT DISTINC f.* FROM liste_films f ' \
#     'JOIN film_genre fg ON f.id = fg.film_id ' \
#     'JOIN liste_genres g ON fg.genre_id = g.id ' \
#     'WHERE f.nom LIKE ? ' \
#     'AND g.id LIKE ? ' \
#     'AND f.annee_sortie LIKE ?',
#     ('%' + nom + '%', genre_id , annee))
    # result = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # return result

def search_film(nom=None, genre_id=None, annee=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT DISTINCT f.*
        FROM liste_films f
        LEFT JOIN film_genre fg ON f.id = fg.film_id
        WHERE 1=1
    '''

    cursor.execute(query)
    params = []

    if nom:
        query += " AND f.nom LIKE ?"
        params.append(f"%{nom}%")

    if genre_id:
        query += '''AND NOT EXISTS(SELECT id FROM liste_genres g WHERE g.id IN(?'''
        params.append(genre_id[0])
        for i in range(1, len(genre_id)):
            query += " ,?"
            params.append(genre_id[i])
        query += ''') AND  NOT EXISTS(
                    SELECT * FROM liste_films ftg
                    WHERE f.id = ftg.id
                    AND fg.genre_id = g.id))'''

    if annee:
        query += " AND f.annee_sortie = ?"
        params.append(annee)

    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

##__________________ Fonctions de gestion des utilisateurs __________________##


def add_utilisateur(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO utilisateur (nom) VALUES (?)', (nom,))
    conn.commit()
    cursor.close()
    conn.close()

def add_film_utilisateur(utilisateur_id, film_id, visionnage=0, like=0, note=0): #pas sur que c a soit ca
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO utilisateur_film (utilisateur_id, film_id, visionnage, like, note) VALUES (?, ?, ?, ?, ?)',
                   (utilisateur_id, film_id, visionnage, like, note))
    conn.commit()
    cursor.close()
    conn.close()

def add_ami(utilisateur_id, ami_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO utilisateur_utilisateur (utilisateur_id, ami_id) VALUES (?, ?)', (utilisateur_id, ami_id))
    conn.commit()
    cursor.close()
    conn.close()

##__________________ Fonctions de gestion des équipes/professionnel... __________________##



def add_professionnel(nom, prenom=None, nationalite=None, date_naissance=None, date_deces=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO professionnel (nom, prenom, nationalite, date_naissance, date_deces) VALUES (?, ?, ?, ?, ?)',
                   (nom, prenom, nationalite, date_naissance, date_deces))
    conn.commit()
    cursor.close()
    conn.close()

def add_metier(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO metier (nom) VALUES (?)', (nom,))
    conn.commit()
    cursor.close()
    conn.close()

#def add_professionnel_metier(professionnel_id, metier_id):#jsp s'il l en faut une


    

# def list():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )
#     mycursor = mydb.cursor()

#     mycursor.execute('''select j.nom, p.nom, prix, t.nom, description from liste_jeux j, liste_genres p, liste_type t where j.plateforme_id=p.id and j.type_id=t.id''')
#     etuds = mycursor.fetchall()
#     print(etuds)
#     mycursor.close()
#     return(etuds)

# def type():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )
#     mycursor = mydb.cursor()

#     mycursor.execute('''select * from liste_type''')
#     etuds = mycursor.fetchall()
#     print(etuds)
#     mycursor.close()
#     return(etuds)



# def add_type(type):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )

#     mycursor = mydb.cursor()
#     insert = 'insert into liste_type(nom) values("' + type + '")'
#     mycursor.execute(insert)
#     mydb.commit()

#     mycursor.close() 

# def add_plateforme(plateforme):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )

#     mycursor = mydb.cursor()
#     insert = 'insert into liste_genres(nom) values("' + plateforme + '")'
#     mycursor.execute(insert)
#     mydb.commit()

#     mycursor.close()

# def add_jeux(nom, plateforme, prix, type, description):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )

#     mycursor = mydb.cursor()
#     insert='''insert into liste_jeux(nom, plateforme_id, prix, type_id, description) values(%s, %s, %s, %s, %s)'''
#     val = (nom, plateforme, prix, type, description)
#     mycursor.execute(insert, val)
#     mydb.commit()

#     mycursor.close()
#     return(list())