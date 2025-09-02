from sleeperpy import Drafts, User
from draft_picks import get_picks
import pandas as pd
import os

# These numbers pulled manually
baseline = {'QB': 119.1, # 31 QBs, Justin Fields
            'RB': 54.7, # 66 RBs, Emari Demarcado
            'WR': 92.4, # 87 WRs, Tim Patrick
            'TE': 103.6 } # 27 TEs, Dallas Goedert

def sleeper_api_call(draft_id: str):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    new_draft_results = []
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        position = pick['metadata']['position']
        player_id = pick['metadata']['player_id']
        new_draft_results.append([name,position,player_id])

    return new_draft_results

def grade_draft(draft_id,verbose = False):
    player_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\PlayerStats2024.csv')

    filtered_players = player_data[['Player', 'PPR','PosRank','OvRank']].fillna(0)
    filtered_players = filtered_players.set_index('Player')

    beerat_draft = Drafts.get_specific_draft(draft_id)
    player_ids = beerat_draft['draft_order'].keys()
    players_in_order = sleeper_api_call(draft_id)
    draft_values = {}
    for player in player_ids:
        username = User.get_user(player)['username']
        pick = beerat_draft['draft_order'][player]
        if verbose: print(f"\nNew player: {username} picking at {pick}")
        pick = beerat_draft['draft_order'][player]
        player_selections = get_picks(pick,True)
        my_players = []
        for pick in player_selections:
            if pick > len(players_in_order):
                continue
            else:
                my_players.append(players_in_order[pick-1])
        team_surplus = 0
        for player in my_players:
            if player[1] in ['WR','RB','TE','QB']:
                name = player[0]
                their_points = filtered_players.loc[name,'PPR']
                their_surplus = max(0,their_points - baseline[player[1]])
                if verbose: print(f"{name} scored {their_surplus:.2f} surplus Points")
                team_surplus += their_surplus
            else:
                if verbose: print("Kicker or Defense")
        draft_values[username] = team_surplus
        if verbose: print(f'Total Suplus that {username} Drafted = {team_surplus:.2f}')

    df = pd.DataFrame(draft_values.items())
    print(df.sort_values(1,ascending=False).head(16))
    return 'Done'
    

beerat_2024_draft_id = '1126950126565609472'

def main():
    print(grade_draft(beerat_2024_draft_id,True))
main()