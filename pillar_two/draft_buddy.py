import pandas as pd
import os
import copy
from draft_picks import get_picks
from classes import Roster, Player
from scipy.stats import norm

MAX_DEPTH = 7

def draft_buddy_wrapper(pick: int, thr_rr: bool = False):
    #create the data frame
    draft_picks = get_picks(pick,thr_rr)

    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\players_with_adp.csv')
    filtered_players = players[['Name', 'Points', 'Position','ADP']].fillna(500)
    
    return draft_buddy(draft_picks,1,filtered_players,roster=Roster())


#Very first attempt, basic
def draft_buddy(picks, pick_round: int, player_df: pd.DataFrame, roster: Roster):
    
    if pick_round > 7:
        return roster
    
    cur_pick = picks[pick_round-1]
    # Need to figure this out
    if roster.can_draft_QB():
        best_QB = player_df[(player_df['Position'] == 'QB') & (player_df['ADP'] >= cur_pick) & ~player_df['Name'].isin(roster.get_QB())].sort_values(by='Points', ascending=False).iloc[0]
        best_QB = Player(name=best_QB['Name'], pos=best_QB['Position'], points=best_QB['Points'], pick=cur_pick)
        draft_QB_roster = copy.deepcopy(roster)
        draft_QB_roster.add_player(best_QB)
        draft_QB_roster = draft_buddy(picks,pick_round+1,player_df,draft_QB_roster)
    else:
        draft_QB_roster = roster
    
    if roster.can_draft_RB():
        best_RB = player_df[(player_df['Position'] == 'RB') & (player_df['ADP'] >= cur_pick) & ~player_df['Name'].isin(roster.get_RB())].sort_values(by='Points', ascending=False).iloc[0]
        best_RB = Player(name=best_RB['Name'], pos=best_RB['Position'], points=best_RB['Points'], pick=cur_pick)
        draft_RB_roster = copy.deepcopy(roster)
        draft_RB_roster.add_player(best_RB)
        draft_RB_roster = draft_buddy(picks,pick_round+1,player_df,draft_RB_roster)
    else:
        draft_RB_roster = roster
    
    if roster.can_draft_WR():
        best_WR = player_df[(player_df['Position'] == 'WR') & (player_df['ADP'] >= cur_pick) & ~player_df['Name'].isin(roster.get_WR())].sort_values(by='Points', ascending=False).iloc[0]
        best_WR = Player(name=best_WR['Name'], pos=best_WR['Position'], points=best_WR['Points'], pick=cur_pick)
        draft_WR_roster = copy.deepcopy(roster)
        draft_WR_roster.add_player(best_WR)
        draft_WR_roster = draft_buddy(picks,pick_round+1,player_df,draft_WR_roster)
    else:
        draft_WR_roster = roster

    if roster.can_draft_TE():
        best_TE = player_df[(player_df['Position'] == 'TE') & (player_df['ADP'] >= cur_pick) & ~player_df['Name'].isin(roster.get_TE())].sort_values(by='Points', ascending=False).iloc[0]
        best_TE = Player(name=best_TE['Name'], pos=best_TE['Position'], points=best_TE['Points'], pick=cur_pick)
        draft_TE_roster = copy.deepcopy(roster)
        draft_TE_roster.add_player(best_TE)
        draft_TE_roster = draft_buddy(picks,pick_round+1,player_df,draft_TE_roster)
    else:
        draft_TE_roster = roster

    # return the roster with the highest points
    rosters = [draft_QB_roster, draft_RB_roster, draft_WR_roster, draft_TE_roster]
    return get_best_roster(rosters)


# Called when you are on the clock, assumes you can draft any available player
def draft_buddy_selective(picks,pick_round,player_df,roster,depth,verbose):
    if pick_round > len(picks):
        return roster
    
    cur_pick = picks[pick_round-1]

    branches = []

    if roster.can_draft_QB():
        best_QB = player_df[(player_df['Position'] == 'QB') & ~player_df['Name'].isin(roster.get_QB())].sort_values(by='Points', ascending=False).iloc[0]
        best_QB = Player(name=best_QB['Name'], pos=best_QB['Position'], points=best_QB['Points'], pick=cur_pick)
        draft_QB_roster = copy.deepcopy(roster)
        draft_QB_roster.add_player(best_QB)
        draft_QB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_QB_roster,depth + 1)
        if verbose: print(f"{best_QB.name} is {draft_QB_roster.total_points}")
        branches.append(draft_QB_roster)
   
    if roster.can_draft_RB():
        best_RB = player_df[(player_df['Position'] == 'RB') & ~player_df['Name'].isin(roster.get_RB())].sort_values(by='Points', ascending=False).iloc[0]
        best_RB = Player(name=best_RB['Name'], pos=best_RB['Position'], points=best_RB['Points'], pick=cur_pick)
        draft_RB_roster = copy.deepcopy(roster)
        draft_RB_roster.add_player(best_RB)
        draft_RB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_RB_roster,depth + 1)
        if verbose: print(f"{best_RB.name} is {draft_RB_roster.total_points}")
        branches.append(draft_RB_roster)
    
    if roster.can_draft_WR():
        best_WR = player_df[(player_df['Position'] == 'WR') & ~player_df['Name'].isin(roster.get_WR())].sort_values(by='Points', ascending=False).iloc[0]
        best_WR = Player(name=best_WR['Name'], pos=best_WR['Position'], points=best_WR['Points'], pick=cur_pick)
        draft_WR_roster = copy.deepcopy(roster)
        draft_WR_roster.add_player(best_WR)
        draft_WR_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_WR_roster, depth + 1)
        if verbose: print(f"{best_WR.name} is {draft_WR_roster.total_points}")
        branches.append(draft_WR_roster)

    if roster.can_draft_TE():
        best_TE = player_df[(player_df['Position'] == 'TE') & ~player_df['Name'].isin(roster.get_TE())].sort_values(by='Points', ascending=False).iloc[0]
        best_TE = Player(name=best_TE['Name'], pos=best_TE['Position'], points=best_TE['Points'], pick=cur_pick)
        draft_TE_roster = copy.deepcopy(roster)
        draft_TE_roster.add_player(best_TE)
        draft_TE_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_TE_roster,depth + 1)
        if verbose: print(f"{best_TE.name} is {draft_TE_roster.total_points}")
        branches.append(draft_TE_roster)

    return get_best_roster(branches)

