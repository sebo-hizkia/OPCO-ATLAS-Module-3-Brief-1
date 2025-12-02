import pytest
from fastapi.testclient import TestClient
from predict_api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_predict():
    payload = {
        "nom": "Dupond",
        "prenom": "Toto",
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
