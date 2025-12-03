from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import time
from app.config import app_logger

import mlflow
import mlflow.sklearn

from app.models_ia import create_nn_model, train_model, model_predict
from app.modules.preprocess import preprocessing, split
from app.modules.evaluate import evaluate_performance


router = APIRouter(
    prefix="/train",
    tags=["IA / Entraînement"]
)

# ---------------------------------------------------------
# ROUTE D'ENTRAÎNEMENT DU MODÈLE IA
# ---------------------------------------------------------

@router.post("/")
def train(db: Session = Depends(get_db)):
    """
    Lance un entraînement du modèle IA
    (placeholder — à remplacer par ton vrai code IA)
    """

    try:

        with mlflow.start_run():

            # Message de début
            app_logger.info(f"Training model")
            start = time.time()

            # preprocesser les data
            X, y, _ = preprocessing(db)


            # split data in train and test dataset
            X_train, X_test, y_train, y_test = split(X, y)

            # # create a new model
            model = create_nn_model(X_train.shape[1])

            # # entraîner le modèle
            model, hist = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test)
            #draw_loss(hist)

            duration = round(time.time() - start, 2)

            #%% predire sur les valeurs de train
            y_pred = model_predict(model, X_train)

            # mesurer les performances MSE, MAE et R²
            perf = evaluate_performance(y_train, y_pred)

            # Logging MLflow
            mlflow.log_metric("MSE", perf["MSE"])
            mlflow.log_metric("MAE", perf["MAE"])
            mlflow.log_metric("R²", perf["R²"])
            mlflow.sklearn.log_model(model, "new_model")

            # Résultat
            return {
                "status": "training completed",
                "training_time_seconds": duration,
                "message": "Modèle entraîné avec succès"
            }

    except Exception as e:
        app_logger.error(f"Erreur à l'entraînement : {e}")
        raise HTTPException(status_code=500, detail=str(e))
