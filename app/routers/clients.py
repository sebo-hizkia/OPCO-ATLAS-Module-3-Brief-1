# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException
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
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients


# ---------------------------------------------------------
# GET /clients/{client_id}
# ---------------------------------------------------------
@router.get("/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# ---------------------------------------------------------
# POST /clients
# ---------------------------------------------------------
@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)


# ---------------------------------------------------------
# DELETE /clients/{client_id}
# ---------------------------------------------------------
@router.delete("/{client_id}", response_model=schemas.Client)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return deleted


# ---------------------------------------------------------
# PUT /clients/{client_id}
# ---------------------------------------------------------
@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    updated = crud.update_client(db, client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated
