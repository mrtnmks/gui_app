import pandas as pd
import numpy as np

# Vytvoření testovacích dat s 15 kategoriemi (místo 10)
np.random.seed(42)
n_respondents = 100

# 15 kategorií
categories = [f'kategorie_{i:02d}' for i in range(1, 16)]

# Vytvoření různých typů respondentů
data = []
for i in range(n_respondents):
    respondent = {}
    respondent['id'] = i + 1
    
    if i < 25:  # Typ A - vysoké hodnoty v kategoriích 1-5
        for j, cat in enumerate(categories):
            if j < 5:
                respondent[cat] = np.random.uniform(0.6, 1.0)
            else:
                respondent[cat] = np.random.uniform(0.0, 0.3)
    elif i < 50:  # Typ B - vysoké hodnoty v kategoriích 6-10  
        for j, cat in enumerate(categories):
            if 5 <= j < 10:
                respondent[cat] = np.random.uniform(0.6, 1.0)
            else:
                respondent[cat] = np.random.uniform(0.0, 0.3)
    elif i < 75:  # Typ C - vysoké hodnoty v kategoriích 11-15
        for j, cat in enumerate(categories):
            if j >= 10:
                respondent[cat] = np.random.uniform(0.6, 1.0)
            else:
                respondent[cat] = np.random.uniform(0.0, 0.3)
    else:  # Typ D - smíšené hodnoty
        for j, cat in enumerate(categories):
            respondent[cat] = np.random.uniform(0.2, 0.8)
    
    data.append(respondent)

# Vytvoření DataFrame
df = pd.DataFrame(data)

# Uložení do CSV
df.to_csv('test_data_15_kategorii.csv', index=False)

print("Testovací soubor vytvořen!")
print(f"Počet respondentů: {len(df)}")
print(f"Počet kategorií: {len(categories)}")
print(f"Sloupce: {list(df.columns)}")
print("\nPrvních 5 řádků:")
print(df.head())
