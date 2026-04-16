import pandas as pd
#read the csv file
df = pd.read_csv("stock_dataset_dirty_212_rows.csv")
# -----------------------------
# 1) Supprimer colonnes inutiles
# -----------------------------
df = df.drop(columns=["Unnamed: 10", "Unnamed: 11", "Unnamed: 12"])

# -----------------------------
# 2) Supprimer doublons complets
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# 3) Supprimer doublons Product_ID (garder 1er)
# -----------------------------
df = df.drop_duplicates(subset=["Product_ID"])

# -----------------------------
# 4) Corriger stock négatif
# -----------------------------
df["Quantite_Stock"] = df["Quantite_Stock"].apply(lambda x: max(x, 0))

# -----------------------------
# 5) Remplacer prix = 0 par NaN
# -----------------------------
import numpy as np
df["Prix_Unitaire"] = df["Prix_Unitaire"].replace(0, np.nan)

# -----------------------------
# 6) Remplir valeurs manquantes
# -----------------------------

# Categorie → mode
df["Categorie"].fillna(df["Categorie"].mode()[0], inplace=True)

# Fournisseur → mode
df["Fournisseur"].fillna(df["Fournisseur"].mode()[0], inplace=True)

# Numériques → moyenne
df["Prix_Unitaire"].fillna(df["Prix_Unitaire"].mean(), inplace=True)
df["Demande_Annuelle"].fillna(df["Demande_Annuelle"].mean(), inplace=True)
df["Cout_Stockage_Unitaire"].fillna(df["Cout_Stockage_Unitaire"].mean(), inplace=True)
df["Lead_Time_Jours"].fillna(df["Lead_Time_Jours"].mean(), inplace=True)

# -----------------------------
# 7) Vérification finale
# -----------------------------
print("Dimensions finales :", df.shape)
print("\nNulls restants :")
print(df.isnull().sum())
# Enregistrer le dataset nettoyé
df.to_csv("stock_cleaned.csv", index=False)