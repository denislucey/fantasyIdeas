from sleeperpy import Drafts, User
import requests

# '1043464076963241984'
def main():
    xavier_id = '1128414458344292352'
    meech_id = '1043464076963241984'
    denis_drafts = Drafts.get_all_drafts_for_user(xavier_id,"nfl",2025)
    print("here")
    # for draft in denis_drafts:
        # print(draft)
    draft_id = '1256103882887532544'
    meech_invitational = Drafts.get_specific_draft('1256103882887532544')
    meech_picks = [5,20,29,44,53,68,77,92,101,116,125,140,149,164,173,188]
    xavier_picks = [6,19,30,43,54,67,78,91,102,115,126,139,150,163,174,187]
    

    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    taken_players = []
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        taken_players.append(name)

    my_players = []
    for pick in meech_picks:
        if pick > len(taken_players):
            continue
        else:
            my_players.append(taken_players[pick-1])

    print(my_players)
    print("Done")

def get_users_drafts():
    ksda_id = '1251178368452284416'
    beerat_id = '1253495736151052288'
    beerat_draft = Drafts.get_specific_draft(beerat_id)
    player_ids = beerat_draft['draft_order'].keys()

    for player in beerat_draft['draft_order'].keys():
        print("New player: " + User.get_user(player)['username'])
        # their_drafts = Drafts.get_all_drafts_for_user(player,"nfl",2023)
        # for draft in their_drafts:
        #     print(draft['metadata']['name'] + ' ' + draft['status'] + ' ' + draft['draft_id'] + ' league id: ' + draft['league_id'])

        for i in [2025]:
            their_drafts = Drafts.get_all_drafts_for_user(player,"nfl",i)
            print(i)
            for dr in their_drafts:
                # all_drafts = Drafts.get_all_drafts_for_league(dr['league_id'])
                print(dr['metadata']['name'] + ' ' + dr['status'] + ' ' + dr['draft_id'] + ' league id: ' + dr['league_id'])
    print("here")

get_users_drafts()
# main()