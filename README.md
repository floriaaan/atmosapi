# Atmos'fr
Projet CESI - Réalisation d'une sonde météorologique avec un BACK-END supporté par un Raspberry Pi 3



Réalisation d'une API REST avec Flask (Python)

## Liens utiles

Site web de Atmos'fr :
```
http://emilie.dehant.webconcepteur.fr/atmosfr
```
Site demo de Atmos'Home :
```
https://floriaaan.github.io/atmos-home
```

## Comment installer le projet ⁉️

Coté serveur, (Raspberry Pi)

```

python3 -m pip install pymysql
python3 -m pip install flask
python3 -m pip install flask_restful
python3 -m pip install flask_cors
python3 -m pip install flask_swagger_ui

apt install mariadb-server
mysql-secure-installation

git clone https://github.com/floriaaan/atmos-fr

python3 install.py (Non testé)
python3 atmosapi.py

```

Coté capteur, ESP8266-01

```
python3 -m pip install esptool
esptool --port (port de connexion de votre flasher esp) erase_flash
esptool --port (PORT) --baud 115200 write_flash --flash_size=detect 0 esp8266-20190529-v1.11.bin

Intégrer les scripts sensor via un IDE compatible (ex: Thonny)
```

Coté client

```
git clone https://github.com/floriaaan/atmos-home/
Remplacer tout les '192.168.43.57' par :
-   Soit l'adresse IP du Raspberry si vous hébergez la Web App sur un autre serveur
        (requis: le serveur doit être connecté au même wifi que le Raspberry et le capteur)
-   Soit localhost ou 127.0.0.1 si vous hébergez la Web App sur le Raspberry Pi
mv /atmoshome/ /var/www/html/

```

## Status
Le rendu final est présenté Vendredi 20 Décembre 2019, lors d'une soutenance orale.
Désormais sous amélioration continue



## Crédits
- Langlois William - pour le support de l'ESP ainsi que du capteur temp/humid
- Leclerc Léo - pour l'étude du marketing du projet ainsi que l'étude de son référencement
- Dehant Emilie - pour l'étude du marketing du projet ainsi que la réalisation de la Landing Page
- Leroux Florian - pour la réalisation de l'API ainsi que de l'application Atmos'Home



