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
        "Mystère", "Romance", "Thriller", "Film télé", "Guerre", "Western"
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
    
    conn.commit()
    cursor.close()
    conn.close()


def genre():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''select * from liste_genres''')
    genre = cursor.fetchall()
    print(genre)
    cursor.close()
    return(genre)

def add_film(nom, resume, annee_sortie, genre_ids):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    insert = '''SELECT COUNT(id) FROM liste_films WHERE nom=? AND annee_sortie=?'''
    val=(nom, annee_sortie)
    exist = cursor.execute(insert, val)
    if (exist != 0):
        return 1

    insert = '''INSERT OR IGNORE INTO liste_films (nom, resume, annee_sortie) VALUES (?, ?, ?)'''
    val = (nom, resume, annee_sortie)
    cursor.execute(insert, val)
    
    # Récupère l'id du film (même si déjà existant)
    cursor.execute('SELECT id FROM liste_films WHERE nom=? AND annee_sortie=?', (nom, annee_sortie))
    film_id = cursor.fetchone()[0]

    # Ajoute la liaison avec chaque genre
    for genre_id in genre_ids:
        cursor.execute('INSERT OR IGNORE INTO film_genre (film_id, genre_id) VALUES (?, ?)', (film_id, genre_id))
    
    conn.commit()
    cursor.close()
    return 0

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