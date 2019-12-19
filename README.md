# Atmos'fr
Projet CESI - Réalisation d'une sonde météorologique avec un BACK-END supporté par un Raspberry Pi 3


Réalisation d'une API REST avec Flask (Python)

## Comment installer le projet ⁉️

Coté serveur, Raspberry Pi

```

python3 -m pip install pymysql
python3 -m pip install flask
python3 -m pip install flask_restful
python3 -m pip install flask_swagger_ui

apt install mariadb-server
mysql-secure-installation

git clone https://github.com/floriaaan/atmos-fr

python3 install.py
python3 atmosapi.py

```

Coté capteur, ESP8266-01

```


```

Coté client

```
unzip atmoshome.zip
Remplacer tout les '192.168.43.57' par :
-   Soit l'adresse IP du Raspberry si vous hébergez la Web App sur un autre serveur (requis: le serveur doit être connecté au même wifi que le Raspberry et le capteur)
-   Soit localhost ou 127.0.0.1 si vous hébergez la Web App sur le Raspberry Pi

```

## Status
Le rendu final est présenté Vendredi 20 Décembre 2019, lors d'une soutenance orale.



## Crédits
- Langlois William
- Leclerc Léo
- Dehant Emilie
- Leroux Florian

