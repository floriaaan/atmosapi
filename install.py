import pymysql
import os

DB = pymysql.connect(
    host="localhost",
    user="atmos",
    passwd="atmos",
    charset="utf8"
)

dbCursor = DB.cursor()

dbCursor.execute("CREATE DATABASE atmos")
DB.commit()
DB.close()

os.system("mysql -u atmos -patmos atmos < generate_Atmosfr.sql")

atmosDB = pymysql.connect(
    host="localhost",
    user="atmos",
    passwd="atmos",
    db="atmos",
    charset="utf8"
)

dbCursor = atmosDB.cursor()

dbCursor.execute("INSERT INTO UTILISATEUR (utilisateur_pseudo, utilisateur_email, utilisateur_mdp) VALUES ('atmos_admin', 'atmosfrcontact@gmail.com', 'atmos')")
atmosDB.commit()

dbCursor.execute("INSERT INTO SONDE (id_utilisateur, sonde_pos_latitude, sonde_pos_longitude, sonde_nom, sonde_active) VALUES (1, 49.477, 1.091, 'prototype', 1)")
atmosDB.commit()

dbCursor.execute("INSERT INTO MESURE (id_sonde, mesure_date, mesure_temp, mesure_humidite) VALUES (1, '2019/12/09 17:30:00', 20.5, 50), (1, '2019/12/09 18:30:00', 19.6, 70)")
atmosDB.commit()


print("Votre AtmosBase est installée")

