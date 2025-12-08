from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sqlalchemy.orm import Session
from app.models import Client, Pret
import pandas as pd

def split(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def load_training_dataframe(db: Session) -> pd.DataFrame:
    """
    Lit les données Client + Pret en base de données
    et retourne un DataFrame pandas.
    """
    # Jointure Client / Pret sur client_id
    rows = (
        db.query(Client, Pret)
        .join(Pret, Pret.client_id == Client.id)
        .all()
    )

    data = []
    for client, pret in rows:
        data.append(
            {
                # Cibles et features numériques
                "montant_pret": pret.montant_pret,
                "age": client.age,
                "taille": client.taille,
                "poids": client.poids,
                "historique_credits": client.historique_credits,
                "risque_personnel_client": client.risque_personnel,
                "score_credit_client": client.score_credit,
                "revenu_estime_mois": pret.revenu_estime_mois,
                "loyer_mensuel": pret.loyer_mensuel,
                "score_credit_pret": pret.score_credit,
                "risque_personnel_pret": pret.risque_personnel,

                # Catégorielles
                "sport_licence": client.sport_licence,
                "smoker": client.smoker,
                "niveau_etude": client.niveau_etude,
                "region": client.region,
                "situation_familiale": client.situation_familiale,
                "nb_enfants": client.nb_enfants,
                "quotient_caf": client.quotient_caf,
            }
        )

    df = pd.DataFrame(data)

    return df

def correct_business_rules(df):
    # nb_enfants ne peut pas être négatif
    if "nb_enfants" in df.columns:
        df["nb_enfants"] = df["nb_enfants"].clip(lower=0)

    # quotient_caf ne peut pas être négatif
    if "quotient_caf" in df.columns:
        df["quotient_caf"] = df["quotient_caf"].clip(lower=0)

    return df



def preprocessing(db: Session, target: str = "montant_pret"):
    """
    Fonction pour effectuer le prétraitement des données :
    - Nettoyage des NaN
    - Application des règles métier (nb_enfants >= 0, quotient_caf >= 0)
    - Traitement des outliers (IQR)
    - Imputation
    - Encodage catégoriel
    - Standardisation des variables numériques
    """

    df = load_training_dataframe(db)

    # -------------------------------
    # SUPPRESSION LIGNES SANS CIBLE
    # -------------------------------
    df = df.dropna(subset=[target])

    # y = variable à prédire
    y = df[target].astype(float).values

    # ---------------------------------------------------------
    # SUPPRESSION COLONNES TROP MANQUANTES (> 40 %)
    # ---------------------------------------------------------
    cols_before = df.shape[1]
    threshold = 0.40
    a_supprimer = list(df.columns[df.isna().mean() > threshold])
    df_clean = df.drop(columns=a_supprimer)
    cols_after = df_clean.shape[1]
    print(f"Nb colonnes avant nettoyage : {cols_before}, nb colonnes après : {cols_after}")

    # ---------------------------------------------------------
    # APPLICATION DES RÈGLES MÉTIER (TRAITEMENT MANQUANT)
    # ---------------------------------------------------------
    df_clean = correct_business_rules(df_clean)

    # ---------------------------------------------------------
    # DÉFINITION DES COLONNES NUMÉRIQUES & CATÉGORIELLES
    # ---------------------------------------------------------
    numeric_cols = [
        "age",
        "taille",
        "poids",
        "historique_credits",
        "risque_personnel_client",
        "score_credit_client",
        "revenu_estime_mois",
        "loyer_mensuel",
        "score_credit_pret",
        "risque_personnel_pret",
        "nb_enfants",
        "quotient_caf",
    ]

    categorical_cols = [
        "sport_licence",
        "smoker",
        "niveau_etude",
        "region",
        "situation_familiale",
    ]

    numeric_cols = [c for c in numeric_cols if c in df_clean.columns]
    categorical_cols = [c for c in categorical_cols if c in df_clean.columns]

    # ---------------------------------------------------------
    # TRAITEMENT DES OUTLIERS
    # ---------------------------------------------------------
    def treat_outliers_iqr(df, cols):
        df_out = df.copy()
        for col in cols:
            if df_out[col].dtype.kind not in "iuf":
                continue

            Q1 = df_out[col].quantile(0.25)
            Q3 = df_out[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            df_out[col] = df_out[col].clip(lower, upper)

        return df_out

    df_no_outliers = treat_outliers_iqr(df_clean, numeric_cols)

    # ---------------------------------------------------------
    # PIPELINES DE TRANSFORMATION
    # ---------------------------------------------------------
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, numeric_cols),
        ("cat", cat_pipeline, categorical_cols)
    ])

    # ---------------------------------------------------------
    # APPLICATION DU PREPROCESSING
    # ---------------------------------------------------------
    X = df_no_outliers.drop(columns=[target])
    X_processed = preprocessor.fit_transform(X)

    return X_processed, y, preprocessor