def calculate_est_val(available_players,cur_pick):
    proj_points = 0
    used_prob = 0
    max_found_score,max_found_name = 0, 'Nobody'
    i = 0
    while used_prob < 0.95:
        cur_player = available_players.iloc[i]
        chance_of_getting = 1 - norm.cdf(cur_pick, loc = cur_player['ADP'], scale = cur_player['ADP']/15)
        value_added = cur_player['Points'] * chance_of_getting * (1-used_prob)
        if value_added > max_found_score:
            max_found_score,max_found_name = value_added,cur_player['Name']
        proj_points += value_added
        used_prob += chance_of_getting * (1-used_prob)
        i += 1
    return max_found_name, proj_points / used_prob


player_map = {}

def draft_buddy_abstract(picks,pick_round,player_df,roster,depth):
    
    if depth > MAX_DEPTH or pick_round > len(picks):
        return roster
    
    branches = []
    cur_pick = picks[pick_round-1]
    # Need to figure this out
    if roster.can_draft_QB():
        best_available_QBs = player_df[(player_df['Position'] == 'QB') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_QB())].sort_values(by='Points', ascending=False)
        key = "QB" + str(cur_pick)
        if key in player_map and (player_map[key][0] not in roster.get_QB()):
            [QB_name,best_QB] = player_map[key]
        else:
            QB_name,best_QB = calculate_est_val(best_available_QBs,cur_pick)
            # player_map[key] = [QB_name,best_QB]
        best_QB = Player(name=QB_name, pos='QB', points=best_QB, pick=cur_pick)
        draft_QB_roster = copy.deepcopy(roster)
        draft_QB_roster.add_player(best_QB)
        draft_QB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_QB_roster,depth+1)
        branches.append(draft_QB_roster)
    
    if roster.can_draft_RB():
        best_available_RBs = player_df[(player_df['Position'] == 'RB') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_RB())].sort_values(by='Points', ascending=False)
        key = "RB" + str(cur_pick)
        if key in player_map:
            best_RB = player_map[key]
        else:
            RB_name,best_RB = calculate_est_val(best_available_RBs,cur_pick)
            best_RB = Player(name=RB_name, pos='RB', points=best_RB, pick=cur_pick)
            # player_map[key] = best_RB
        draft_RB_roster = copy.deepcopy(roster)
        draft_RB_roster.add_player(best_RB)
        draft_RB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_RB_roster,depth+1)
        branches.append(draft_RB_roster)
    
    if roster.can_draft_WR():
        best_available_WRs = player_df[(player_df['Position'] == 'WR') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_WR())].sort_values(by='Points', ascending=False)
        key = "WR" + str(cur_pick)
        if key in player_map:
            WR_name,best_WR = player_map[key]
        else:
            WR_name,best_WR = calculate_est_val(best_available_WRs,cur_pick)
            # player_map[key] = (WR_name,best_WR)
        best_WR = Player(name=WR_name, pos='WR', points=best_WR, pick=cur_pick)
        draft_WR_roster = copy.deepcopy(roster)
        draft_WR_roster.add_player(best_WR)
        draft_WR_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_WR_roster,depth+1)
        branches.append(draft_WR_roster)

    if roster.can_draft_TE():
        best_available_TEs = player_df[(player_df['Position'] == 'TE') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_TE())].sort_values(by='Points', ascending=False)
        key = "TE" + str(cur_pick)
        if key in player_map:
            TE_name,best_TE = player_map[key]
        else:
            TE_name,best_TE = calculate_est_val(best_available_TEs,cur_pick)
            # player_map[key] = (TE_name,best_TE)
        best_TE = Player(name=TE_name, pos='TE', points=best_TE, pick=cur_pick)
        draft_TE_roster = copy.deepcopy(roster)
        draft_TE_roster.add_player(best_TE)
        draft_TE_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_TE_roster,depth+1)
        branches.append(draft_TE_roster)

    return get_best_roster(branches)

def get_best_roster(rosters):
    return max(rosters, key=lambda r: r.total_points + r.total_PAWS)

def main():
    for i in range(1,17):
        print(f"Pick: {i}")
        print(f"Score: {draft_buddy_wrapper(pick=i,thr_rr=False)}")
    # best_roster = draft_buddy_wrapper(pick=16,thr_rr=False)
    # print(best_roster)


# main()