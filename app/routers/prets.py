# app/routers/prets.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/prets",
    tags=["Prets"]
)


# ---------------------------------------------------------
# GET /prets
# ---------------------------------------------------------
@router.get("/", response_model=list[schemas.Pret])
def read_prets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prets = crud.get_prets(db, skip=skip, limit=limit)
    return prets


# ---------------------------------------------------------
# GET /prets/{pret_id}
# ---------------------------------------------------------
@router.get("/{pret_id}", response_model=schemas.Pret)
def read_pret(pret_id: int, db: Session = Depends(get_db)):
    pret = crud.get_pret(db, pret_id)
    if not pret:
        raise HTTPException(status_code=404, detail="Pret not found")
    return pret


# ---------------------------------------------------------
# POST /prets
# ---------------------------------------------------------
@router.post("/", response_model=schemas.Pret)
def create_pret(pret: schemas.PretCreate, db: Session = Depends(get_db)):
    # Vérifier que le client existe
    client = crud.get_client(db, pret.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return crud.create_pret(db, pret)


# ---------------------------------------------------------
# DELETE /prets/{pret_id}
# ---------------------------------------------------------
@router.delete("/{pret_id}", response_model=schemas.Pret)
def delete_pret(pret_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_pret(db, pret_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pret not found")
    return deleted


# ---------------------------------------------------------
# PUT /prets/{pret_id}
# ---------------------------------------------------------
@router.put("/{pret_id}", response_model=schemas.Pret)
def update_pret(pret_id: int, pret: schemas.PretCreate, db: Session = Depends(get_db)):
    updated = crud.update_pret(db, pret_id, pret)
    if not updated:
        raise HTTPException(status_code=404, detail="Pret not found")
    return updated
