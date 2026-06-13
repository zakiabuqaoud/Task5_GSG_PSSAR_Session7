

import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# 1. تحميل ملف المباريات فقط (هذا هو المطلوب)
# ============================================
df = pd.read_csv('../data/raw/chess_games.csv')  # ملف المباريات الذي أرسلته

print("أول 5 مباريات:")
print(df.head())
print(f"\nعدد المباريات الكلي: {len(df)}")

# ============================================
# 2. اختيار لاعب لديه 15+ مباراة (كلاعب أبيض أو أسود)
# ============================================
# نجمع جميع المباريات لكل لاعب (سواء أبيض أو أسود)
all_white = df['white_id'].value_counts()
all_black = df['black_id'].value_counts()
total_games_per_player = all_white.add(all_black, fill_value=0).sort_values(ascending=False)

print("\nاللاعبون الذين لديهم 15+ مباراة:")
players_15plus = total_games_per_player[total_games_per_player >= 15]
print(players_15plus)

# نختار لاعبًا (مثال: shivangithegenius)
player_name = 'shivangithegenius'  # يمكنك تغييره

# ============================================
# 3. استخراج جميع مباريات هذا اللاعب (بيانات حقيقية)
# ============================================
# مباريات كلاعب أبيض
white_games = df[df['white_id'] == player_name].copy()
white_games['rating'] = white_games['white_rating']
white_games['color'] = 'White'
white_games['game_order'] = range(1, len(white_games) + 1)  # ترتيب زمني

# مباريات كلاعب أسود
black_games = df[df['black_id'] == player_name].copy()
black_games['rating'] = black_games['black_rating']
black_games['color'] = 'Black'
black_games['game_order'] = range(1, len(black_games) + 1)

# دمج المباريات وترتيبها حسب game_id (الزمن الحقيقي)
all_player_games = pd.concat([white_games, black_games], ignore_index=True)
all_player_games = all_player_games.sort_values('game_id').reset_index(drop=True)
all_player_games['game_number'] = range(1, len(all_player_games) + 1)

print(f"\nاللاعب {player_name} لديه {len(all_player_games)} مباراة:")
print(all_player_games[['game_number', 'color', 'rating', 'white_id', 'black_id']].head(10))

# ============================================
# 4. التأكد من وجود 15+ مباراة
# ============================================
if len(all_player_games) < 15:
    print(f"\n⚠️ هذا اللاعب لديه {len(all_player_games)} مباراة فقط (<15)")
    print("سيتم اختيار لاعب آخر تلقائيًا...")
    # اختيار أول لاعب في القائمة لديه 15+ مباراة
    for player in players_15plus.index:
        # حساب مباريات هذا اللاعب
        temp_white = df[df['white_id'] == player].copy()
        temp_white['rating'] = temp_white['white_rating']
        temp_black = df[df['black_id'] == player].copy()
        temp_black['rating'] = temp_black['black_rating']
        temp_all = pd.concat([temp_white, temp_black], ignore_index=True)
        if len(temp_all) >= 15:
            player_name = player
            all_player_games = temp_all.sort_values('game_id').reset_index(drop=True)
            all_player_games['game_number'] = range(1, len(all_player_games) + 1)
            print(f"✅ تم اختيار اللاعب: {player_name} (لديه {len(all_player_games)} مباراة)")
            break

# ============================================
# 5. حساب المتوسطات (بدون أي قيم عشوائية)
# ============================================
all_player_games['rolling_5'] = all_player_games['rating'].rolling(window=5).mean()
all_player_games['expanding'] = all_player_games['rating'].expanding().mean()

# ============================================
# 6. إيجاد أعلى تقييم
# ============================================
max_rating = all_player_games['rating'].max()
max_game = all_player_games[all_player_games['rating'] == max_rating]['game_number'].values[0]

print(f"\n📊 تحليل اللاعب {player_name}:")
print(f"   - عدد المباريات: {len(all_player_games)}")
print(f"   - أعلى تقييم: {max_rating} (المباراة رقم {max_game})")
print(f"   - أول 5 مباريات (بيانات حقيقية):")
print(all_player_games[['game_number', 'rating', 'rolling_5', 'expanding']].head())

# ============================================
# 7. الرسم (باستخدام بيانات حقيقية 100%)
# ============================================
plt.figure(figsize=(12, 6))

# الرسم الخام (Raw)
plt.plot(all_player_games['game_number'], all_player_games['rating'],
         marker='o', linestyle='-', linewidth=1.5, markersize=4,
         label='Raw Rating', color='blue', alpha=0.7)

# المتوسط المتحرك (Rolling 5)
plt.plot(all_player_games['game_number'], all_player_games['rolling_5'],
         marker='s', linestyle='--', linewidth=2, markersize=4,
         label='Rolling(5) Average', color='orange')

# المتوسط التراكمي (Expanding)
plt.plot(all_player_games['game_number'], all_player_games['expanding'],
         marker='^', linestyle='-.', linewidth=2, markersize=4,
         label='Expanding Average', color='green')

# تعليم أعلى تقييم
plt.annotate(f'Highest: {max_rating}',
             xy=(max_game, max_rating),
             xytext=(max_game + 1, max_rating + 50),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             fontsize=10, fontweight='bold', color='red',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# تنسيق الرسم
plt.title(f'Rolling Analysis for Player: {player_name}\n({len(all_player_games)} Real Games)',
          fontsize=14, fontweight='bold')
plt.xlabel('Game Number (Chronological order by game_id)', fontsize=12)
plt.ylabel('Rating', fontsize=12)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# عرض الجدول الكامل للمباريات
print("\n📋 جميع مباريات اللاعب (بيانات حقيقية):")
print(all_player_games[['game_number', 'color', 'rating', 'rolling_5', 'expanding', 'victory_status', 'winner']])