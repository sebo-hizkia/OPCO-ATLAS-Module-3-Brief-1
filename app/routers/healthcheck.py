from fastapi import APIRouter, Depends, HTTPException
from app.config import app_logger

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

# ---------------------------------------------------------
# Route de vérification
# ---------------------------------------------------------
@router.get("/", tags=["system"])
async def health():
    """
    Retourne l'état de santé de l'API
    """
    try:
        app_logger.info(f"healthcheck")

        return {"status": "OK", "database": "connected"}


    except Exception as e:
        app_logger.error(f"Erreur healthcheck : {e}")
        raise HTTPException(status_code=500, detail="API non fonctionnelle")
