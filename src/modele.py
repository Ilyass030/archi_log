import mysql.connector

def create_list():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )
    mycursor = mydb.cursor()

    mycursor.execute('''create table if not exists liste_genres(
                        id int auto_increment primary key, nom varchar(20))''')

    mycursor.execute('''create table if not exists liste_films(
                        id int auto_increment primary key,nom varchar(50), resume varchar(500),
                        annee_sortie unsigned int, nb_visionnage unsigned int,
                        nb_notes unsigned int, note_moyenne unsined char''')
    
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (1, "Action"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (2, "Aventure"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (3, "Animation"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (4, "Comédie"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Crime"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Documentaire"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Drama"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Famille"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Fantasy"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Histoire"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Horreur"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Musique"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Mystère"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Romance"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Thriller"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Film télé"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Guerre"))
    mycursor.execute('''insert ignore into liste_genres (id, nom) values(%s, %s)''', (5, "Western"))

    mydb.commit()
    mycursor.close()

def list():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )
    mycursor = mydb.cursor()

    mycursor.execute('''select j.nom, p.nom, prix, t.nom, description from liste_jeux j, liste_genres p, liste_type t where j.plateforme_id=p.id and j.type_id=t.id''')
    etuds = mycursor.fetchall()
    print(etuds)
    mycursor.close()
    return(etuds)

def type():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )
    mycursor = mydb.cursor()

    mycursor.execute('''select * from liste_type''')
    etuds = mycursor.fetchall()
    print(etuds)
    mycursor.close()
    return(etuds)

def plateforme():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )
    mycursor = mydb.cursor()

    mycursor.execute('''select * from liste_genres''')
    etuds = mycursor.fetchall()
    print(etuds)
    mycursor.close()
    return(etuds)

def add_type(type):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )

    mycursor = mydb.cursor()
    insert = 'insert into liste_type(nom) values("' + type + '")'
    mycursor.execute(insert)
    mydb.commit()

    mycursor.close() 

def add_plateforme(plateforme):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )

    mycursor = mydb.cursor()
    insert = 'insert into liste_genres(nom) values("' + plateforme + '")'
    mycursor.execute(insert)
    mydb.commit()

    mycursor.close()

def add_jeux(nom, plateforme, prix, type, description):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )

    mycursor = mydb.cursor()
    insert='''insert into liste_jeux(nom, plateforme_id, prix, type_id, description) values(%s, %s, %s, %s, %s)'''
    val = (nom, plateforme, prix, type, description)
    mycursor.execute(insert, val)
    mydb.commit()

    mycursor.close()
    return(list())