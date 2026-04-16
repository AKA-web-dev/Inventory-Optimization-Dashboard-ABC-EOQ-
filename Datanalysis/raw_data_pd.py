import pandas as pd
#read the csv file
df = pd.read_csv("stock_dataset_dirty_212_rows.csv")
# Aperçu général
print("Dimensions :", df.shape)
print("\nColonnes :")
print(df.columns)

print("\nTypes de données :")
print(df.dtypes)

print("\n5 premières lignes :")
print(df.head())
# Valeurs manquantes
print("\nValeurs manquantes par colonne :")
print(df.isnull().sum())

# Doublons complets
print("\nNombre de doublons complets :", df.duplicated().sum())

# Doublons sur Product_ID
print("\nNombre de doublons sur Product_ID :", df.duplicated(subset=["Product_ID"]).sum())

# Stocks négatifs
print("\nLignes avec stock négatif :")
print(df[df["Quantite_Stock"] < 0])

# Prix unitaire égal à 0
print("\nLignes avec prix unitaire = 0 :")
print(df[df["Prix_Unitaire"] == 0])