from sleeperpy import Drafts
import pandas as pd
import os
import matplotlib.pyplot as plt

def sleeper_api_call(draft_id: str):
    draft_results = Drafts.get_all_picks_in_draft(draft_id)
    # return draft_results

    new_draft_results = []
    i = 1
    for pick in draft_results:
        name = pick['metadata']['first_name'] + ' ' + pick['metadata']['last_name']
        position = pick['metadata']['position']
        player_id = pick['metadata']['player_id']
        new_draft_results.append([name,position,player_id,i])
        i += 1

    return new_draft_results

baseline = {'QB': 119.1, # 31 QBs, Justin Fields
            'RB': 54.7, # 66 RBs, Emari Demarcado
            'WR': 92.4, # 87 WRs, Tim Patrick
            'TE': 103.6 } # 27 TEs, Dallas Goedert

beerat_2024_draft_id = '1126950126565609472'

def main():
    player_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '\\PlayerStats2024.csv')

    filtered_players = player_data[['Player', 'PPR','PosRank','OvRank']].fillna(0)
    filtered_players = filtered_players.set_index('Player')

    draft_order = sleeper_api_call(beerat_2024_draft_id)
    pick_df = pd.DataFrame(draft_order,columns=['Name','Position','ID','Pick'])
    pick_df = pick_df.join(filtered_players,on='Name',how='left')
    pick_df['Surplus Value'] = pick_df.apply(lambda x: generate_replacement_level(x['PPR'], x['Position']), axis=1)
    pick_df.plot(x='Pick',y='Surplus Value')
    plt.show()
    print(draft_order)

def generate_replacement_level(score,position):
    if position in ['QB','RB','WR','TE']:
        return max(0,score-baseline[position])
    else:
        return 0

main()