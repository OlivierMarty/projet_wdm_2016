# Projet de Web Data Management 2016


## Installation

Avec Python 3, faites :

    git clone git@github.com:OlivierMarty/projet_wdm_2016.git
    cd projet_wdm_2016
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Configuration

Dans le fichier `config.py`, il faut configurer une API pour le service
jcdecaux_vls (pour l'obtenir, aller à http://developer.jcdecaux.com/)

La section notifications de ce fichier permet de configurer la façon dont les
notifications sont envoyées :
 - sendmail : envoie un mail (nécessite que la commande `mail` foncitonne)
 - print : affiche dans la console
 - free : envoie un SMS vie l'API free (voir http://mobile.free.fr/)

## Utilisation

Pour lancer le programme :

    python3 main.py

Les accès à Google Calendar et Gmail sera demandé au premier lancement.

Pour lancer la démo :

    python3 demo.py

### API utilisées

RATP, jcdecaux_vls (Vélib', Vélo'V, Bicloo, etc) et Transilien (pas vraiment
intégré car on ne connait pas (encore) la localisation des stations).

## Note

Le code gère peu d'exceptions : à la moindre erreur le programme plantera.
