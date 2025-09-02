import pandas as pd
import os
import copy
from draft_picks import get_picks
from classes import Roster, Player
from scipy.stats import norm

MAX_DEPTH = 7
# FN_CALLS = 0

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
    if pick_round == 1:
        positions = ["RB","WR"]
    else:
        positions = ["QB","RB","WR","TE"]

    for position in positions:
        if roster.can_draft(position):
            best_available = player_df[(player_df['Position'] == position) & ~player_df['Name'].isin(roster.players)].sort_values(by='Points', ascending=False).iloc[0]
            best_available = Player(name=best_available['Name'], pos=best_available['Position'], points=best_available['Points'], pick=cur_pick)
            new_roster = copy.deepcopy(roster)
            new_roster.add_player(best_available)
            new_roster = draft_buddy_abstract(picks,pick_round+1,player_df,new_roster,depth+1)
            if verbose:
                print(f"{best_available.name} is {new_roster.total_points:.2f} and {new_roster.total_PAWS:.2f}")
                # print(new_roster)
            branches.append(new_roster)
    return get_best_roster(branches)


# FN_CALLS_2 = 0
# LOOP_ITER = 0
def calculate_est_val(available_players,cur_pick):
    # global FN_CALLS_2
    # global LOOP_ITER
    # FN_CALLS_2 += 1
    proj_points = 0
    used_prob = 0
    max_found_score,max_found_name = 0, 'Nobody'
    i = 0
    while used_prob < 0.95:
        cur_player = available_players.iloc[i]
        chance_of_getting = 1 - norm.cdf(cur_pick, loc = cur_player['ADP']*.9, scale = cur_player['ADP']/12)
        value_added = cur_player['Points'] * chance_of_getting * (1-used_prob)
        if value_added > max_found_score:
            max_found_score,max_found_name = value_added,cur_player['Name']
        proj_points += value_added
        used_prob += chance_of_getting * (1-used_prob)
        i += 1
    return max_found_name, proj_points / used_prob


player_map = {}

def draft_buddy_abstract(picks,pick_round,player_df,roster,depth):
    # global FN_CALLS 
    # FN_CALLS += 1
    if depth > MAX_DEPTH or pick_round > len(picks):
        return roster
    
    branches = []
    cur_pick = picks[pick_round-1]
    # Need to figure this out
    positions = ["QB","RB","WR","TE"]

    for position in positions:
        if roster.can_draft(position):
            best_available = player_df[(player_df['Position'] == position) & (player_df['ADP'] >= cur_pick*.75) & ~player_df['Name'].isin(roster.players)].sort_values(by='Points', ascending=False)
            key = position + str(cur_pick)
            # Come back to
            if key in player_map and not player_map[key][0] in roster.players:
                [name,projection] = player_map[key]
            else:
                name,projection = calculate_est_val(best_available,cur_pick)
                # player_map[key] = [name,projection]
            best_available = Player(name = name,pos = position,points=projection,pick=cur_pick)
            new_roster = copy.deepcopy(roster)
            new_roster.add_player(best_available)
            new_roster = draft_buddy_abstract(picks,pick_round+1,player_df,new_roster,depth+1)
            branches.append(new_roster)

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