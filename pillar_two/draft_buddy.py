import pandas as pd
import os
import copy
from draft_picks import get_picks
from classes import Roster, Player
from scipy.stats import norm

def draft_buddy_wrapper(pick: int, thr_rr: bool = False):
    #create the data frame
    draft_picks = get_picks(pick,thr_rr)

    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\players_with_adp.csv')
    filtered_players = players[['Name', 'Points', 'Position','ADP']].fillna(500)
    
    return draft_buddy(draft_picks,1,filtered_players,roster=Roster())

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
    best_roster = max(rosters, key=lambda r: r.total_points)
    return best_roster


# Called when you are on the clock, assumes you can draft any available player
def draft_buddy_selective(picks,pick_round,player_df,roster):
    if pick_round > 7:
        return roster
    
    cur_pick = picks[pick_round-1]

    branches = []
    # Need to figure this out
    if roster.can_draft_QB():
        best_QB = player_df[(player_df['Position'] == 'QB') & ~player_df['Name'].isin(roster.get_QB())].sort_values(by='Points', ascending=False).iloc[0]
        best_QB = Player(name=best_QB['Name'], pos=best_QB['Position'], points=best_QB['Points'], pick=cur_pick)
        draft_QB_roster = copy.deepcopy(roster)
        draft_QB_roster.add_player(best_QB)
        draft_QB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_QB_roster)
        branches.append(draft_QB_roster)

        # best_last_chance_QB = player_df[(player_df['Position'] == 'QB') & ~player_df['Name'].isin(roster.get_QB()) & (player_df['ADP'] <= picks[pick_round])].sort_values(by='Points', ascending=False).iloc[0]
        # if best_last_chance_QB['Name'] != best_QB.name:
        #     best_last_chance_QB = Player(name=best_last_chance_QB['Name'], pos='QB', points=best_last_chance_QB['Points'], pick=cur_pick)
        #     draft_last_chance_QB_roster = copy.deepcopy(roster)
        #     draft_last_chance_QB_roster.add_player(best_QB)
        #     draft_last_chance_QB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_last_chance_QB_roster)
        #     branches.append(draft_last_chance_QB_roster)
    
    if roster.can_draft_RB():
        best_RB = player_df[(player_df['Position'] == 'RB') & ~player_df['Name'].isin(roster.get_RB())].sort_values(by='Points', ascending=False).iloc[0]
        best_RB = Player(name=best_RB['Name'], pos=best_RB['Position'], points=best_RB['Points'], pick=cur_pick)
        draft_RB_roster = copy.deepcopy(roster)
        draft_RB_roster.add_player(best_RB)
        draft_RB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_RB_roster)
        branches.append(draft_RB_roster)

        # best_last_chance_RB = player_df[(player_df['Position'] == 'RB') & ~player_df['Name'].isin(roster.get_RB()) & (player_df['ADP'] <= picks[pick_round])].sort_values(by='Points', ascending=False).iloc[0]
        # if best_last_chance_RB['Name'] != best_RB.name:
        #     best_last_chance_RB = Player(name=best_last_chance_RB['Name'], pos='RB', points=best_last_chance_RB['Points'], pick=cur_pick)
        #     draft_last_chance_RB_roster = copy.deepcopy(roster)
        #     draft_last_chance_RB_roster.add_player(best_RB)
        #     draft_last_chance_RB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_last_chance_RB_roster)
        #     branches.append(draft_last_chance_RB_roster)
    
    if roster.can_draft_WR():
        best_WR = player_df[(player_df['Position'] == 'WR') & ~player_df['Name'].isin(roster.get_WR())].sort_values(by='Points', ascending=False).iloc[0]
        best_WR = Player(name=best_WR['Name'], pos=best_WR['Position'], points=best_WR['Points'], pick=cur_pick)
        draft_WR_roster = copy.deepcopy(roster)
        draft_WR_roster.add_player(best_WR)
        draft_WR_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_WR_roster)
        branches.append(draft_WR_roster)

        # best_last_chance_WR = player_df[(player_df['Position'] == 'WR') & ~player_df['Name'].isin(roster.get_WR()) & (player_df['ADP'] <= picks[pick_round])].sort_values(by='Points', ascending=False).iloc[0]
        # if best_last_chance_WR['Name'] != best_WR.name:
        #     best_last_chance_WR = Player(name=best_last_chance_WR['Name'], pos='WR', points=best_last_chance_WR['Points'], pick=cur_pick)
        #     draft_last_chance_WR_roster = copy.deepcopy(roster)
        #     draft_last_chance_WR_roster.add_player(best_WR)
        #     draft_last_chance_WR_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_last_chance_WR_roster)
        #     branches.append(draft_last_chance_WR_roster)

    if roster.can_draft_TE():
        best_TE = player_df[(player_df['Position'] == 'TE') & ~player_df['Name'].isin(roster.get_TE())].sort_values(by='Points', ascending=False).iloc[0]
        best_TE = Player(name=best_TE['Name'], pos=best_TE['Position'], points=best_TE['Points'], pick=cur_pick)
        draft_TE_roster = copy.deepcopy(roster)
        draft_TE_roster.add_player(best_TE)
        draft_TE_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_TE_roster)
        branches.append(draft_TE_roster)

        # best_last_chance_TE = player_df[(player_df['Position'] == 'TE') & ~player_df['Name'].isin(roster.get_TE()) & (player_df['ADP'] <= picks[pick_round])].sort_values(by='Points', ascending=False).iloc[0]
        # if best_last_chance_TE['Name'] != best_TE.name:
        #     best_last_chance_TE = Player(name=best_last_chance_TE['Name'], pos='TE', points=best_last_chance_TE['Points'], pick=cur_pick)
        #     draft_last_chance_TE_roster = copy.deepcopy(roster)
        #     draft_last_chance_TE_roster.add_player(best_TE)
        #     draft_last_chance_TE_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_last_chance_TE_roster)
        #     branches.append(draft_last_chance_TE_roster)

    # return the roster with the highest points
    best_roster = max(branches, key=lambda r: r.total_points)
    return best_roster

