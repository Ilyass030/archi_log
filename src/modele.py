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
                note_moyenne REAL DEFAULT 0.0
            )
        ''')
    
    conn.commit()
    cursor.close()
    conn.close()




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

# def plateforme():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="leane0208",
#         database="archi_logicielle"
#     )
#     mycursor = mydb.cursor()

#     mycursor.execute('''select * from liste_genres''')
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