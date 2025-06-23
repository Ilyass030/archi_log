import mysql.connector

def create_list():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leane0208",
        database="archi_logicielle"
    )
    mycursor = mydb.cursor()

    mycursor.execute('''create table if not exists liste_type(
                        id int auto_increment primary key, nom varchar(20))''')

    mycursor.execute('''create table if not exists liste_plateforme(
                        id int auto_increment primary key, nom varchar(20))''')

    mycursor.execute('''create table if not exists liste_jeux(
                        id int auto_increment primary key,nom varchar(50), plateforme_id int,
                        prix int, type_id int, description varchar(500))''')
    
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (1, "FPS"))
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (2, "TPS"))
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (3, "Stratégie"))
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (4, "Simulation"))
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (5, "RPG"))
    mycursor.execute('''insert ignore into liste_type (id, nom) values(%s, %s)''', (6, "Platformer"))

    mycursor.execute('''insert ignore into liste_plateforme (id, nom) values(%s, %s)''', (1, "PC"))
    mycursor.execute('''insert ignore into liste_plateforme (id, nom) values(%s, %s)''', (2, "XBox series X"))
    mycursor.execute('''insert ignore into liste_plateforme (id, nom) values(%s, %s)''', (3, "Playstation 5"))
    mycursor.execute('''insert ignore into liste_plateforme (id, nom) values(%s, %s)''', (4, "Nintendo Switch"))
    mycursor.execute('''insert ignore into liste_plateforme (id, nom) values(%s, %s)''', (5, "Téléphone Portable"))

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

    mycursor.execute('''select j.nom, p.nom, prix, t.nom, description from liste_jeux j, liste_plateforme p, liste_type t where j.plateforme_id=p.id and j.type_id=t.id''')
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

    mycursor.execute('''select * from liste_plateforme''')
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
    insert = 'insert into liste_plateforme(nom) values("' + plateforme + '")'
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