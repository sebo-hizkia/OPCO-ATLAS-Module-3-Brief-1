from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import mlflow
import mlflow.sklearn

from app.database import get_db
from app.config import app_logger
from app.modules.preprocess import preprocessing, split
from app.models_ia import adapt_model_input, train_model, model_predict
from app.modules.evaluate import evaluate_performance
from app.modules.draw import draw_loss

import joblib
import matplotlib.pyplot as plt

router = APIRouter(
    prefix="/retrain",
    tags=["IA / Ré-entraînement"]
)

@router.post("/")
def retrain(db: Session = Depends(get_db)):
    """
    Ré-entraînement du modèle avec nouvelles features
    (nb_enfants, quotient_caf) sans perdre les poids existants
    """

    try:
        with mlflow.start_run():

            app_logger.info("Re-training model with extended inputs")
            start = time.time()

            # ----------------------------
            # 1. Charger les nouvelles données
            # ----------------------------
            X, y, preprocessor = preprocessing(db)
            X_train, X_test, y_train, y_test = split(X, y)

            # ----------------------------
            # 2. Charger ancien modèle
            # ----------------------------
            old_model = mlflow.sklearn.load_model(
                "models:/model1/Production"
            )

            old_input_dim = old_model.input_shape[1]
            new_input_dim = X_train.shape[1]

            app_logger.info(
                f"Old input dim: {old_input_dim} | New input dim: {new_input_dim}"
            )

            # ----------------------------
            # 3. Adapter la couche d'entrée
            # ----------------------------
            new_model = adapt_model_input(old_model, new_input_dim)

            # ----------------------------
            # 4. Ré-entraîner
            # ----------------------------
            new_model, history = train_model(
                new_model,
                X_train,
                y_train,
                X_val=X_test,
                y_val=y_test
            )

            duration = round(time.time() - start, 2)

            # ----------------------------
            # 5. Évaluation
            # ----------------------------
            y_pred = model_predict(new_model, X_test)
            perf = evaluate_performance(y_test, y_pred)

            fig = draw_loss(history)

            # ----------------------------
            # 6. MLflow logging
            # ----------------------------
            mlflow.log_metric("MSE", perf["MSE"])
            mlflow.log_metric("MAE", perf["MAE"])
            mlflow.log_metric("R2", perf["R²"])
            mlflow.log_param("added_features", "nb_enfants, quotient_caf")

            joblib.dump(preprocessor, "models/preprocessor_v2.pkl")
            mlflow.log_artifact("models/preprocessor_v2.pkl")

            mlflow.sklearn.log_model(new_model, "model_v2")
            mlflow.log_figure(fig, "loss_retrain.png")

            plt.close(fig)

            return {
                "status": "retraining completed",
                "training_time_seconds": duration,
                "new_features": ["nb_enfants", "quotient_caf"]
            }

    except Exception as e:
        app_logger.error(f"Erreur ré-entraînement : {e}")
        raise HTTPException(status_code=500, detail=str(e))
