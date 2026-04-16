import pandas as pd
import numpy as np
#read the csv file
df = pd.read_csv("stock_cleaned.csv")
# -----------------------------
# 1) Valeur du stock
# -----------------------------
df["Valeur_Stock"] = df["Quantite_Stock"] * df["Prix_Unitaire"]

# -----------------------------
# 2) Consommation annuelle (€)
# -----------------------------
df["Consommation_Annuelle_Valeur"] = df["Demande_Annuelle"] * df["Prix_Unitaire"]

# -----------------------------
# 3) Tri décroissant
# -----------------------------
df = df.sort_values(by="Consommation_Annuelle_Valeur", ascending=False)

# -----------------------------
# 4) Pourcentage cumulé
# -----------------------------
df["Pourcentage"] = df["Consommation_Annuelle_Valeur"] / df["Consommation_Annuelle_Valeur"].sum()
df["Pourcentage_Cumule"] = df["Pourcentage"].cumsum()

# -----------------------------
# 5) Classification ABC
# -----------------------------
def classify_abc(x):
    if x <= 0.80:
        return "A"
    elif x <= 0.95:
        return "B"
    else:
        return "C"

df["Classe_ABC"] = df["Pourcentage_Cumule"].apply(classify_abc)

# Vérification
print(df[["Produit", "Consommation_Annuelle_Valeur", "Classe_ABC"]].head(10))
# Distribution des classes
print(df["Classe_ABC"].value_counts())
# VOIR les produits de classe A
print(df[df["Classe_ABC"] == "A"].head())
# VOIR les produits de classe B
print(df[df["Classe_ABC"] == "B"].head())
# VOIR les produits de classe C
print(df[df["Classe_ABC"] == "C"].head())
# Distribution finale
print(df["Classe_ABC"].value_counts())

# -----------------------------
# 6) EOQ
# -----------------------------


df["EOQ"] = np.sqrt(
    (2 * df["Demande_Annuelle"] * df["Cout_Commande"]) / df["Cout_Stockage_Unitaire"]
)

# -----------------------------
# 7) Demande journalière
# -----------------------------
df["Demande_Journaliere"] = df["Demande_Annuelle"] / 365

# -----------------------------
# 8) Stock de sécurité
# -----------------------------
df["Stock_Securite"] = df["Demande_Journaliere"] * df["Lead_Time_Jours"] * 1.2

# -----------------------------
# 9) Point de commande
# -----------------------------
df["Point_Commande"] = (
    df["Demande_Journaliere"] * df["Lead_Time_Jours"]
) + df["Stock_Securite"]

# -----------------------------
# 10) Statut stock
# -----------------------------
def statut(row):
    if row["Quantite_Stock"] <= row["Point_Commande"]:
        return "A commander"
    elif row["Quantite_Stock"] <= row["Point_Commande"] * 1.2:
        return "Surveillance"
    else:
        return "OK"

df["Statut"] = df.apply(statut, axis=1)

# -----------------------------
# 11) Stratégie
# -----------------------------
def reco(row):
    if row["Classe_ABC"] == "A":
        return "Controle strict + commandes frequentes"
    elif row["Classe_ABC"] == "B":
        return "Controle normal"
    else:
        return "Commande en lot + faible priorite"

df["Strategie"] = df.apply(reco, axis=1)
# Enregistrer le résultat final
df.to_csv("inventory_analysis_final.csv", index=False)
# Aperçu final
print(df["Statut"].value_counts())
