import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import scatter_matrix
from scipy.signal import dfreqresp
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
fname = "stats_3000_games.csv"
data = pd.read_csv(fname)

data['Winner'] = np.where(data['Winner'] == 'Team1', 1, 0)
data = data.drop(columns=['MatchID'])
data = data.drop(columns=['Elo'])

X = data.iloc[:, :-1]  # Targetvektor
Y = data.iloc[:, -1]  # Merkmalvektor Win

scaler = StandardScaler()
dataScaled = scaler.fit_transform(X)
data = pd.DataFrame(dataScaled, columns=X.columns)
data['Win'] = Y


def correlationMatrix(data):
    data = data.drop(columns=['Team1:MidLane', 'Team1:TopLane', 'Team1:Jungle', 'Team1:Support', 'Team1:AD Carry'])
    data = data.drop(columns=['Team2:MidLane', 'Team2:TopLane', 'Team2:Jungle', 'Team2:Support', 'Team2:AD Carry'])
    data = data.drop(columns=['Team1:AverageLevel', 'Team2:AverageLevel', 'Team1:DragonKills', 'Team2:DragonKills'])
    data = data.drop(columns=['Team1:ElderDragonKills', 'Team2:ElderDragonKills', 'Team1:InhibitorKills', 'Team2:InhibitorKills'])
    data = data.drop(columns=['Unnamed: 0'])
    corralationMatrix = data.corr()
    plt.figure(figsize=(12, 8))
    heatmap = sns.heatmap(corralationMatrix, annot=True, cmap='magma', fmt='.1f', linewidths=0)
    heatmap.set_xticklabels(data.columns, rotation=35)
    heatmap.set_yticklabels(data.columns, rotation=35)
    plt.show()


def scattermatrix(data):
    data = data.drop(columns=['Team1:MidLane', 'Team1:TopLane', 'Team1:Jungle', 'Team1:Support', 'Team1:AD Carry'])
    data = data.drop(columns=['Team2:MidLane', 'Team2:TopLane', 'Team2:Jungle', 'Team2:Support', 'Team2:AD Carry'])
    data = data.drop(columns=['Team1:AverageLevel', 'Team2:AverageLevel', 'Team1:DragonKills', 'Team2:DragonKills'])
    data = data.drop(
        columns=['Team1:ElderDragonKills', 'Team2:ElderDragonKills', 'Team1:InhibitorKills', 'Team2:InhibitorKills', 'Unnamed: 0'])
    scatterMatrix = scatter_matrix(data, figsize=(12, 12))
    for ax in scatterMatrix.ravel():
        ax.xaxis.label.set_rotation(0)
        ax.yaxis.label.set_rotation(45)
        ax.xaxis.label.set_size(10)
        ax.yaxis.label.set_size(10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.1, hspace=0.1)
    plt.show()


correlationMatrix(data)
scattermatrix(data)
