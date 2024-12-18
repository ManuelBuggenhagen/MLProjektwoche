import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import scatter_matrix
from scipy.signal import dfreqresp
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
fname = "stats_300_games.csv"
data = pd.read_csv(fname)


def getGameDetails(dataframe, matchID):
    df = dataframe[dataframe['MatchID'] == matchID]
    df = df.set_index("Minute")
    df = df.drop(columns=['Unnamed: 0'])
    return df


def makeTablePNG(data):
    fig, ax = plt.subplots(figsize=(42, 8))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data.values,
                     colLabels=data.columns,
                     loc='center',
                     cellLoc='center',
                     colColours=['#f2f2f2'] * len(data.columns))

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(data.columns))))
    # plt.show()
    plt.savefig("table_output.png", bbox_inches='tight')
    plt.close()


def getALlGamesFromOneElo(originalData, elo):
    df = originalData[originalData['Elo'] == elo]
    df = df.drop(columns=['Elo'])
    df = df.drop(columns=['MatchID'])
    df['Winner'] = np.where(df['Winner'] == 'Team1', 0, 1)
    return df


def correlationMatrix(data):
    data = data.drop(columns=['Team1:MidLane','Team1:TopLane','Team1:Jungle','Team1:Support','Team1:AD Carry'])
    data = data.drop(columns=['Team2:MidLane', 'Team2:TopLane', 'Team2:Jungle', 'Team2:Support', 'Team2:AD Carry'])
    data = data.drop(columns=['Team1:AverageLevel', 'Team2:AverageLevel', 'Team1:DragonKills', 'Team2:DragonKills'])
    data = data.drop(columns=['Team1:ElderDragonKills', 'Team2:ElderDragonKills', 'Team1:InhibitorsKills', 'Team2:Inhibitors:Kills'])
    data = data.drop(columns=['Winner'])
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
    data = data.drop(columns=['Team1:ElderDragonKills', 'Team2:ElderDragonKills', 'Team1:InhibitorsKills', 'Team2:Inhibitors:Kills'])
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


one_game = getGameDetails(data, 'EUW1_7177092123')
# makeTablePNG(one_game)

allBronze = getALlGamesFromOneElo(data, "Bronze4")
allPlatinum = getALlGamesFromOneElo(data, "Platinum4")
allDiamond = getALlGamesFromOneElo(data, "Diamond4")

# print(allBronze)
# print(allPlatinum)
# print(allDiamond)

#correlationMatrix(allBronze)
#scattermatrix(allBronze)
