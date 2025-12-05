from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    ForeignKey, Date
)
from sqlalchemy.orm import relationship
from .database import Base


# =========================================================
#              Client (mapping table : clients)
# =========================================================
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    # Identité (encadré par la RGPD) : ne doit pas être stockée/utilisée pour la génération de modèle IA
    # nom = Column(String, index=True)
    # prenom = Column(String, index=True)
    age = Column(Integer)

    # Données physiques
    taille = Column(Float)
    poids = Column(Float)

    # Le sexe est une données discriminatoire pour l'application
    # sexe = Column(String(1))

    # Profil / Habitudes
    sport_licence = Column(String(3))        # oui / non
    smoker = Column(String(3))               # oui / non

    # Éducation / Région
    niveau_etude = Column(String(50))
    region = Column(String(100))

    # Nationalité est une données discriminatoire pour l'application
    # nationalite_francaise = Column(String(3))  # oui / non

    # Situation sociale
    situation_familiale = Column(String(50), nullable=True)

    # Historique & scores généraux
    historique_credits = Column(Float, nullable=True)
    risque_personnel = Column(Float, nullable=True)
    score_credit = Column(Float, nullable=True)

    # Comptes & dates
    date_creation_compte = Column(Date, nullable=True)

    # Relation 1:N -> un client peut avoir plusieurs prêts
    prets = relationship("Pret", back_populates="client", cascade="all, delete-orphan")

    # Nouveaux champs introduits dans le brief 2
    nb_enfants = Column(Integer, nullable=True)
    quotient_caf = Column(Float, nullable=True)


# =========================================================
#                 Pret (mapping table : prets)
# =========================================================
class Pret(Base):
    __tablename__ = "prets"

    id = Column(Integer, primary_key=True, index=True)

    # Relation vers Client
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))

    # Données financières du prêt
    montant_pret = Column(Float)
    revenu_estime_mois = Column(Integer)      # revenu au moment de la demande
    loyer_mensuel = Column(Float, nullable=True) # loyer au moment de la demande

    # Scores financiers du moment
    score_credit = Column(Float, nullable=True)
    risque_personnel = Column(Float, nullable=True)

    # Relation SQLAlchemy
    client = relationship("Client", back_populates="prets")
