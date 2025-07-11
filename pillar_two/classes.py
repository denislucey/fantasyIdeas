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