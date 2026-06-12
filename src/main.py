
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

# Loading Data
print("Start Loading Data:...")
netflix_df = pd.read_csv("../data/raw/netflix_titles.csv")
chess_games_df = pd.read_csv("../data/raw/chess_games.csv")
players_df = pd.read_csv("../data/raw/players.csv")
temp_df = pd.read_csv("../data/raw/players.csv")
print("Finish Loading Data:...")




