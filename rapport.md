# OPCO-ATLAS-Module-1-Brief-2 - Rapport de Synthèse – Nettoyage de Données Numériques (FastIA)
## Documentation Synthétique du Nettoyage & Analyse Éthique

### Objectif

Préparer deux jeux de données :

Dataset nettoyé (technique) : valeurs manquantes traitées, outliers supprimés, standardisation.

Dataset éthique : version nettoyée + suppression des attributs sensibles non conformes aux bonnes pratiques RGPD.

### Étapes principales du nettoyage
#### Valeurs manquantes

- Suppression des colonnes avec > 40 % de NA.
- Imputation médiane pour loyer_mensuel.
- Suppression des lignes restantes contenant des NA.

#### Outliers

- Détection IQR sur : age, taille, poids, revenu_estime_mois, montant_pret.
- Suppression des lignes contenant au moins un outlier.

#### Standardisation

StandardScaler appliqué sur toutes les colonnes numériques du dataset.

#### Décisions éthiques

Suppression des attributs sensibles ou identifiants directs :

- données personnelles (RGPD),
- informations sensibles (santé, nationalité),
- variables pouvant introduire des biais discriminatoires.

### Tableau récapitulatif des décisions par colonne

| Colonne                        | Type                    | Traitement technique                      | Décision éthique   | Raison / justification                                         |
|-------------------------------|--------------------------|--------------------------------------------|---------------------|----------------------------------------------------------------|
| nom                           | Identifiant              | Conservée techniquement                    | ❌ Supprimée        | Identifiant direct, inutile et contraire au RGPD              |
| prenom                        | Identifiant              | Conservée techniquement                    | ❌ Supprimée        | Identifiant direct, interdit pour la décision automatisée     |
| sexe                          | Catégorielle             | Non traitée                                 | ❌ Supprimée        | Donnée sensible, risque de discrimination                      |
| smoker                        | Catégorielle (santé)     | Non traitée                                 | ❌ Supprimée        | Donnée liée à la santé → protégée par RGPD                    |
| nationalité_francaise         | Catégorielle             | Non traitée                                 | ❌ Supprimée        | Origine nationale → discrimination potentielle                |
| situation_familiale           | Catégorielle             | ❌ Suppression (trop de NA)                 | ❌ Supprimée        | Incomplète + sensible (vie privée)                            |
| risque_personnel              | Score interne            | Conservée techniquement                    | ❌ Supprimée        | Variable potentiellement discriminante / biaisée              |
| age                           | Numérique                | Outliers filtrés + standardisation         | ✔️ Conservée        | Pertinent pour la solvabilité                                 |
| taille                        | Numérique                | Outliers filtrés + standardisation         | ✔️ Conservée        | Pas sensible, utile si corrélée à d'autres variables          |
| poids                         | Numérique                | Outliers filtrés + standardisation         | ✔️ Conservée        | Pas sensible (hors BMI santé), acceptable                     |
| revenu_estime_mois            | Numérique                | Outliers filtrés + standardisation         | ✔️ Conservée        | Variable clé pour décision de prêt                            |
| montant_pret                  | Numérique (cible?)       | Outliers filtrés + standardisation         | ✔️ Conservée        | Variable centrale du cas d’usage                              |
| loyer_mensuel                 | Numérique                | Imputation médiane + standardisation       | ✔️ Conservée        | Pertinent pour évaluer reste à vivre                          |
| Toutes autres colonnes numériques | Numérique            | Standardisation                            | ✔️ Conservées       | Aucune sensibilité                                   |

### Résultat final

dataset_standardized.csv → version nettoyée et normalisée.

dataset_ethic.csv → version éthique : colonnes sensibles supprimées.
