# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# CONFIG : connexion à PostgreSQL dans Docker
# ---------------------------------------------------------

DATABASE_URL = "postgresql://fastia:fastiapwd@localhost:5436/fastia"
# IMPORTANT :
# - user : fastia
# - password : fastiapwd
# - host : localhost (car l'API n'est PAS dans Docker pour l'instant)
# - port : 5436 (car PostgreSQL locaux)
# - dbname : fastia


# ---------------------------------------------------------
# INITIALISATION SQLALCHEMY
# ---------------------------------------------------------

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ---------------------------------------------------------
# Dépendance FastAPI pour obtenir une session DB
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
