import pandas as pd
import os
import copy
from draft_picks import get_picks
from classes import Roster, Player

def draft_buddy_wrapper(pick: int, thr_rr: bool = False):
    #create the data frame
    draft_picks = get_picks(pick,thr_rr)

    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\players_with_adp.csv')
    filtered_players = players[['Name', 'Points', 'Position','ADP']].dropna()
    
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

def main():
    # for i in range(1,17):
        # print(f"Pick: {i}")
        # print(f"Score: {draft_buddy_wrapper(pick=i,thr_rr=True)}")
    best_roster = draft_buddy_wrapper(pick=11,thr_rr=False)
    print(best_roster)


# main()