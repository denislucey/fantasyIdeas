from sleeperpy import Drafts

def sleeper_api_call(draft_id: str, picks):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    return draft_results[picks[0]-1]['metadata']['last_name']


def main():
    draft_id = '1244427804271968256'
    picks = [5, 28, 37, 60, 69, 92, 101]
    print(sleeper_api_call(draft_id, picks))
    return

main()