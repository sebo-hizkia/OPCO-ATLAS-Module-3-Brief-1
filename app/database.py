import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# CONFIG : connexion à PostgreSQL dans Docker
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

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
