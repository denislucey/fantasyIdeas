import pandas as pd
import os


# Initial mem: 692653
all_players = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\sheet_8_25.csv')

RB_worst_starter = all_players[all_players['Position'] == 'RB'].sort_values(by='Proj Points', ascending=False).iloc[31]['Proj Points']
QB_worst_starter = all_players[all_players['Position'] == 'QB'].sort_values(by='Proj Points', ascending=False).iloc[15]['Proj Points']
WR_worst_starter = all_players[all_players['Position'] == 'WR'].sort_values(by='Proj Points', ascending=False).iloc[47]['Proj Points']
TE_worst_starter = all_players[all_players['Position'] == 'TE'].sort_values(by='Proj Points', ascending=False).iloc[15]['Proj Points']




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
        self.starters = []
        self.players = []
        self.total_PAWS = 0
        self.QBs = []
        self.RBs = []
        self.WRs = []
        self.TEs = []

    def __str__(self):
        roster_str = f"Roster Points: {self.total_points}\n"
        roster_str += f"PAWS: {self.total_PAWS}\n"
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
            self.total_PAWS += (player.points - QB_worst_starter)
            if len(self.QBs) <= 1:
                self.total_points += player.points
                self.starters.append(player.name)
        elif player.pos == 'WR':
            self.WRs.append(player)
            self.total_PAWS += (player.points - WR_worst_starter)
            if len(self.WRs) <= 3:
                self.total_points += player.points
                self.starters.append(player.name)
        elif player.pos == 'RB':
            self.RBs.append(player)
            self.total_PAWS += (player.points - RB_worst_starter)
            if len(self.RBs) <= 3:
                self.total_points += player.points
                self.starters.append(player.name)
        elif player.pos == 'TE':
            self.TEs.append(player)
            self.total_PAWS += (player.points - TE_worst_starter)
            if len(self.TEs) <= 1:
                self.total_points += player.points
                self.starters.append(player.name)

        self.players.append(player.name)

    def can_draft(self,position):
        if position == "QB":
            return len(self.QBs) < 2
        elif position == "RB":
            return len(self.RBs) < 10
        elif position == "WR":
            return len(self.WRs) < 10
        elif position == "TE":
            return len(self.TEs) < 2
        else:
            return False

    def can_draft_QB(self):
        return len(self.QBs) < 2
  
    def can_draft_RB(self):
        return len(self.RBs) < 10

    def can_draft_WR(self):
        return len(self.WRs) < 10

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
                    self.total_PAWS -= (player.points - QB_worst_starter)
                    self.QBs.pop(i)
        elif player.pos == 'RB':
            for i in range(len(self.RBs)):
                if self.RBs[i].name == player.name:
                    self.total_PAWS += (player.points - RB_worst_starter)
                    self.total_points -= player.points
                    self.RBs.pop(i)
        elif player.pos == 'WR':
            for i in range(len(self.WRs)):
                if self.WRs[i].name == player.name:
                    self.total_PAWS += (player.points - WR_worst_starter)
                    self.total_points -= player.points
                    self.WRs.pop(i)
        elif player.pos == 'TE':
            for i in range(len(self.TEs)):
                if self.TEs[i].name == player.name:
                    self.total_PAWS += (player.points - TE_worst_starter)
                    self.total_points -= player.points
                    self.TEs.pop(i)
        
        self.starters.remove(player.name)
        if player.name in self.starters:
            self.total_points -= player.points
            self.starters.remove(player.name)
