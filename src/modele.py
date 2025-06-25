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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS professionnel_metier (
        professionnel_id INTEGER,
        metier_id INTEGER,
        PRIMARY KEY (professionnel_id, metier_id),
        FOREIGN KEY (professionnel_id) REFERENCES professionnel(id),
        FOREIGN KEY (metier_id) REFERENCES metier(id)
    )
''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS film_professionnel (
        film_id INTEGER,
        professionnel_id INTEGER,
        PRIMARY KEY (film_id, professionnel_id),
        FOREIGN KEY (film_id) REFERENCES liste_films(id),
        FOREIGN KEY (professionnel_id) REFERENCES professionnel(id)
    )   
''')
                   
    
    conn.commit()
    cursor.close()
    conn.close()


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
    film = cursor.execute('''SELECT * FROM liste_films f WHERE f.id=?''', film_id).fetchall()
    cursor.close()
    conn.close()
    return(film)

def film_genres(film_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM liste_genres g 
                    JOIN film_genre fg ON g.id=fg.genre_id
                    WHERE ?=fg.film_id''', film_id)
    film_genres = cursor.fetchall()
    print(film_genres)
    cursor.close()
    return(film_genres)

def add_film(nom, resume, annee_sortie, genre_ids):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    insert = '''SELECT COUNT(id) FROM liste_films WHERE nom=? AND annee_sortie=?'''
    val=(nom, annee_sortie)
    exist = cursor.execute(insert, val).fetchall()[0]
    print(exist)
    if (exist[0] != 0):
        return 1
    insert = '''INSERT OR IGNORE INTO liste_films (nom, resume, annee_sortie) VALUES (?, ?, ?)'''
    val = (nom, resume, annee_sortie)
    cursor.execute(insert, val)
    # Récupère l'id du film (même si déjà existant)
    cursor.execute('SELECT id FROM liste_films WHERE nom=? AND annee_sortie=?', (nom, annee_sortie))
    film_id = cursor.fetchone()[0]

    # Ajoute la liaison avec chaque genre
    for genre_id in genre_ids:
        print(genre_id)
        cursor.execute('INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)', (film_id, genre_id))
    
    conn.commit()
    cursor.close()
    return 0


def delete_film(nom, annee_sortie):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM liste_films WHERE nom=? AND annee_sortie=?', (nom, annee_sortie))
    film = cursor.fetchone()
    if film is None:
        cursor.close()
        conn.close()
        return 1
    film_id = film[0]


    cursor.execute('DELETE FROM film_genre WHERE film_id=?', (film_id,))


    cursor.execute('DELETE FROM liste_films WHERE id=?', (film_id,))

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

def search_film(nom, genre_id, annee):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = '''
        SELECT DISTINCT f.*
        FROM liste_films f
        LEFT JOIN film_genre fg ON f.id = fg.film_id
        WHERE 1=1
    '''

    cursor.execute(query)
    film_id = cursor.fetchall()

    print(film_id)
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

    print(query)

    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

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