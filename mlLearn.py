import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt

# Daten einlesen
df = pd.read_csv('stats_3000_games.csv')
# print(df.describe())
# print(df.columns.tolist())

# Diferenz der Features berechnen
transformedData = pd.DataFrame()
transformedData['Minute'] = df['Minute']
transformedData['Top'] = df['Team1:TopLane'] - df['Team2:TopLane']
transformedData['Mid'] = df['Team1:MidLane'] - df['Team2:MidLane']
transformedData['Jungle'] = df['Team1:Jungle'] - df['Team2:Jungle']
transformedData['ADC'] = df['Team1:AD Carry'] - df['Team2:AD Carry']
transformedData['Support'] = df['Team1:Support'] - df['Team2:Support']
transformedData['PlayerKills'] = df['Team1:Kills'] - df['Team2:Kills']
transformedData['TurretKills'] = df['Team1:TurretKills'] - df['Team2:TurretKills']
transformedData['InhibitorKills'] = df['Team1:InhibitorKills'] - df['Team2:InhibitorKills']
transformedData['DragonKills'] = df['Team1:DragonKills'] - df['Team2:DragonKills']
transformedData['ElderDragonKills'] = df['Team1:ElderDragonKills'] - df['Team2:ElderDragonKills']
transformedData['BaronKills'] = df['Team1:BaronKills'] - df['Team2:BaronKills']
transformedData['Level'] = df['Team1:AverageLevel'] - df['Team2:AverageLevel']
transformedData['Win'] = np.where(df['Winner'] == 'Team1', 1, 0)

# Features und Zielvariable filtern 
X = transformedData[['Minute', 'Top', 'Mid', 'Jungle', 'ADC', 'Support', 'PlayerKills', 'TurretKills', 'InhibitorKills', 'DragonKills', 'ElderDragonKills', 'BaronKills', 'Level']]
y = transformedData['Win']

# Skalierung der Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aufteilung in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Training 
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(2,2), random_state=1, max_iter=5000)
clf.fit(X_train, y_train)

# Vorhersagen und Evaluation
y_pred = clf.predict(X_test)
y_pred_proba = clf.predict_proba(X_test)[:,1]

accuracy = accuracy_score(y_test, y_pred)
print("Genauigkeit auf dem Testset: " + str(accuracy))








# Berechnen einer konkreten Warscheinlichkeit
new_data = pd.read_csv("finalgame.csv")

# berechne golddif für jede minute 
new_data['Diff_Gold'] = new_data['Team1:Gold'] - new_data['Team2:Gold']

# Plot der Gold-Differenz
plt.plot(new_data['Minute'], new_data['Diff_Gold'])
plt.axhline(y=0, color='r', linestyle='-')
plt.fill_between(new_data['Minute'], new_data['Diff_Gold'], 0, 
                 where=new_data['Diff_Gold'] >= 0, 
                 facecolor='blue', alpha=0.5, interpolate=True)
plt.fill_between(new_data['Minute'], new_data['Diff_Gold'], 0, 
                 where=new_data['Diff_Gold'] < 0, 
                 facecolor='red', alpha=0.5, interpolate=True)
plt.xlabel('Minute')
plt.ylabel('Gold Difference')
plt.show()


transformedTest = pd.DataFrame()
transformedTest['Minute'] = new_data['Minute']
transformedTest['Top'] = new_data['Team1:TopLane'] - new_data['Team2:TopLane']
transformedTest['Mid'] = new_data['Team1:MidLane'] - new_data['Team2:MidLane']
transformedTest['Jungle'] = new_data['Team1:Jungle'] - new_data['Team2:Jungle']
transformedTest['ADC'] = new_data['Team1:AD Carry'] - new_data['Team2:AD Carry']
transformedTest['Support'] = new_data['Team1:Support'] - new_data['Team2:Support']
transformedTest['PlayerKills'] = new_data['Team1:Kills'] - new_data['Team2:Kills']
transformedTest['TurretKills'] = new_data['Team1:TurretsKills'] - new_data['Team2:TurretsKills']
transformedTest['InhibitorKills'] = new_data['Team1:InhibitorsKills'] - new_data['Team2:InhibitorsKills']
transformedTest['DragonKills'] = new_data['Team1:DragonKills'] - new_data['Team2:DragonKills']
transformedTest['ElderDragonKills'] = new_data['Team1:ElderDragonKills'] - new_data['Team2:ElderDragonKills']
transformedTest['BaronKills'] = new_data['Team1:BaronKills'] - new_data['Team2:BaronKills']
transformedTest['Level'] = new_data['Team1:AverageLevel'] - new_data['Team2:AverageLevel']

X_new = transformedTest[['Minute', 'Top', 'Mid', 'Jungle', 'ADC', 'Support', 
                        'PlayerKills', 'TurretKills', 'InhibitorKills', 
                        'DragonKills', 'ElderDragonKills', 'BaronKills', 'Level']]

X_new_scaled = scaler.transform(X_new)

new_prob = clf.predict_proba(X_new_scaled)[:,1]

new_data['Team1_win_probability'] = new_prob

# plotten der Wahrscheinlichkeiten
plt.plot(new_data['Minute'], new_data['Team1_win_probability'])
plt.xlabel('Minute')
plt.ylabel('Team1 Win Probability')
plt.show()