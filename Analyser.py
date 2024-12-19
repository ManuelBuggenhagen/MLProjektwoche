import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
fname = "stats_3000_games.csv"
data = pd.read_csv(fname)

transformedData = pd.DataFrame()
transformedData['Minute'] = data['Minute']
transformedData['Top'] = data['Team1:TopLane'] - data['Team2:TopLane']
transformedData['Mid'] = data['Team1:MidLane'] - data['Team2:MidLane']
transformedData['Jungle'] = data['Team1:Jungle'] - data['Team2:Jungle']
transformedData['ADC'] = data['Team1:AD Carry'] - data['Team2:AD Carry']
transformedData['Support'] = data['Team1:Support'] - data['Team2:Support']
transformedData['PlayerKills'] = data['Team1:Kills'] - data['Team2:Kills']
transformedData['TurretKills'] = data['Team1:TurretKills'] - data['Team2:TurretKills']
transformedData['InhibitorKills'] = data['Team1:InhibitorKills'] - data['Team2:InhibitorKills']
transformedData['DragonKills'] = data['Team1:DragonKills'] - data['Team2:DragonKills']
transformedData['ElderDragonKills'] = data['Team1:ElderDragonKills'] - data['Team2:ElderDragonKills']
transformedData['BaronKills'] = data['Team1:BaronKills'] - data['Team2:BaronKills']
transformedData['Level'] = data['Team1:AverageLevel'] - data['Team2:AverageLevel']
transformedData['Win'] = np.where(data['Winner'] == 'Team1', 1, 0)
# transformedData= transformedData.set_index('Minute')

# print("Team 1 Perspective:")
# print(transformedData.head(33))

# testOneGame = transformedData.head(33)
# print(testOneGame)

# Normalisieren der Daten
X = transformedData.iloc[:, :-1]  # Targetvektor
Y = transformedData[['Win']].values  # Merkmalvektor
Y = Y.ravel()

scalerX = StandardScaler()
X = scalerX.fit_transform(X)

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)

# Trainieren des Modells
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1, max_iter=2000)
clf.fit(X_train, Y_train)

prediction = clf.predict(X_test)
print(prediction)
print()
print(Y_test)

acc_score = round(accuracy_score(Y_test, prediction), 2)
print('Accuracy:', acc_score)

