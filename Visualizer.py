import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
fname = "gold_stats_challenger.csv"
data = pd.read_csv(fname)

formattedDf = pd.DataFrame()
formattedDf["Minute"] = data["Minute"]
formattedDf["Gold Diff vs Team2"] = data["Team1 Gold"] - data["Team2 Gold"]
formattedDf["Team1 Win"] = (data["Winning Team"] == "Team 1").astype(int)  # 1 for win, 0 for loose


plt.figure(figsize=(12, 7))
array = list(range(22))
selectedData = formattedDf.head(22)
team1Gold = selectedData["Gold Diff vs Team2"]
plt.plot(array, team1Gold, '-r', label='Gold Diff vs Team2')
plt.legend(loc='upper right')
plt.show()