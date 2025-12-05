import pytest
from fastapi.testclient import TestClient
from app.predict_api import app
from app.database import SessionLocal, Base, engine
from app.models import Client, Pret

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_predict():
    payload = {
        "age": 48,
        "taille": 172,
        "poids": 75,
        "sexe": "H",
        "sport_licence": "non",
        "niveau_etude": "bac+2",
        "region": "Occitanie",
        "smoker": "non",
        "nationalité_francaise": "oui",
        "revenu_estime_mois": 2100
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "montant_pret" in data
    assert isinstance(data["montant_pret"], float)


# ---------------------------------------------------------
# Nettoyage de la base de données entre chaque tests
# ---------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_db():
    """Réinitialise la base avant chaque test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------
# TEST API: Clients
# ---------------------------------------------------------

def test_create_client():
    response = client.post(
        "/clients/",
        json={
            "age": 25,
            "taille": 175.0,
            "poids": 70.5,
            "sport_licence": "non",
            "smoker": "oui",
            "niveau_etude": "bac",
            "region": "Occitanie",
            "situation_familiale": "célibataire",
            "historique_credits": 1.5,
            "risque_personnel": 0.2,
            "score_credit": 0.8,
            "date_creation_compte": "2024-01-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["age"] == 25


def test_get_clients_list():
    # Create 1 client
    client.post(
        "/clients/",
        json={
            "age": 30,
            "taille": 180.0,
            "poids": 80.0,
            "sport_licence": "oui",
            "smoker": "non",
            "niveau_etude": "bac+2",
            "region": "Île-de-France",
            "situation_familiale": "marié",
            "historique_credits": 2.0,
            "risque_personnel": 0.3,
            "score_credit": 0.9,
            "date_creation_compte": "2024-02-01"
        }
    )

    response = client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_delete_client():
    # Create
    res = client.post(
        "/clients/",
        json={
            "age": 20,
            "taille": 165.0,
            "poids": 55.0,
            "sport_licence": "non",
            "smoker": "non",
            "niveau_etude": "bac",
            "region": "Bretagne",
            "situation_familiale": "célibataire",
            "historique_credits": 0.5,
            "risque_personnel": 0.1,
            "score_credit": 0.7,
            "date_creation_compte": "2023-05-01"
        }
    )
    client_id = res.json()["id"]

    # Delete
    del_res = client.delete(f"/clients/{client_id}")
    assert del_res.status_code == 200

    # Ensure deleted
    get_res = client.get(f"/clients/{client_id}")
    assert get_res.status_code == 404


# ---------------------------------------------------------
# TEST API: Prets
# ---------------------------------------------------------

def test_create_pret():
    # Create client first
    res_client = client.post(
        "/clients/",
        json={
            "age": 27,
            "taille": 172.0,
            "poids": 65.0,
            "sport_licence": "oui",
            "smoker": "non",
            "niveau_etude": "master",
            "region": "Grand-Est",
            "situation_familiale": "célibataire",
            "historique_credits": 1.0,
            "risque_personnel": 0.2,
            "score_credit": 0.9,
            "date_creation_compte": "2023-10-01"
        }
    )
    client_id = res_client.json()["id"]

    res_pret = client.post(
        "/prets/",
        json={
            "client_id": client_id,
            "montant_pret": 15000.0,
            "revenu_estime_mois": 2000,
            "loyer_mensuel": 650.0,
            "score_credit": 0.9,
            "risque_personnel": 0.2
        }
    )

    assert res_pret.status_code == 200
    data = res_pret.json()
    assert data["client_id"] == client_id
    assert data["montant_pret"] == 15000.0


def test_get_prets_list():
    # Create a client
    res_client = client.post(
        "/clients/",
        json={
            "age": 28,
            "taille": 170.0,
            "poids": 60.0,
            "sport_licence": "non",
            "smoker": "non",
            "niveau_etude": "bac+3",
            "region": "Occitanie",
            "situation_familiale": "célibataire",
            "historique_credits": 0.4,
            "risque_personnel": 0.3,
            "score_credit": 0.85,
            "date_creation_compte": "2024-03-01"
        }
    )
    client_id = res_client.json()["id"]

    # Create a pret
    client.post(
        "/prets/",
        json={
            "client_id": client_id,
            "montant_pret": 5000.0,
            "revenu_estime_mois": 1800,
            "loyer_mensuel": 500,
            "score_credit": 0.85,
            "risque_personnel": 0.3
        }
    )

    response = client.get("/prets/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_pret():
    # Create client
    res_client = client.post(
        "/clients/",
        json={
            "age": 35,
            "taille": 185.0,
            "poids": 90.0,
            "sport_licence": "oui",
            "smoker": "non",
            "niveau_etude": "doctorat",
            "region": "Nouvelle-Aquitaine",
            "situation_familiale": "marié",
            "historique_credits": 3.0,
            "risque_personnel": 0.4,
            "score_credit": 0.8,
            "date_creation_compte": "2022-06-01"
        }
    )
    client_id = res_client.json()["id"]

    # Create pret
    res_pret = client.post(
        "/prets/",
        json={
            "client_id": client_id,
            "montant_pret": 25000.0,
            "revenu_estime_mois": 3000,
            "loyer_mensuel": 800,
            "score_credit": 0.8,
            "risque_personnel": 0.4
        }
    )
    pret_id = res_pret.json()["id"]

    # Delete
    del_res = client.delete(f"/prets/{pret_id}")
    assert del_res.status_code == 200

    # Ensure deleted
    get_res = client.get(f"/prets/{pret_id}")
    assert get_res.status_code == 404

# ---------------------------------------------------------
# TEST API: Training
# ---------------------------------------------------------

def test_train_route():
    """
    Teste la route /train pour vérifier :
    - le statut HTTP
    - le format de la réponse
    - que l'entraînement ne plante pas
    """

    response = client.post("/train/")
    assert response.status_code == 200, "La route /train doit répondre 200"

    data = response.json()

    # Vérifie la structure minimale attendue
    assert "status" in data
    assert data["status"] == "trained"

    # Le chemin du modèle entraîné doit apparaître
    assert "model_path" in data
    assert isinstance(data["model_path"], str)
    assert data["model_path"].endswith(".h5") or data["model_path"].endswith(".pkl")

    # Vérifie que MLflow a probablement loggé un run
    # (si tu veux rendre le test encore plus strict)
    assert "run_id" in data
    assert isinstance(data["run_id"], str)
