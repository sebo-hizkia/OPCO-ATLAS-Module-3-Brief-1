import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Client, Pret
from datetime import datetime

CSV_PATH = "data/data.csv"


def convert_comma_float(x):
    """Convertit '62,5' -> 62.5, retourne None si vide."""
    if pd.isna(x):
        return None
    if isinstance(x, str):
        return float(x.replace(",", "."))
    return float(x)


def import_csv():
    print("Lecture du CSV : {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    db: Session = SessionLocal()

    for idx, row in df.iterrows():
        print(f" => Import ligne {idx+1}/{len(df)} : {row['nom']}")

        # ---------------------------
        # Création du Client
        # ---------------------------
        client = Client(
            # Pas d'import des données protégées par la RGPD
            # nom=row["nom"],
            # prenom=row["prenom"],
            age=int(row["age"]),

            # valeurs string comme dans CSV
            taille=convert_comma_float(row["taille"]),
            poids=convert_comma_float(row["poids"]),
            # sexe=row["sexe"], # Ecartée pour des raisons éthiques
            sport_licence=row["sport_licence"],
            smoker=row["smoker"],
            niveau_etude=row["niveau_etude"],
            region=row["region"],

            # Ecartée pour des raisons éthiques
            # nationalite_francaise=row["nationalité_francaise"],

            situation_familiale=row.get("situation_familiale"),

            historique_credits=convert_comma_float(row["historique_credits"]),
            risque_personnel=convert_comma_float(row["risque_personnel"]),
            score_credit=convert_comma_float(row["score_credit"]),

            date_creation_compte=(
                None if pd.isna(row["date_creation_compte"])
                else datetime.strptime(row["date_creation_compte"], "%Y-%m-%d").date()
            ),
        )

        db.add(client)
        db.commit()
        db.refresh(client)  # récupère l'id généré pour le Pret

        # ---------------------------
        # Création du Pret
        # ---------------------------
        pret = Pret(
            client_id=client.id,
            montant_pret=convert_comma_float(row["montant_pret"]),
            revenu_estime_mois=int(row["revenu_estime_mois"]),
            loyer_mensuel=convert_comma_float(row["loyer_mensuel"]),
            score_credit=convert_comma_float(row["score_credit"]),
            risque_personnel=convert_comma_float(row["risque_personnel"]),
        )

        db.add(pret)
        db.commit()

    db.close()
    print("Import terminé avec succès !")


if __name__ == "__main__":
    import_csv()
