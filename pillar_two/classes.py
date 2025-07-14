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
        self.QBs = []
        self.RBs = []
        self.WRs = []
        self.TEs = []

    def __str__(self):
        roster_str = f"Roster Points: {self.total_points}\n"
        roster_str += f"QBs: {self.print_pos_data('QB')}\n"
        roster_str += f"RBs: {self.print_pos_data('RB')}\n"
        roster_str += f"WRs: {self.print_pos_data('WR')}\n"
        roster_str += f"TEs: {self.print_pos_data('TE')}\n"
        return roster_str
    
    def print_pos_data(self,pos: str):
        new_list = {}
        player_list = []
        if pos == 'QB':
            player_list = self.QBs
        elif pos == 'RB':
            player_list = self.RBs
        elif pos == 'WR':
            player_list = self.WRs
        elif pos == 'TE':
            player_list = self.TEs

        for player in player_list:
            new_list[player.name] = [player.points,player.round]
        return new_list

    def add_player(self, player: Player):
        if player.pos == 'QB':
            self.QBs.append(player)
            if len(self.QBs) <= 1:
                self.total_points += player.points
        elif player.pos == 'WR':
            self.WRs.append(player)
            if len(self.WRs) <= 3:
                self.total_points += player.points
        elif player.pos == 'RB':
            self.RBs.append(player)
            if len(self.RBs) <= 2:
                self.total_points += player.points
        elif player.pos == 'TE':
            self.TEs.append(player)
            if len(self.TEs) <= 2:
                self.total_points += player.points

    def can_draft_QB(self):
        return len(self.QBs) < 2
  
    def can_draft_RB(self):
        return len(self.RBs) < 7

    def can_draft_WR(self):
        return len(self.WRs) < 7

    def can_draft_TE(self):
        return len(self.TEs) < 2

    def get_QB(self):
        qbs = []
        for qb in self.QBs:
            qbs.append(qb.name)
        return qbs
  
    def get_RB(self):
        rbs = []
        for rb in self.RBs:
            rbs.append(rb.name)
        return rbs

    def get_WR(self):
        wrs = []
        for wr in self.WRs:
            wrs.append(wr.name)
        return wrs

    def get_TE(self):
        tes = []
        for te in self.TEs:
            tes.append(te.name)
        return tes

    def remove_player(self, player: Player):
        if player.pos == 'QB':
            for i in range(len(self.QBs)):
                if self.QBs[i].name == player.name:
                    self.total_points -= player.points
                    self.QBs.pop(i)
        elif player.pos == 'RB':
            for i in range(len(self.RBs)):
                if self.RBs[i].name == player.name:
                    self.total_points -= player.points
                    self.RBs.pop(i)
        elif player.pos == 'WR':
            for i in range(len(self.RBs)):
                if self.RBs[i].name == player.name:
                    self.total_points -= player.points
                    self.RBs.pop(i)
        elif player.pos == 'TE':
            for i in range(len(self.TEs)):
                if self.TEs[i].name == player.name:
                    self.total_points -= player.points
                    self.TEs.pop(i)
