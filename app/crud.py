# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas


# =========================================================
#                      CLIENT CRUD
# =========================================================

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if client:
        db.delete(client)
        db.commit()
    return client


def update_client(db: Session, client_id: int, updated_client: schemas.ClientCreate):
    db_client = get_client(db, client_id)
    if not db_client:
        return None

    for field, value in updated_client.dict().items():
        setattr(db_client, field, value)

    db.commit()
    db.refresh(db_client)
    return db_client


# =========================================================
#                        PRET CRUD
# =========================================================

def get_prets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pret).offset(skip).limit(limit).all()


def get_pret(db: Session, pret_id: int):
    return db.query(models.Pret).filter(models.Pret.id == pret_id).first()


def create_pret(db: Session, pret: schemas.PretCreate):
    db_pret = models.Pret(**pret.dict())
    db.add(db_pret)
    db.commit()
    db.refresh(db_pret)
    return db_pret


def delete_pret(db: Session, pret_id: int):
    pret = get_pret(db, pret_id)
    if pret:
        db.delete(pret)
        db.commit()
    return pret


def update_pret(db: Session, pret_id: int, updated_pret: schemas.PretCreate):
    db_pret = get_pret(db, pret_id)
    if not db_pret:
        return None

    for field, value in updated_pret.dict().items():
        setattr(db_pret, field, value)

    db.commit()
    db.refresh(db_pret)
    return db_pret
