# OPCO-ATLAS-Module-3-Brief-1
M3 : Intégrer des nouvelles données en faisant évoluer le pipeline de processing et le modèle d'IA

## Configuration de l'environnement virtuel python

````
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
````

## Structure du projet

OPCO-ATLAS-Module-3-Brief-1/
│
├── app/
│ ├── main.py # Démarrage de l’API FastAPI
│ ├── database.py # Connexion PostgreSQL via SQLAlchemy
│ ├── models.py # ORM : Client & Pret
│ ├── schemas.py # Schémas Pydantic pour l’API
│ ├── crud.py # Fonctions d’accès et manipulation DB
│ ├── routers/
│ │ ├── clients.py # Routes CRUD Client
│ │ └── prets.py # Routes CRUD Pret
│ └── scripts/
│ └── import_csv.py # Script d’import depuis le CSV
│
├── data/
│ └── data.csv # Jeu de données
│
├── docker-compose.yml # Contient le service PostgreSQL
├── requirements.txt # Dépendances Python
└── README.md

## Contexte

Pour illustrer l'utilisation de la méthode Merise, je vais considérer pour ce brief que dans le fichier client de la banque, un même client pourrait avoir contracté plusieurs prêts.
Je crée donc une table **client** et une table **pret**.
On fait correspondre les types de données entre le csv et la base de données. Les interprétations (booléens, catégories, normalisation) seront faites pendant la phase IA.

**models.py** : modèles de mapping base de données - SQLAlchemy

## Fonctionnalités

### Service PostgreSQL

Démarrage du service :

````
docker compose up -d
````

Accès à la base de données :

````
sudo -u postgres psql -h localhost -p 5436 -U fastia
````

### Import des données

Lancement du script d'import du fichier data/data.csv dans la base de données PostgreSQL :

````
python -m scripts.import_csv
````

### API FastAPI

Lancement :

````
python -m uvicorn app.predict_api:app --reload
````

Routes

Clients
Méthode	Route	Description
GET	/clients	Liste des clients
GET	/clients/{id}	Détails d’un client
POST	/clients	Ajouter un client
DELETE	/clients/{id}	Supprimer un client
PUT	/clients/{id}	Mettre à jour un client
Prets
Méthode	Route	Description
GET	/prets	Liste des prêts
GET	/prets/{id}	Détails d’un prêt
POST	/prets	Ajouter un prêt
DELETE	/prets/{id}	Supprimer un prêt
PUT	/prets/{id}	Mettre à jour un prêt

### Tests API

```
PYTHONPATH=. pytest
```
