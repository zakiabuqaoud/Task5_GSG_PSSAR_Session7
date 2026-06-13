
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
def q1_median_turns():
    print("Start Q1) med turns by Victory Status and Winner")

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
    plt.title('Median Turns by Victory Status and Winner', fontsize=14)
    plt.xlabel('Victory Status', fontsize=12)
    plt.ylabel('Median Turns', fontsize=12)

    plt.show()
    print("Finish Q1) Med turns by Victory Status and Winner")

# Q2 Choose any player with 15+ games. Plot raw rating + rolling(5) + expanding avg. Annotate their highest-rated game.
def q2():
    print("Q2 Started...")
    all_white = chess_games_df['white_id'].value_counts()
    all_black = chess_games_df['black_id'].value_counts()
    total_games_per_player = all_white.add(all_black, fill_value=0).sort_values(ascending=False)

    players_15games = total_games_per_player[total_games_per_player >= 15]
    players_15games = players_15games.reset_index()
    # print selected player
    player_name = players_15games. iloc[0]['white_id']
    print(f"The Player is selected: {player_name} ")

    # when was white
    white_games = chess_games_df[chess_games_df['white_id'] == player_name].copy()
    white_games['rating'] = white_games['white_rating']
    white_games['color'] = 'White'
    white_games['game_order'] = range(1, len(white_games) + 1)  # ترتيب زمني

    # when was black
    black_games = chess_games_df[chess_games_df['black_id'] == player_name].copy()
    black_games['rating'] = black_games['black_rating']
    black_games['color'] = 'Black'
    black_games['game_order'] = range(1, len(black_games) + 1)

    all_player_games = pd.concat([white_games, black_games], ignore_index=True)
    all_player_games = all_player_games.sort_values('game_id').reset_index(drop=True)
    all_player_games['game_number'] = range(1, len(all_player_games) + 1)

    for player in players_15games.index:
        temp_white = chess_games_df[chess_games_df['white_id'] == player].copy()
        temp_white['rating'] = temp_white['white_rating']
        temp_black = chess_games_df[chess_games_df['black_id'] == player].copy()
        temp_black['rating'] = temp_black['black_rating']
        temp_all = pd.concat([temp_white, temp_black], ignore_index=True)
        if len(temp_all) >= 15:
            player_name = player
            all_player_games = temp_all.sort_values('game_id').reset_index(drop=True)
            all_player_games['game_number'] = range(1, len(all_player_games) + 1)
            break
    all_player_games['rolling_5'] = all_player_games['rating'].rolling(window=5).mean()
    all_player_games['expanding'] = all_player_games['rating'].expanding().mean()

    max_rating = all_player_games['rating'].max()
    max_game = all_player_games[all_player_games['rating'] == max_rating]['game_number'].values[0]

    plt.figure(figsize=(12, 6))

    # Expanding
    plt.plot(all_player_games['game_number'], all_player_games['expanding'],
             marker='^', linestyle='-.', linewidth=2, markersize=4,
             label='Expanding Average', color='green')

    plt.annotate(f'Highest: {max_rating}',
                 xy=(max_game, max_rating),
                 xytext=(max_game + 1, max_rating + 50),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                 fontsize=10, fontweight='bold', color='red',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))


    plt.plot(all_player_games['game_number'], all_player_games['rating'],
             marker='o', linestyle='-', linewidth=1.5, markersize=4,
             label='Raw Rating', color='blue', alpha=0.7)

    plt.plot(all_player_games['game_number'], all_player_games['rolling_5'],
             marker='s', linestyle='--', linewidth=2, markersize=4,
             label='Rolling(5) Average', color='orange')

    plt.title(f'Rolling Analysis for Player: {player_name}\n({len(all_player_games)} Real Games)',
              fontsize=14, fontweight='bold')
    plt.xlabel('Game Number (Chronological order by game_id)', fontsize=12)
    plt.ylabel('Rating', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Q2 Finished...")


# Loading Data
print("Start Loading Data:...")
netflix_df = pd.read_csv("../data/raw/netflix_titles.csv")
chess_games_df = pd.read_csv("../data/raw/chess_games.csv")
players_df = pd.read_csv("../data/raw/players.csv")
temp_df = pd.read_csv("../data/raw/players.csv")
print("Finish Loading Data:...")

# Solution on the Question
q1_median_turns()
q2()