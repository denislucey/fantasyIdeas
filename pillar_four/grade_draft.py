from sleeperpy import Drafts, User
from draft_picks import get_picks
import pandas as pd
import os

# These numbers pulled manually
baseline_2024 = {'QB': 119.1, # 31 QBs, Justin Fields
            'RB': 54.7, # 66 RBs, Emari Demarcado
            'WR': 92.4, # 87 WRs, Tim Patrick
            'TE': 103.6 } # 27 TEs, Dallas Goedert

baseline_2025 = {'QB': 33.1,#28 
                 'RB': 3.9,#72,
                 'WR': 12.7,#82, 
                 'TE': 15.3,#27, 
                 'K': 0,#14, 
                 'DEF': 0 #17
                 }

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

def add_new_player(roster,position,points,name):
    potential_add = [name,points]
    if position == 'QB' and roster['QB'][1] < points:
        roster['QB'] = potential_add
    elif position == 'RB':
        if points > roster['RB1'][1]:
            potential_flex = roster['RB2']
            roster['RB2'] = roster['RB1']
            roster['RB1'] = potential_add
            if potential_flex[1] > roster['FLEX'][1]: roster['FLEX'] = potential_flex
        elif points > roster['RB2'][1]:
            potential_flex = roster['RB2']
            roster['RB2'] = potential_add
            if potential_flex[1] > roster['FLEX'][1]: roster['FLEX'] = potential_flex
        elif points > roster['FLEX'][1]: roster['FLEX'] = potential_add
    elif position == 'WR':
        if points > roster['WR1'][1]:
            potential_flex = roster['WR2']
            roster['WR2'] = roster['WR1']
            roster['WR1'] = potential_add
            if potential_flex[1] > roster['FLEX'][1]: roster['FLEX'] = potential_flex
        elif points > roster['WR2'][1]:
            potential_flex = roster['WR2']
            roster['WR2'] = potential_add
            if potential_flex[1] > roster['FLEX'][1]: roster['FLEX'] = potential_flex
        elif points > roster['FLEX'][1]: roster['FLEX'] = potential_add
    elif position == 'TE':
        if points > roster['TE'][1]:
            potential_flex = roster['TE']
            roster['TE'] = potential_add
            if potential_flex[1] > roster['FLEX'][1]: roster['FLEX'] = potential_flex
        elif points > roster['FLEX'][1]: roster['FLEX'] = potential_add
    return roster

def grade_draft(draft_id,verbose = False,starters_only = False, use_surplus = True,year=2024):
    player_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + f'\\PlayerStats{year}.csv')

    filtered_players = player_data[['Player', 'PPR','PosRank','OvRank']].fillna(0)

    player_map = {
        "Brian Robinson Jr.": "Brian Robinson",
        "D.J. Moore": "DJ Moore",
        "Tre Harris": "Tre' Harris",
        "Kenneth Walker III": "Kenneth Walker",
        "Calvin Austin III": "Calvin Austin",
        "Marquise Brown": "Hollywood Brown",
        "D.K. Metcalf": "DK Metcalf",
        "Michael Pittman Jr.": "Michael Pittman",
        "Tyrone Tracy Jr.": "Tyrone Tracy",
        "Josh Palmer": "Joshua Palmer",
        "Demario Douglas": "DeMario Douglas",
        "Marvin Harrison Jr.": "Marvin Harrison",
        "Chigoziem Okonkwo": "Chig Okonkwo"
    }

    filtered_players['Player'] = filtered_players['Player'].map(player_map).fillna(filtered_players['Player'])
    filtered_players = filtered_players.set_index('Player')


    if year == 2024: baseline = baseline_2024 
    else: baseline = baseline_2025

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
        # QB, RB1, RB2, WR1, WR2, TE, Flex
        best_starters = {
            'QB':["Fake Player",0],
            'RB1':["Fake Player",0],
            'RB2':["Fake Player",0],
            'WR1':["Fake Player",0],
            'WR2':["Fake Player",0],
            'TE':["Fake Player",0],
            'FLEX':["Fake Player",0]
        }
        for player in my_players:
            if player[1] in ['WR','RB','TE','QB']:
                name = player[0]
                try:
                    their_points = filtered_players.loc[name,'PPR']
                except KeyError:
                    print(name)
                    their_points = 0
                if starters_only:
                    best_starters = add_new_player(best_starters,player[1],their_points,name)
                else:
                    if use_surplus:
                        their_surplus = max(0,their_points - baseline[player[1]])
                        if verbose: print(f"{name} scored {their_surplus:.2f} surplus Points")
                    else:
                        their_surplus = their_points
                        if verbose: print(f"{name} scored {their_surplus:.2f} Points")
                    team_surplus += their_surplus
            else:
                if verbose and not starters_only: print("Kicker or Defense")
        if starters_only:
            for player in best_starters.keys():
                team_surplus += best_starters[player][1]
                if verbose: print(f"{player}: {best_starters[player][0]} scored {best_starters[player][1]}")
        draft_values[username] = team_surplus
        if verbose: print(f'Total Surplus that {username} Drafted = {team_surplus:.2f}')

    df = pd.DataFrame(draft_values.items())
    print(df.sort_values(1,ascending=False).head(16))
    return 'Done'
    

beerat_2024_draft_id = '1126950126565609472'
beerat_2025_draft_id = '1253495736151052288'

def main():
    print(grade_draft(beerat_2025_draft_id,
                      verbose = True,
                      starters_only = False,
                      use_surplus = True,
                      year=2025))
main()