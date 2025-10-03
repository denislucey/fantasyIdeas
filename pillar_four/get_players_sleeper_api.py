from sleeperpy import Players
import pandas as pd
import os

def get_sleeper_draft_and_write_to_csv_file(write = True):
    player_json = Players.get_all_players()


    df = pd.DataFrame.from_dict(player_json,orient='index')
    df = df[['full_name']]
    df.to_csv('PlayersFromSleeper.csv',encoding='utf-8',index=False)
    return df


def main():
    get_sleeper_draft_and_write_to_csv_file()
    # turn_sleeper_csv_into_index()

# Only run this once, big api call
main()