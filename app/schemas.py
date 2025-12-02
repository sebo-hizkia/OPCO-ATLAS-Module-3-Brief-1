from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

# =========================================================
#               Schema de contrôle pour Client
# =========================================================

class ClientBase(BaseModel):
    # nom: str
    # prenom: str
    age: int
    taille: float
    poids: float
    # sexe: str
    sport_licence: str
    smoker: str
    niveau_etude: str
    region: str
    # nationalite_francaise: str
    situation_familiale: Optional[str] = None
    historique_credits: Optional[float] = None
    risque_personnel: Optional[float] = None
    score_credit: Optional[float] = None
    date_creation_compte: Optional[date] = None

class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # permet à pydantic d’accepter les objets SQLAlchemy


# =========================================================
#                Schema de contrôle pour Pret
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
    model_config = ConfigDict(from_attributes=True)
