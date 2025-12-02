# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# =========================================================
#                      CLIENT SCHEMAS
# =========================================================

class ClientBase(BaseModel):
    nom: str
    prenom: str
    age: int
    taille: str
    poids: str
    sexe: str
    sport_licence: str
    smoker: str
    niveau_etude: str
    region: str
    nationalite_francaise: str
    situation_familiale: Optional[str] = None
    historique_credits: Optional[float] = None
    risque_personnel: Optional[float] = None
    score_credit: Optional[float] = None
    date_creation_compte: Optional[date] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


# =========================================================
#                      PRET SCHEMAS
# =========================================================

class PretBase(BaseModel):
    montant_pret: float
    revenu_estime_mois: int
    loyer_mensuel: Optional[float] = None
    score_credit: Optional[float] = None
    risque_personnel: Optional[float] = None


class PretCreate(PretBase):
    client_id: int  # Relation obligatoire


class Pret(PretBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True
