import nfl_data_py as nfl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from constants import RandomForestFeatures

features = [
    'season','player_id','fantasy_points_ppr','games'
]

# creating the dataframe to get player name, id and position
players = nfl.import_players()
players = players[['display_name', 'gsis_id','position','birth_date', 'rookie_year']]
players.rename(columns={'display_name': 'full_name', 'gsis_id': 'player_id'}, inplace=True)
players = players.dropna(subset=['birth_date'])
players['birth_year'] = players['birth_date'].str.split('-').str[0].astype(int)


df = nfl.import_seasonal_data(range(2015, 2025),"REG")
merged_df = df.merge(players[['player_id', 'full_name', 'position','rookie_year','birth_year']], on='player_id', how='left')

def project_top_x_players_for_position(x: int, pos: str) -> None:

    if pos in ['RB', 'WR', 'TE']:
        feature_list = RandomForestFeatures.RB_FEATURES.value
    else:
        feature_list = RandomForestFeatures.QB_FEATURES.value

    pos_df = merged_df[merged_df['position'] == pos]
    pos_df['fantasy_ppr_ppg'] = pos_df['fantasy_points_ppr'] / pos_df['games']
    pos_df['years_in_league'] = pos_df['season'] - pos_df['rookie_year']
    pos_df['age'] = pos_df['season'] - pos_df['birth_year']
    pos_df['next_season_fantasy_points'] = pos_df.groupby('player_id')['fantasy_points_ppr'].shift(-1)
    pos_df['next_season_fantasy_ppr_ppg'] = pos_df.groupby('player_id')['fantasy_ppr_ppg'].shift(-1)
    next_season_players = pos_df[pos_df['season'] == 2024]
    pos_df = pos_df.dropna(subset=['next_season_fantasy_points'])

    X = pos_df[RandomForestFeatures.RB_FEATURES.value]
    y = pos_df['next_season_fantasy_ppr_ppg']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    print(f"Model's Average Error: {mae:.2f} fantasy points")


    # creating the next season predictions and using them to print the top 45 players
    next_season_predictions = model.predict(next_season_players[RandomForestFeatures.RB_FEATURES.value])

    next_season_players['predicted_fantasy_ppr_ppg'] = next_season_predictions * 17
    condensed = next_season_players[['full_name', 'player_id', 'predicted_fantasy_ppr_ppg']]
    
    print(f"Top {x} projected {pos} for the 2025 season:")
    print(condensed.sort_values('predicted_fantasy_ppr_ppg',ascending=False).head(x))

    return


def main() -> str:
    # getting the data from 2015 to 2024
    # ML stuff that I need to better understand
    project_top_x_players_for_position(35, 'QB')
    project_top_x_players_for_position(45, 'RB')
    project_top_x_players_for_position(45, 'WR')
    project_top_x_players_for_position(25, 'TE')
    return "Yes"


if __name__ == "__main__":
    main()
    print("Test completed successfully.")