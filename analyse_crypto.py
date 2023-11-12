import pandas as pd
import matplotlib.pyplot as plt

# Exemple de données (vous devrez récupérer des données réelles à partir d'une API ou d'une source de données)
data = {
    'Date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'],
    'Bitcoin': [30000, 31000, 29000, 32000],
    'Ethereum': [1500, 1600, 1400, 1700],
    'Litecoin': [120, 130, 110, 140]
}

# Création d'un DataFrame à partir des données
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Affichage des données
print(df)

# Visualisation des données
plt.figure(figsize=(10, 6))

for crypto in ['Bitcoin', 'Ethereum', 'Litecoin']:
    plt.plot(df['Date'], df[crypto], label=crypto)

plt.title('Analyse des Crypto-monnaies')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.legend()
plt.show()
