from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
import time

from app.config import app_logger
from app.schemas import ClientInput
from app.modules.preprocess import preprocessing
import joblib
import pandas as pd

import mlflow
import mlflow.sklearn

# Charger le preprocessor
preprocessor_loaded = joblib.load("models/preprocessor.pkl")

router = APIRouter(
    prefix="/predict",
    tags=["IA / Prédiction"]
)

# ---------------------------------------------------------
# ROUTE PREDICTION DU PRET
# ---------------------------------------------------------

@router.post("/")
def predict(input_data: ClientInput):
    """
    Lance la prédiction du montant de prêt
    """
    try:
        app_logger.info(f"Requête reçue : {input_data}")

        # Convertir DataFrame pour preprocessing
        df = pd.DataFrame([input_data.model_dump()])

        X_processed = preprocessor_loaded.transform(df)

        # Charger le dernier modèle entraîné depuis MLFlow
        run_id = mlflow.search_runs(order_by=["attributes.start_time DESC"]).iloc[0]["run_id"]
        model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

        y_pred = model_predict(model, X_processed)

        app_logger.info(f"Prédiction : {y_pred}")

        return {"montant_pret": float(y_pred[0])}

    except Exception as e:
        app_logger.error(f"Erreur d'analyse : {e}")
        raise HTTPException(status_code=500, detail=str(e))
