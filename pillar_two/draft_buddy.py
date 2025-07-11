import pandas as pd
import os
import copy

from draft_picks import three_rr, no_three_rr

# NEED TO ADD PLAYERS AS A DF
# NEED TO ADD logic to parse the best players from a df

class Player:
    """Represents a player"""
    def __init__(self, name: str, pos: str, points: float, pick: int):
        self.name = name
        self.pos = pos
        self.points = points
        self.round = (pick-1) // 16 + 1
        self.pick = pick

class Roster:
    """Represents a team"""
    def __init__(self):
        self.total_points = 0
        self.QB = None
        self.RB1 = None
        self.RB2 = None
        self.WR1 = None
        self.WR2 = None
        self.TE = None
        self.FLEX = None

    def __str__(self):
        roster_str = f"Roster Points: {self.total_points}\n"
        roster_str += f"QB: {self.QB.name if self.QB else 'None'} {self.QB.round if self.QB else 'None'}\n"
        roster_str += f"RB1: {self.RB1.name if self.RB1 else 'None'} {self.RB1.round if self.RB1 else 'None'}\n"
        roster_str += f"RB2: {self.RB2.name if self.RB2 else 'None'} {self.RB2.round if self.RB2 else 'None'}\n"
        roster_str += f"WR1: {self.WR1.name if self.WR1 else 'None'} {self.WR1.round if self.WR1 else 'None'}\n"
        roster_str += f"WR2: {self.WR2.name if self.WR2 else 'None'} {self.WR2.round if self.WR2 else 'None'}\n"
        roster_str += f"TE: {self.TE.name if self.TE else 'None'} {self.TE.round if self.TE else 'None'}\n"
        roster_str += f"FLEX: {self.FLEX.name if self.FLEX else 'None'} {self.FLEX.round if self.FLEX else 'None'}\n"
        return roster_str

    def add_player(self, player: Player):
        if player.pos == 'QB' and self.QB is None:
            self.QB = player
        elif player.pos == 'RB':
            if self.RB1 is None:
                self.RB1 = player
            elif self.RB2 is None:
                self.RB2 = player
            elif self.FLEX is None:
                self.FLEX = player
        elif player.pos == 'WR':
            if self.WR1 is None:
                self.WR1 = player
            elif self.WR2 is None:
                self.WR2 = player
            elif self.FLEX is None:
                self.FLEX = player
        elif player.pos == 'TE':
            if self.TE is None:
                self.TE = player
            elif self.FLEX is None:
                self.FLEX = player
        self.total_points += player.points

    def can_draft_QB(self):
        return self.QB is None
    
    def can_draft_RB(self):
        return self.RB1 is None or self.RB2 is None or self.FLEX is None

    def can_draft_WR(self):
        return self.WR1 is None or self.WR2 is None or self.FLEX is None

    def can_draft_TE(self):
        return self.TE is None or self.FLEX is None
    
    def get_QB(self):
        qbs = []
        if self.QB:
            qbs.append(self.QB.name)
        return qbs
        
    def get_RB(self):
        rbs = []
        if self.RB1:
            rbs.append(self.RB1.name)
        if self.RB2:
            rbs.append(self.RB2.name)
        if self.FLEX and self.FLEX.pos == 'RB':
            rbs.append(self.FLEX.name)
        return rbs
    
    def get_WR(self):
        wrs = []
        if self.WR1:
            wrs.append(self.WR1.name)
        if self.WR2:
            wrs.append(self.WR2.name)
        if self.FLEX and self.FLEX.pos == 'WR':
            wrs.append(self.FLEX.name)
        return wrs
    
    def get_TE(self):
        tes = []
        if self.TE:
            tes.append(self.TE.name)
        if self.FLEX and self.FLEX.pos == 'TE':
            tes.append(self.FLEX.name)
        return tes
    
    def remove_player(self, player: Player):
        if player.pos == 'QB' and self.QB == player:
            self.total_points -= player.points
            self.QB = None
        elif player.pos == 'RB':
            if self.RB1 == player:
                self.total_points -= player.points
                self.RB1 = None
            elif self.RB2 == player:
                self.total_points -= player.points
                self.RB2 = None
            elif self.FLEX == player:
                self.total_points -= player.points
                self.FLEX = None
        elif player.pos == 'WR':
            if self.WR1 == player:
                self.total_points -= player.points
                self.WR1 = None
            elif self.WR2 == player:
                self.total_points -= player.points
                self.WR2 = None
            elif self.FLEX == player:
                self.total_points -= player.points
                self.FLEX = None
        elif player.pos == 'TE':
            if self.TE == player:
                self.total_points -= player.points
                self.TE = None
            elif self.FLEX == player:
                self.total_points -= player.points
                self.FLEX = None


def draft_buddy_wrapper(pick: int, three_rr: bool = False):
    #create the data frame
    if three_rr:
        draft_picks = three_rr[pick]
    else:
        draft_picks = no_three_rr[pick]

    players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\players_with_adp.csv')
    filtered_players = players[['Name', 'Points', 'Position','ADP']].dropna()
    # print(filtered_players.head(10))
    # create the array of draft picks
    # draft_picks = [8,25,40,57,72,89,104]
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
    best_roster = draft_buddy_wrapper(pick=3,three_rr=False)
    print(best_roster)


main()