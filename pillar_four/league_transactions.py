from sleeperpy import Leagues,Drafts,User
from get_players_sleeper_api import get_sleeper_draft_and_write_to_csv_file

league_id_2024 = '1126950126012014592'
draft_id = '1126950126565609472'

def main():
    league = Leagues.get_rosters(league_id_2024)
    roster_id_to_owner_id_map = {}
    for roster in league:
        roster_id_to_owner_id_map[roster['roster_id']] = roster['owner_id']
    player_map = get_sleeper_draft_and_write_to_csv_file(False)

    beerat_draft = Drafts.get_specific_draft(draft_id)
    player_ids = beerat_draft['draft_order'].keys()
    id_mapping = {}
    for id_num in player_ids:
        id_mapping[id_num] = User.get_user(id_num)['username']
    
    for i in range(1,17):
        print(f"---Week {i}---")
        week_x_transactions = Leagues.get_transactions(league_id_2024,i)
        for transaction in week_x_transactions:
            if transaction['type'] == 'trade':
                print("-New Trade-")
                players_added = transaction['adds']
                for player in players_added.keys():
                    receiving_team = players_added[player]
                    name = player_map.loc[player,'full_name']
                    print(f"{name} to {id_mapping[roster_id_to_owner_id_map[receiving_team]]}")


main()