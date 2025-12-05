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
            }
        )

    df = pd.DataFrame(data)

    return df


def preprocessing(db: Session, target: str = "montant_pret"):
    """
    Fonction pour effectuer le prétraitement des données :
    - Imputation des valeurs manquantes.
    - Standardisation des variables numériques.
    - Encodage des variables catégorielles.
    """

    df = load_training_dataframe(db)

    # On supprime les lignes où la cible est manquante
    df = df.dropna(subset=[target])

    # y = variable à prédire
    y = df[target].astype(float).values

    # Suppression les colonnes avec trop de données manquantes ( > 40%)
    cols_before = df.shape[1]
    threshold = 0.40  # 40%
    a_supprimer = list(df.columns[df.isna().mean() > threshold])
    df_clean = df.drop(columns=a_supprimer)
    cols_after = df_clean.shape[1]
    print(f"Nb colonnes avant nettoyage : {cols_before}, nb colonnes après : {cols_after}")

    # Colonnes numériques / catégorielles
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
    ]

    categorical_cols = [
        "sport_licence",
        "smoker",
        "niveau_etude",
        "region",
        "situation_familiale",
    ]

    # On garde seulement celles qui existent réellement (au cas où)
    numeric_cols = [c for c in numeric_cols if c in df_clean.columns]
    categorical_cols = [c for c in categorical_cols if c in df_clean.columns]

    # ------------------------------------
    # TRAITEMENT DES OUTLIERS (IQR method)
    # ------------------------------------
    def treat_outliers_iqr(df, cols):
        df_out = df.copy()
        for col in cols:
            if df_out[col].dtype.kind not in "iuf":  # int/float
                continue

            Q1 = df_out[col].quantile(0.25)
            Q3 = df_out[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            # On tronque les valeurs hors limites
            df_out[col] = df_out[col].clip(lower, upper)

        return df_out

    df_no_outliers = treat_outliers_iqr(df_clean, numeric_cols)

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

    X = df_no_outliers.drop(columns=[target])
    X_processed = preprocessor.fit_transform(X)

    return X_processed, y, preprocessor





