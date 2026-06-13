
# import kaggle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# temp_df = pd.read_csv(
#  'https://raw.githubusercontent.com/'
# 'datasets/global-temp/main/data/annual.csv')
#
# temp_df.to_csv('../data/raw/temp_data.csv', index=False)

# Q1) Pivot + melt + grouped bar
def q1():
    pivot_table_chess_games = chess_games_df.pivot_table(
        index='victory_status',
        columns='winner',
        values='turns',
        aggfunc='median'
    )

    melted_df = pivot_table_chess_games.reset_index().melt(
        id_vars='victory_status',
        var_name='winner',
        value_name='median_turns'
    )

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(
        data=melted_df,
        x='victory_status',
        y='median_turns',
        hue='winner',
        palette='Set2'
    )

    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            if not pd.isna(height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    fontweight='bold'
                )

    plt.show()

# Loading Data
print("Start Loading Data:...")
netflix_df = pd.read_csv("../data/raw/netflix_titles.csv")
chess_games_df = pd.read_csv("../data/raw/chess_games.csv")
players_df = pd.read_csv("../data/raw/players.csv")
temp_df = pd.read_csv("../data/raw/players.csv")
print("Finish Loading Data:...")
q1()