def calculate_est_val(available_players,cur_pick):
    proj_points = 0
    used_prob = 0
    max_found_score,max_found_name = 0, 'Nobody'
    i = 0
    while used_prob < 0.95:
        cur_player = available_players.iloc[i]
        chance_of_getting = 1 - norm.cdf(cur_pick-1, loc = cur_player['ADP'], scale = cur_player['ADP']/15)
        
        # Think of a better solution
        
        value_added = cur_player['Points'] * chance_of_getting * (1-used_prob)
        if value_added > max_found_score:
            max_found_score,max_found_name = value_added,cur_player['Name']
        proj_points += value_added
        used_prob += chance_of_getting * (1-used_prob)
        i += 1
    return max_found_name, proj_points / used_prob


def draft_buddy_abstract(picks,pick_round,player_df,roster):
    
    if pick_round > 7:
        return roster
    
    cur_pick = picks[pick_round-1]
    # Need to figure this out
    if roster.can_draft_QB():
        best_available_QBs = player_df[(player_df['Position'] == 'QB') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_QB())].sort_values(by='Points', ascending=False)
        QB_name,best_QB = calculate_est_val(best_available_QBs,cur_pick)
        best_QB = Player(name=QB_name, pos='QB', points=best_QB, pick=cur_pick)
        draft_QB_roster = copy.deepcopy(roster)
        draft_QB_roster.add_player(best_QB)
        draft_QB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_QB_roster)
    else:
        draft_QB_roster = roster
    
    if roster.can_draft_RB():
        best_available_RBs = player_df[(player_df['Position'] == 'RB') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_RB())].sort_values(by='Points', ascending=False)
        RB_name,best_RB = calculate_est_val(best_available_RBs,cur_pick)
        best_RB = Player(name=RB_name, pos='RB', points=best_RB, pick=cur_pick)
        draft_RB_roster = copy.deepcopy(roster)
        draft_RB_roster.add_player(best_RB)
        draft_RB_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_RB_roster)
    else:
        draft_RB_roster = roster
    
    if roster.can_draft_WR():
        best_available_WRs = player_df[(player_df['Position'] == 'WR') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_WR())].sort_values(by='Points', ascending=False)
        WR_name,best_WR = calculate_est_val(best_available_WRs,cur_pick)
        best_WR = Player(name=WR_name, pos='WR', points=best_WR, pick=cur_pick)
        draft_WR_roster = copy.deepcopy(roster)
        draft_WR_roster.add_player(best_WR)
        draft_WR_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_WR_roster)
    else:
        draft_WR_roster = roster

    if roster.can_draft_TE():
        best_available_TEs = player_df[(player_df['Position'] == 'TE') & (player_df['ADP'] >= cur_pick*.7) & ~player_df['Name'].isin(roster.get_TE())].sort_values(by='Points', ascending=False)
        TE_name,best_TE = calculate_est_val(best_available_TEs,cur_pick)
        best_TE = Player(name=TE_name, pos='TE', points=best_TE, pick=cur_pick)
        draft_TE_roster = copy.deepcopy(roster)
        draft_TE_roster.add_player(best_TE)
        draft_TE_roster = draft_buddy_abstract(picks,pick_round+1,player_df,draft_TE_roster)
    else:
        draft_TE_roster = roster

    # return the roster with the highest points
    rosters = [draft_QB_roster, draft_RB_roster, draft_WR_roster, draft_TE_roster]
    best_roster = max(rosters, key=lambda r: r.total_points)
    return best_roster

def main():
    for i in range(1,17):
        print(f"Pick: {i}")
        print(f"Score: {draft_buddy_wrapper(pick=i,thr_rr=False)}")
    # best_roster = draft_buddy_wrapper(pick=16,thr_rr=False)
    # print(best_roster)


# main()