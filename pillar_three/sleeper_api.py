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
def sleeper_draft_buddy(draft_id: str,print_positions: bool):
    
    # call api to get drafted players
    taken_players = sleeper_api_call(draft_id)

    #import value sheet
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\ktc_value.csv')

    filtered_players = players[['Updated 08/07/25 at 09:19am','Position','Team','Value','Age']]
    filtered_players.columns = ['Name','Position','Team','Value','Age']

    
    remaining_players = filtered_players[~filtered_players['Name'].isin(taken_players)].dropna()

    positions = ["QB","RB","WR","TE"]
    if print_positions:
        for pos in positions:
            print(remaining_players[remaining_players['Position'] == pos].sort_values(by='Value',ascending=False).head(3))
    else:
        print(remaining_players.sort_values(by='Value',ascending=False).head(8))



DRAFT_ID = '1260287819801169920'

def main():
    start_time = time.time()
    sleeper_draft_buddy(draft_id=DRAFT_ID,print_positions=True)
    print(f"Exectution Time: {time.time() - start_time}")

main()

# Benchmarks:
# 2 WR in top 3 picks

#3 QB in top 8 rounds
# 3 WR in top 5 picks
