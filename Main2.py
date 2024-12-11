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
fname = "all_gold_stats.csv"
data = pd.read_csv(fname)
# print(data.head(10),"\n")

formattedDf = pd.DataFrame()
formattedDf["Minute"] = data["Minute"]
formattedDf["Gold Diff vs Team2"] = data["Team1 Gold"] - data["Team2 Gold"]
formattedDf["Team1 Win"] = (data["Winning Team"] == "Team1").astype(int)  # 1 for win, 0 for loose
print("original data:\n", formattedDf.head(10), "\n")

"""
# Normalisieren der Daten
mmScaler = MinMaxScaler()
featureData = formattedDf.iloc[:, :-1]
#print("feature Data:\n", featureData)
dataNormal = mmScaler.fit_transform(featureData)
dataNormalFrame = pd.DataFrame(dataNormal, columns=featureData.columns)
print("normalized data:\n", dataNormalFrame.head(10), "\n")
"""

# Aufteilen der Daten in Trainings- und Testdaten
X = formattedDf[['Minute', 'Gold Diff vs Team2']]
Y = formattedDf['Team1 Win']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
print("test Data:\n", X_test, "\n")

# Trainieren des Modells
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1, max_iter=2000)
clf.fit(X_train, y_train)

prediction = clf.predict(X_test)
print("prediction:\n", prediction, "\n")
print("test values:\n", y_test.values, "\n")

# accuracy score
acc_score = round(accuracy_score(y_test, prediction), 2)
print('Accuracy:', acc_score)





