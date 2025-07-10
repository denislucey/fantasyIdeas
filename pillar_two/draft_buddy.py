import pandas as pd


# NEED TO ADD PLAYERS AS A DF
# NEED TO ADD logic to parse the best players from a df

class Player:
    def __init__(self, name: str, pos: str, points: float, pick: int):
        self.name = name
        self.pos = pos
        self.points = points
        self.round = pick // 16 + 1
        self.pick = pick

class Roster:
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
        roster_str += f"QB: {self.QB.name if self.QB else 'None'}\n"
        roster_str += f"RB1: {self.RB1.name if self.RB1 else 'None'}\n"
        roster_str += f"RB2: {self.RB2.name if self.RB2 else 'None'}\n"
        roster_str += f"WR1: {self.WR1.name if self.WR1 else 'None'}\n"
        roster_str += f"WR2: {self.WR2.name if self.WR2 else 'None'}\n"
        roster_str += f"TE: {self.TE.name if self.TE else 'None'}\n"
        roster_str += f"FLEX: {self.FLEX.name if self.FLEX else 'None'}\n"
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


def draft_buddy_wrapper(pick: int, three_rr: bool = False):
    #create the data frame
    if three_rr:
        pick += 1

    # create the array of draft picks
    draft_picks = [8,25,40,57,72,98,104]
    return draft_buddy(draft_picks,1,players,roster=Roster())

def draft_buddy(picks, pick_round: int, player_df: pd.DataFrame, roster: Roster):
    
    if pick_round > 7:
        return roster
    
    cur_pick = picks[pick_round-1]

    # Need to figure this out
    if roster.can_draft_QB():
        draft_QB_roster = draft_buddy(picks,pick_round+1,player_df,roster.add_player(best_QB))
        roster.remove_player(best_QB)
    else:
        draft_QB_roster = roster
    
    if roster.can_draft_RB():
        draft_RB_roster = draft_buddy(picks,pick_round+1,player_df,roster.add_player(best_RB))
        roster.remove_player(best_RB)
    else:
        draft_RB_roster = roster
    
    if roster.can_draft_WR():
        draft_WR_roster = draft_buddy(picks,pick_round+1,player_df,roster.add_player(best_WR))
        roster.remove_player(best_WR)
    else:
        draft_WR_roster = roster

    if roster.can_draft_TE():
        draft_TE_roster = draft_buddy(picks,pick_round+1,player_df,roster.add_player(best_TE))
        roster.remove_player(best_TE)
    else:
        draft_TE_roster = roster

    # return the roster with the highest points
    rosters = [draft_QB_roster, draft_RB_roster, draft_WR_roster, draft_TE_roster]
    best_roster = max(rosters, key=lambda r: r.total_points)
    return best_roster

def main():
    draft_buddy_wrapper(pick=1,three_rr=False)