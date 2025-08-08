from sleeperpy import Drafts
import pandas as pd
import os
import time

def sleeper_api_call(draft_id: str):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    new_draft_results = []
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        new_draft_results.append(name)

    return new_draft_results        

# Only use if you are on the clock
def sleeper_draft_buddy(draft_id: str):
    
    # call api to get drafted players
    taken_players = sleeper_api_call(draft_id)

    #import value sheet
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\ktc_value.csv')

    filtered_players = players[['Updated 08/07/25 at 09:19am','Position','Team','Value','Age']]
    filtered_players.columns = ['Name','Position','Team','Value','Age']

    
    remaining_players = filtered_players[~filtered_players['Name'].isin(taken_players)].dropna()

    print(remaining_players.sort_values(by='Value',ascending=False).head(5))



def print_bpa(pos: str, draft_id: str, amt: int):
    taken_players = sleeper_api_call(draft_id)
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\sheet_7_13.csv')

    filtered_players = players[['Player', 'Proj Points', 'Position','Sleeper ADP','PARL']].fillna(500)
    filtered_players.columns = ['Name', 'Points', 'Position', 'ADP','PARL']
    remaining_players = filtered_players[~filtered_players['Name'].isin(taken_players)]
    print(remaining_players[remaining_players['Position'] == pos].sort_values(by='V', ascending=False).head(amt))
    return


DRAFT_ID = '1259369380064534528'

def main():
    start_time = time.time()
    sleeper_draft_buddy(draft_id=DRAFT_ID)
    print(f"Exectution Time: {time.time() - start_time}")

main()
# print_bpa('WR',DRAFT_ID,3)
# print_bpa('RB',DRAFT_ID,3)
# print_bpa('TE',DRAFT_ID,3)
# print_bpa('QB',DRAFT_ID,3)