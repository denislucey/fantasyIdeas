from sleeperpy import Leagues,User
import requests

ksda_dynasty_id = '1251178367256907776'
ksda_draft_id = '1251178368452284416'

def main():
    league = Leagues.get_rosters(ksda_dynasty_id)
    roster_id_to_owner_id_map = {}
    for roster in league:
        roster_id_to_owner_id_map[roster['roster_id']] = User.get_user(roster['owner_id'])['username']

    matchups = Leagues.get_matchups(ksda_dynasty_id,1)
    player_projections = test_stats_api("https://api.sleeper.app/v1/projections/nfl/regular/2025/1")
    team_proj = 0
    denis_team = matchups[0]
    for player in denis_team['starters']:
        team_proj += player_projections[player]['pts_ppr']
        print(player_projections[player]['pts_ppr'])
    print(team_proj)
    # print(matchups)
    print('Done')

def test_stats_api(url):
    result_json_string = requests.get(url)
    try:
        result_json_string.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e
        #return SleeperWrapperException("Empty value returned")

    result = result_json_string.json()
    return result


# print(test_stats_api("https://api.sleeper.app/v1/projections/nfl/regular/2025/1"))

main()

