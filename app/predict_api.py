from fastapi import FastAPI, HTTPException
from loguru import logger
from app.database import Base, engine
from app.models import Client, Pret
from app.schemas import ClientBase, PretBase

# Routers
from app.routers import clients, prets, train, healthcheck

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
app.include_router(train.router)
app.include_router(healthcheck.router)



