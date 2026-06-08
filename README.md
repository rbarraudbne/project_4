# ♟ Gestionnaire de tournois d'échecs

Application console en Python pour gérer des tournois d'échecs selon le système suisse. 
Le logiciel fonctionne en local et n'a pas besoin de connexion internet, il permet de créer et de stocker les joueurs dans fichier JSON, et de même pour les tournois.
Il suit la conception Modèle-Vue-Contrôleur (MVC).

## Prérequis

- Python 3.10+
- pip

## Installation
 
```bash
pip install -r requirements.txt
```
 
## Lancer le programme
 
```bash
python main.py
```

## Structure du projet
 
```
Chess_project/
├── models/
│   ├── player.py        # Modèle joueur
│   ├── tournament.py    # Modèle tournoi (génération de paires, classement)
│   ├── round.py         # Modèle tour
│   ├── database.py      # Gestion des fichiers JSON
│   └── match.py         # Modèle match
├── views/
│   ├── baseview.py      # Classe de base (saisie, affichage)
│   ├── main_menu.py     # Menu principal
│   ├── player.py        # Vue joueur
│   ├── tournament.py    # Vue tournoi
│   └── report.py        # Vue rapports
├── controllers/
│   ├── player_controller.py      # Contrôleur joueur
│   ├── tournament_controller.py  # Contrôleur tournoi
│   └── report_controller.py      # Contrôleur rapports
main.py                  # Point d'entrée
data/                    # Fichiers JSON générés automatiquement
requirements.txt
```
 
## Générer le rapport flake8
 
```bash
flake8 --max-line-length=119 --format=html --htmldir=flake8_rapport
```
 
Le rapport HTML sera disponible dans le dossier `flake8_rapport/`.
