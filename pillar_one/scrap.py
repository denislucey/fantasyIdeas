import nfl_data_py as nfl



def main() -> str:
    # creating the dataframe to get player name, id and position
    players = nfl.import_players()
    print(players.columns)
    players = players[['display_name', 'gsis_id','position','birth_date']]
    players.rename(columns={'display_name': 'full_name', 'gsis_id': 'player_id'}, inplace=True)
    players = players.dropna(subset=['birth_date'])
    players['birth_year'] = players['birth_date'].str.split('-').str[0].astype(int)
    print(players.head(10))
    return "SEE"

main()