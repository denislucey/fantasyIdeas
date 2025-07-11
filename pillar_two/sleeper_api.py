from sleeperpy import Drafts
from draft_picks import get_picks

def sleeper_api_call(draft_id: str, picks):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    new_draft_results = []
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        new_draft_results.append(name)

    return new_draft_results
        



def main():
    draft_id = '1244427804271968256'
    picks = get_picks(1,False)
    taken_players = sleeper_api_call(draft_id, picks)
    my_players = []
    for pick in picks:
        if pick > len(taken_players):
            continue
        else:
            my_players.append(taken_players[pick-1])

    print(my_players)
    return

main()