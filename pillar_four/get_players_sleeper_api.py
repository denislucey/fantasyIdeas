from sleeperpy import Players
import pandas as pd

def get_sleeper_draft_and_write_to_csv_file():
    player_json = Players.get_all_players()

    df = pd.DataFrame(player_json.items())
    df.to_csv('PlayersFromSleeper.csv',encoding='utf-8',index=False)




def main():
    get_sleeper_draft_and_write_to_csv_file()

# Only run this once, big api call
main()