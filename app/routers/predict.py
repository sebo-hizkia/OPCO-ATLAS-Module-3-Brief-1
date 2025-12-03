from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
import time

from app.config import app_logger

router = APIRouter(
    prefix="/predict",
    tags=["IA / Prédiction"]
)

# ---------------------------------------------------------
# ROUTE PREDICTION DU PRET
# ---------------------------------------------------------

@router.post("/")
def model_predict(input_data: ClientInput):
    """
    Lance un entraînement du modèle IA
    (placeholder — à remplacer par ton vrai code IA)
    """
    try:
        logger.info(f"Requête reçue : {input_data}")

        # Convertir DataFrame pour preprocessing
        df = pd.DataFrame([input_data.model_dump()])

        X_processed = preprocessor_loaded.transform(df)

        y_pred = model_predict(model, X_processed)

        logger.info(f"Prédiction : {y_pred}")

        return {"montant_pret": float(y_pred[0])}

    except Exception as e:
        logger.error(f"Erreur d'analyse : {e}")
        raise HTTPException(status_code=500, detail=str(e))
