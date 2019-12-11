INSERT INTO UTILISATEUR (utilisateur_pseudo, utilisateur_email, utilisateur_mdp) VALUES ('atmos_admin', 'atmosfrcontact@gmail.com', 'atmos')
INSERT INTO SONDE (id_utilisateur, sonde_pos_latitude, sonde_pos_longitude, sonde_nom) VALUES (1, 49.477, 1.091, 'prototype')
INSERT INTO CAPTEUR (id_sonde, capteur_mesure, capteur_valeur) VALUES ( 1, 'ESP8266', 0)
INSERT INTO MESURE (id_capteur, mesure_date, mesure_temp, mesure_humidite) VALUES (1, '2019/12/09 17:30:00', 20.5, 50), (1, '2019/12/09 18:30:00', 19.6, 70);