import nfl_data_py as nfl
import pandas as pd

features = [
    'season','player_id','fantasy_points_ppr'
]

def main():
    players = nfl.import_players()
    players = players[['display_name', 'gsis_id','position']]
    players.rename(columns={'display_name': 'full_name', 'gsis_id': 'player_id'}, inplace=True)
    
    df = nfl.import_seasonal_data(range(2015, 2025),"REG")
    slimmed = df[features]
    slimmed = slimmed.merge(players[['player_id', 'full_name', 'position']], on='player_id', how='left')
    rb_df = slimmed[slimmed['position'] == 'RB']
    print(rb_df.sort_values("fantasy_points_ppr",ascending=False).head(15))
    
    # print(rb_df.head(1))
    return "Yes"


if __name__ == "__main__":
    main()
    print("Test completed successfully.")