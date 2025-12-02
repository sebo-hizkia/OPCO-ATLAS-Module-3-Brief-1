from fastapi import FastAPI, HTTPException
from loguru import logger
from app.database import Base, engine
from app.models import Client, Pret

# Routers
from app.routers import clients, prets

# ---------------------------------------------------------
# Création des tables (si elles n'existent pas déjà)
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# Initialisation FastAPI
# ---------------------------------------------------------
app = FastAPI(
    title="FastIA - API Prêts",
    description="API exposant les données Client et Pret pour le projet OPCA Atlas Module 3.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Charge automatiquement les routes présentes dans app/routers
# ---------------------------------------------------------
app.include_router(clients.router)
app.include_router(prets.router)

# ---------------------------------------------------------
# Route de vérification
# ---------------------------------------------------------
@app.get("/health", tags=["system"])
async def health():
    """
    Retourne l'état de santé de l'API
    """
    try:
        logger.info(f"healthcheck")

        return {"status": "OK", "database": "connected"}


    except Exception as e:
        logger.error(f"Erreur healthcheck : {e}")
        raise HTTPException(status_code=500, detail="API non fonctionnelle")
