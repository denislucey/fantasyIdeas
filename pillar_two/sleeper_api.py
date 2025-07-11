from sleeperpy import Drafts
from draft_picks import get_picks
from classes import Player, Roster
from draft_buddy import draft_buddy
import pandas as pd
import os

def sleeper_api_call(draft_id: str, picks):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    new_draft_results = []
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        new_draft_results.append(name)

    return new_draft_results
        

# Only use if you are on the clock
def sleeper_draft_buddy(draft_id: str, spot: int, thr_rr: bool):
    # get picks
    picks = get_picks(spot,thr_rr)

    # call api to get drafted players
    taken_players = sleeper_api_call(draft_id,picks)

    #import players
    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\players_with_adp.csv')
    filtered_players = players[['Name', 'Points', 'Position','ADP']].dropna()

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

    best_roster = draft_buddy(picks,len(my_players)+1,remaining_players,my_roster)
    print(best_roster)
    # call draft buddy



def main():
    return sleeper_draft_buddy('1249429883939979264',9,False)

main()