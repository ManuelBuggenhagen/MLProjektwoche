import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from pandas.plotting import scatter_matrix


class show:
    def __init__(self):
        self.content = pd.read_csv("stats_300_games.csv")

        self.colorList = ["red", "blue", "green", "orange", "purple", "cyan", "yellow", "magenta", "brown", "pink", "grey", "black"]

        pd.set_option('display.max_columns', None)  # Alle Spalten anzeigen
        pd.set_option('display.expand_frame_repr', False)  # Zeilenumbruch vermeiden
        pd.set_option('display.max_rows', None)  # Alle Zeilen anzeige

        print(self.content.head(40))

        # Kennzeichnen der Daten bei denen ein Match endet
        self.content["matchEnd"] = 0
        currentMatchId = self.content.iloc[0]["MatchID"]
        iList = list(range(len(self.content) - 1))
        for i in iList:
            if currentMatchId != self.content.iloc[i]["MatchID"]:
                self.content.at[i - 1, "matchEnd"] = 1
                currentMatchId = self.content.iloc[i]["MatchID"]

        # sumKills Spalte hinzufügen
        self.content["sumKills"] = self.content["Team1:Kills"] + self.content["Team2:Kills"]

        # sumGold Spalte hinzufügen
        self.content["sumGold"] = self.content["Team1:Gold"] + self.content["Team2:Gold"]

    def analyse1(self):
        # List der zu analysierenden Elos
        eloList = self.content["Elo"].unique()
        analyse = pd.DataFrame(columns=["AnzahlMatches", "MinutenMin", "MinutenMax", "MinutenMean", "MinutenStdAbweichung", "KillsMin", "KillsMax", "KillsMean", "KillsStdAbweichung", "GoldMin", "GoldMax", "GoldMean", "GoldStdAbweichung", "Elo"])

        # Std, Mean, Min und Max Werte für alle Elos
        numberOfValues = self.content[self.content["matchEnd"] == 1]["MatchID"].count()
        minMin = self.content[self.content["matchEnd"] == 1]["Minute"].min().round(2)
        minMax = self.content[self.content["matchEnd"] == 1]["Minute"].max().round(2)
        minMean = self.content[self.content["matchEnd"] == 1]["Minute"].mean().round(2)
        minStd = self.content[self.content["matchEnd"] == 1]["Minute"].std().round(2)

        killsMin = self.content[self.content["matchEnd"] == 1]["sumKills"].min().round(2)
        killsMax = self.content[self.content["matchEnd"] == 1]["sumKills"].max().round(2)
        killsMean = self.content[self.content["matchEnd"] == 1]["sumKills"].mean().round(2)
        killsStd = self.content[self.content["matchEnd"] == 1]["sumKills"].std().round(2)

        goldMin = self.content[self.content["matchEnd"] == 1]["sumGold"].min().round(2)
        goldMax = self.content[self.content["matchEnd"] == 1]["sumGold"].max().round(2)
        goldMean = self.content[self.content["matchEnd"] == 1]["sumGold"].mean().round(2)
        goldStd = self.content[self.content["matchEnd"] == 1]["sumGold"].std().round(2)

        # Ergebnisse der Analyse hinzufügen
        analyse.loc[len(analyse)] = [numberOfValues, minMin, minMax, minMean, minStd, killsMin, killsMax, killsMean, killsStd, goldMin, goldMax, goldMean, goldStd, "Alle"]

        # Std, Mean, Min und Max Werte für jede Elo einzeln
        for elo in eloList:
            numberOfValues = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["MatchID"].count()

            minMin = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["Minute"].min().round(2)
            minMax = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["Minute"].max().round(2)
            minMean = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["Minute"].mean().round(2)
            minStd = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["Minute"].std().round(2)

            killsMin = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumKills"].min().round(2)
            killsMax = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumKills"].max().round(2)
            killsMean = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumKills"].mean().round(2)
            killsStd = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumKills"].std().round(2)

            goldMin = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumGold"].min().round(2)
            goldMax = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumGold"].max().round(2)
            goldMean = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumGold"].mean().round(2)
            goldStd = self.content[(self.content["matchEnd"] == 1) & (self.content["Elo"] == elo)]["sumGold"].std().round(2)

            # Ergebnisse der Analyse hinzufügen
            analyse.loc[len(analyse)] = [numberOfValues, minMin, minMax, minMean, minStd, killsMin, killsMax, killsMean,
                                         killsStd, goldMin, goldMax, goldMean, goldStd, elo]

        print(analyse)
        return analyse

    def showAnalyse1(self, analyse):
        # Fenster definieren
        fig, axes = plt.subplots(4, 3, figsize=(12, 6))

        # Iterations-Variablen erstellen
        values = []
        #atributList = ["MinutenMin", "MinutenMax", "MinutenMean", "KillsMin", "KillsMax", "KillsMean", "GoldMin", "GoldMax", "GoldMean"]
        atributList = ["MinutenMin", "MinutenMax", "MinutenMean", "MinutenStdAbweichung", "KillsMin", "KillsMax", "KillsMean", "KillsStdAbweichung", "GoldMin", "GoldMax", "GoldMean", "GoldStdAbweichung"]
        gridPosition = [0, 0]

        # Fenster mit den verschiedenen Diagrammen füllen
        for atributIndex in range(len(atributList)):
            atribut = atributList[atributIndex]
            values = analyse[atribut].tolist()
            position = np.linspace(0, 10, len(values)).tolist()

            pos = tuple(gridPosition)
            axes[pos].bar(position, height=values, color=self.colorList, edgecolor='black', width=1, alpha=0.8)
            axes[pos].set_xticks([])
            axes[pos].set_title(atribut)

            # Wenn unten angekommen eine Zeile weiter gehen
            if gridPosition[0] == 3:
                gridPosition = np.add(gridPosition, [-4, 1]).tolist()
            gridPosition = np.add(gridPosition, [1, 0]).tolist()

        # Label mit farben setzten
        legend_handles = [mpatches.Patch(color=color, label=label) for color, label in zip(self.colorList, analyse["Elo"].tolist())]
        fig.legend(handles=legend_handles,
                   loc="lower center",  # Position der Legende
                   ncol=4)

        # Fenster anzeigen
        plt.tight_layout()
        plt.show()

    def showStdPerRound(self):
        kill_stats = self.content.groupby("Minute")["sumKills"].mean()
        gold_stats = self.content.groupby("Minute")["sumGold"].mean()

        # Liniendiagramm erstellen
        plt.figure(figsize=(12, 6))

        # Plot für die durchschnittlichen Kills pro Minute
        plt.plot(kill_stats.index, kill_stats, label='Durchschnittliche Kills pro Minute', color='blue')

        # Plot f端r das durchschnittliche Gold pro Minute
        plt.plot(gold_stats.index, gold_stats, label='Durchschnittliches Gold pro Minute', color='red')

        # Achsentitel und Diagrammtitel setzen
        plt.xlabel("Minute")
        plt.ylabel("Werte")
        plt.title("Durchschnittliche Kills und Gold pro Minute")

        # Legende hinzufügen
        plt.legend()

        # Layout optimieren und Diagramm anzeigen
        plt.tight_layout()
        plt.show()

    def showMeanKillPerElo(self):
        # Liniendiagramm erstellen
        plt.figure(figsize=(12, 6))
        minuten = self.content[self.content["Elo"] == "Bronze4"]["Minute"].unique()


        durchschnittliche_kills = [
            self.content[(self.content["Elo"] == "Bronze4") & (self.content["Minute"] == minute)]["sumKills"].mean()
            for minute in minuten
        ]
        plt.plot(minuten, durchschnittliche_kills, label='Bronze4', color=self.colorList[0])

        durchschnittliche_kills = [
            self.content[(self.content["Elo"] == "Platinum4") & (self.content["Minute"] == minute)]["sumKills"].mean()
            for minute in minuten
        ]
        plt.plot(minuten, durchschnittliche_kills, label='Platinum4', color=self.colorList[1])

        durchschnittliche_kills = [
            self.content[(self.content["Elo"] == "Diamond4") & (self.content["Minute"] == minute)]["sumKills"].mean()
            for minute in minuten
        ]
        plt.plot(minuten, durchschnittliche_kills, label='Diamond4', color=self.colorList[2])

        plt.xlabel("Minute")
        plt.ylabel("Durchschnittliche Kills")
        plt.title("Durchschnittliche Kills der Elos")

        # Legende hinzufügen
        plt.legend()

        plt.tight_layout()
        plt.show()

    def correlation(self):
        # Filtern der Daten die wir nicht mitnehmen wollen
        columns_to_exclude = ["Team1:TopLane",  "Team1:Jungle",  "Team1:MidLane",  "Team1:AD Carry",  "Team1:Support",  "Team2:TopLane", "Team2:Jungle",  "Team2:MidLane",  "Team2:AD Carry",  "Team2:Support", "Winner", "matchEnd", "MatchID", "Elo", "Unnamed: 0"]
        filtered_content = self.content.drop(columns=columns_to_exclude, inplace=False)

        correlation_matrix = filtered_content.corr()

        # Heatmap zeichnen
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Korrelationsmatrix")
        plt.show()

    def scatter(self):
        # Filtern der Daten die wir nicht mitnehmen wollen
        columns_to_exclude = ["Team1:TopLane", "Team1:Jungle", "Team1:MidLane", "Team1:AD Carry", "Team1:Support",
                              "Team2:TopLane", "Team2:Jungle", "Team2:MidLane", "Team2:AD Carry", "Team2:Support",
                              "Winner", "matchEnd", "MatchID", "Elo", "Unnamed: 0"]
        filtered_content = self.content.drop(columns=columns_to_exclude, inplace=False)

        fig, ax = plt.subplots(figsize=(12, 8))
        scatter_matrix(
            filtered_content,
            figsize=(12, 8),
            diagonal='hist',  # Histogramme auf der Diagonale
            cmap='viridis',  # Farbschema (z.B. 'viridis', 'plasma', 'coolwarm')
            ax=ax
        )

        # Schriftgröße der Achsenbeschriftungen anpassen
        for ax in fig.axes:
            ax.xaxis.label.set_fontsize(10)
            ax.yaxis.label.set_fontsize(10)
            ax.tick_params(axis='x', rotation=45, labelsize=8)  # X-Achse drehen
            ax.tick_params(axis='y', labelsize=8)  # Y-Achse Schriftgröße anpassen

        plt.show()


if __name__ == "__main__":
    show = show()
    analyse = show.analyse1()
    show.showAnalyse1(analyse)
    show.showStdPerRound()
    show.showMeanKillPerElo()
    show.correlation()
    show.scatter()
