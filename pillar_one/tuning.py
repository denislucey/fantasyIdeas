import nfl_data_py as nfl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
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


df = nfl.import_seasonal_data(range(2013, 2025),"REG")
merged_df = df.merge(players[['player_id', 'full_name', 'position','rookie_year','birth_year']], on='player_id', how='left')

def project_top_x_players_for_position(x: int, pos: str) -> None:

    if pos == 'RB':
        base_feature_list = RandomForestFeatures.RB_FEATURES.value
    elif pos == 'WR':
        base_feature_list = RandomForestFeatures.WR_FEATURES.value
    elif pos == 'TE':
        base_feature_list = RandomForestFeatures.TE_FEATURES.value
    else:
        base_feature_list = RandomForestFeatures.QB_FEATURES.value

    pos_df = merged_df[merged_df['position'] == pos]
    pos_df = pos_df.sort_values(by=['full_name', 'season'])
    pos_df['fantasy_ppr_ppg'] = pos_df['fantasy_points_ppr'] / pos_df['games']
    pos_df['rush_ypc'] = pos_df['rushing_yards'] / pos_df['carries']
    pos_df['rush_ypg'] = pos_df['rushing_yards'] / pos_df['games']
    pos_df['years_in_league'] = pos_df['season'] - pos_df['rookie_year']
    pos_df['age'] = pos_df['season'] - pos_df['birth_year']
    pos_df['next_season_fantasy_points'] = pos_df.groupby('player_id')['fantasy_points_ppr'].shift(-1)
    pos_df['next_season_fantasy_ppr_ppg'] = pos_df.groupby('player_id')['fantasy_ppr_ppg'].shift(-1)
    
    feature_list = base_feature_list.copy()
    
    for feature in base_feature_list:
        pos_df[feature + '_minus_one'] = pos_df.groupby('player_id')[feature].shift(1)
        feature_list.append(feature + '_minus_one')
        # pos_df[feature + '_minus_two'] = pos_df.groupby('player_id')[feature].shift(2)
        # feature_list.append(feature + '_minus_two')

    pos_df = pos_df.dropna(subset=['next_season_fantasy_points'])

    X = pos_df[feature_list]
    y = pos_df['next_season_fantasy_ppr_ppg']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    print(f"Model has {X_train.shape[1]} features and {X_train.shape[0]} training samples.")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    print(f"Model's Average Error: {mae:.2f} fantasy points")

    param_grid = {
    'n_estimators': [100],
    'max_depth': [10, 20, None],
    'min_samples_leaf': [1, 3, 5],
    'max_features': ['sqrt', 0.3, 0.5]
    }

    grid = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid.fit(X, y)

    print("Best Params:", grid.best_params_)
    print("Best MAE:", -grid.best_score_)

    return


def main() -> str:
    # getting the data from 2015 to 2024
    # ML stuff that I need to better understand
    project_top_x_players_for_position(35, 'QB')
    # project_top_x_players_for_position(45, 'RB')
    # project_top_x_players_for_position(45, 'WR')
    # project_top_x_players_for_position(25, 'TE')
    return "Yes"


if __name__ == "__main__":
    main()
    print("Test completed successfully.")