from sleeperpy import Drafts
from draft_picks import get_picks
from classes import Player, Roster
from draft_buddy import draft_buddy_selective
from scipy.stats import norm
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
def sleeper_draft_buddy(draft_id: str, spot: int, thr_rr: bool,depth: int):
    # get picks
    picks = get_picks(spot,thr_rr)

    # call api to get drafted players
    taken_players = sleeper_api_call(draft_id)

    #import players
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\sheet_7_13.csv')

    filtered_players = players[['Player', 'Proj Points', 'Position','Sleeper ADP']].fillna(500)
    filtered_players.columns = ['Name', 'Points', 'Position', 'ADP']
    # filtered_players = players[['Name', 'Points', 'Position','ADP']].fillna(500)

    # get players you have drafted
    my_players = []
    for pick in picks:
        if pick > len(taken_players):
            continue
        else:
            my_players.append(taken_players[pick-1])

    # create roster with those players
    my_roster = Roster()
    for player in my_players:
        player_data = filtered_players[filtered_players['Name']==player].iloc[0]
        player_to_add = Player(player,player_data['Position'],player_data['Points'],0)
        my_roster.add_player(player_to_add)

    remaining_players = filtered_players[~filtered_players['Name'].isin(taken_players)]

    best_roster = draft_buddy_selective(picks,len(my_players)+1,remaining_players,my_roster,depth)
    print(best_roster)
    # call draft buddy



def print_bpa(pos: str, draft_id: str, amt: int):
    taken_players = sleeper_api_call(draft_id)
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\sheet_7_13.csv')

    filtered_players = players[['Player', 'Proj Points', 'Position','Sleeper ADP','PARL']].fillna(500)
    filtered_players.columns = ['Name', 'Points', 'Position', 'ADP','PARL']
    remaining_players = filtered_players[~filtered_players['Name'].isin(taken_players)]
    print(remaining_players[remaining_players['Position'] == pos].sort_values(by='Points', ascending=False).head(amt))
    return

def main():
    start_time = time.time()
    sleeper_draft_buddy('1256707916308692992',10,True,0)
    print(f"Exectution Time: {time.time() - start_time}")

main()
# print_bpa('WR','1251017401995112448',3)
# print_bpa('RB','1251017401995112448',3)
# print_bpa('TE','1251017401995112448',3)
# print_bpa('QB','1251017401995112448',3)