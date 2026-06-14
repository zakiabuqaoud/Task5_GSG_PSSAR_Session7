
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

# Q3 method
def q3():
    print("Start Question3 ...")
    gist_temp_df = temp_df[temp_df['Source'] == 'GISTEMP'].copy()
    gist_temp_df = gist_temp_df.sort_values('Year')

    gist_temp_df['rolling_10'] = gist_temp_df['Mean'].rolling(window=10).mean()

    hottest_row = gist_temp_df.loc[gist_temp_df['Mean'].idxmax()]
    hottest_year = int(hottest_row['Year'])
    hottest_temp = hottest_row['Mean']

    plt.figure(figsize=(14, 7))
    plt.plot(gist_temp_df['Year'], gist_temp_df['Mean'],
             color='black', linewidth=1.5, label='gist_temp Annual Mean')

    plt.plot(gist_temp_df['Year'], gist_temp_df['rolling_10'],
             color='red', linewidth=2.5, linestyle='--',
             label='Rolling 10-Year Average')

    plt.fill_between(gist_temp_df['Year'], gist_temp_df['Mean'], 0,
                     where=(gist_temp_df['Mean'] >= 0),
                     color='red', alpha=0.3, label='Above Zero')

    plt.fill_between(gist_temp_df['Year'], gist_temp_df['Mean'], 0,
                     where=(gist_temp_df['Mean'] < 0),
                     color='blue', alpha=0.3, label='Below Zero')

    plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.7)

    plt.annotate(f'Hottest Year: {hottest_year}\n{hottest_temp:.2f}°C',
                 xy=(hottest_year, hottest_temp),
                 xytext=(hottest_year - 15, hottest_temp + 0.3),
                 arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
                 fontsize=11, fontweight='bold', color='darkred',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))

    plt.scatter(hottest_year, hottest_temp, color='darkred', s=80, zorder=5, edgecolors='black')

    plt.title('Global Temperature Anomaly (GISTEMP)\n1880 - Present',
              fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Temperature Anomaly (°C)', fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    print("Finish question3 ...")

def q4():
    print("Question 4 started ...")
    movies = netflix_df[netflix_df['type'] == 'Movie'].copy()
    movies['duration_min'] = movies['duration'].str.extract(r'(\d+)').astype(float)
    movies_clean = movies.dropna(subset=['duration_min'])

    plt.figure(figsize=(12, 6))

    n, bins, patches = plt.hist(movies_clean['duration_min'],
                                bins=30,
                                color='steelblue',
                                edgecolor='black',
                                alpha=0.7,
                                label='Movies')

    mean_dur = movies_clean['duration_min'].mean()
    plt.axvline(mean_dur, color='red', linestyle='--', linewidth=2,
                label=f'Mean: {mean_dur:.1f} min')

    median_dur = movies_clean['duration_min'].median()
    plt.axvline(median_dur, color='green', linestyle='-.', linewidth=2,
                label=f'Median: {median_dur:.1f} min')

    plt.title('Distribution of Movie Durations on Netflix', fontsize=14, fontweight='bold')
    plt.xlabel('Duration (minutes)', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    print("Question 4 finished ...")


# Loading Data
print("Start Loading Data:...")
netflix_df = pd.read_csv("../data/raw/netflix_titles.csv")
chess_games_df = pd.read_csv("../data/raw/chess_games.csv")
players_df = pd.read_csv("../data/raw/players.csv")
temp_df = pd.read_csv("../data/raw/temp_data.csv")
print("Finish Loading Data:...")

# Solution on the Question
q1_median_turns()
q2()
q3()
q4()
