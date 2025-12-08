# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

# ---------------------------------------------------------
# GET /clients
# ---------------------------------------------------------
@router.get("/", response_model=list[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        clients = crud.get_clients(db, skip=skip, limit=limit)
        return clients
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des clients : {str(e)}"
        )

# ---------------------------------------------------------
# GET /clients/{client_id}
# ---------------------------------------------------------
@router.get("/{client_id}", response_model=schemas.Client)
def read_client(
    client_id: int = Path(..., gt=0, description="ID du client à récupérer"),
    db: Session = Depends(get_db)
):
    try:
        client = crud.get_client(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client introuvable")
        return client

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du client : {str(e)}"
        )

# ---------------------------------------------------------
# POST /clients
# ---------------------------------------------------------
@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_client(db, client)
        if not created:
            raise HTTPException(status_code=400, detail="Création du client impossible")
        return created

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création du client : {str(e)}"
        )

# ---------------------------------------------------------
# DELETE /clients/{client_id}
# ---------------------------------------------------------
@router.delete("/{client_id}", response_model=schemas.Client)
def delete_client(
    client_id: int = Path(..., gt=0, description="ID du client à supprimer"),
    db: Session = Depends(get_db)
):
    try:
        deleted = crud.delete_client(db, client_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Client introuvable")

        return deleted

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression du client : {str(e)}"
        )

# ---------------------------------------------------------
# PUT /clients/{client_id}
# ---------------------------------------------------------
@router.put("/{client_id}", response_model=schemas.Client)
def update_client(
    client_id: int = Path(..., gt=0, description="ID du client à mettre à jour"),
    client: schemas.ClientCreate = None,
    db: Session = Depends(get_db)
):
    if client is None:
        raise HTTPException(status_code=400, detail="Aucune donnée fournie pour la mise à jour.")

    try:
        updated = crud.update_client(db, client_id, client)
        if not updated:
            raise HTTPException(status_code=404, detail="Client introuvable")

        return updated

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la mise à jour du client : {str(e)}"
        )
