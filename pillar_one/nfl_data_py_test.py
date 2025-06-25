import nfl_data_py as nfl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

features = [
    'season','player_id','fantasy_points_ppr','games'
]

test_features = [
    'carries', 'rushing_yards',
    'rushing_tds', 'rushing_fumbles', 'rushing_fumbles_lost',
    'rushing_first_downs', 'rushing_epa', 'rushing_2pt_conversions',
    'receptions', 'targets', 'receiving_yards', 'receiving_tds',
    'receiving_fumbles', 'receiving_fumbles_lost', 'receiving_air_yards',
    'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa',
    'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share',
    'wopr_x', 'special_teams_tds', 'fantasy_points', 'fantasy_points_ppr',
    'games', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh',
    'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh', 'years_in_league',
    'age'
]

def main() -> str:
    # creating the dataframe to get player name, id and position
    players = nfl.import_players()
    players = players[['display_name', 'gsis_id','position','birth_date', 'rookie_year']]
    players.rename(columns={'display_name': 'full_name', 'gsis_id': 'player_id'}, inplace=True)
    players = players.dropna(subset=['birth_date'])
    players['birth_year'] = players['birth_date'].str.split('-').str[0].astype(int)
    print(players.columns)
    
    # getting the data from 2015 to 2024
    df = nfl.import_seasonal_data(range(2015, 2025),"REG")
    # print(df.columns)

    slimmed = df
    slimmed = slimmed.merge(players[['player_id', 'full_name', 'position','rookie_year','birth_year']], on='player_id', how='left')
    rb_df = slimmed[slimmed['position'] == 'RB']
    # print(rb_df.columns)
    rb_df['fantasy_ppr_ppg'] = rb_df['fantasy_points_ppr'] / rb_df['games']
    rb_df['years_in_league'] = rb_df['season'] - rb_df['rookie_year']
    rb_df['age'] = rb_df['season'] - rb_df['birth_year']
    rb_df['next_season_fantasy_points'] = rb_df.groupby('player_id')['fantasy_points_ppr'].shift(-1)
    rb_df['next_season_fantasy_ppr_ppg'] = rb_df.groupby('player_id')['fantasy_ppr_ppg'].shift(-1)
    next_season_players = rb_df[rb_df['season'] == 2024]
    rb_df = rb_df.dropna(subset=['next_season_fantasy_points'])
    X = rb_df[test_features]
    y = rb_df['next_season_fantasy_ppr_ppg']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    print(f"Model's Average Error: {mae:.2f} fantasy points")


    # print(next_season_players.head(45))
    next_season_predictions = model.predict(next_season_players[test_features])

    next_season_players['predicted_fantasy_ppr_ppg'] = next_season_predictions * 17
    condensed = next_season_players[['full_name', 'player_id', 'predicted_fantasy_ppr_ppg']]
    print(condensed.sort_values('predicted_fantasy_ppr_ppg',ascending=False).head(45))


    return "Yes"


if __name__ == "__main__":
    main()
    print("Test completed successfully.")