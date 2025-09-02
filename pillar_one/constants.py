from enum import Enum

class RandomForestFeatures(Enum):

    RB_FEATURES = [
        # Yearly stats
    'carries', 'rushing_yards', 'fantasy_ppr_ppg',
    'rushing_tds', 'rushing_fumbles', 'rushing_fumbles_lost',
    'rushing_first_downs', 'rushing_epa',
    'receptions', 'targets', 'receiving_yards', 'receiving_tds',
    'receiving_air_yards',
    'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa',
    'racr', 'target_share', 'air_yards_share',
    'wopr_x', 'fantasy_points', 'fantasy_points_ppr',
    'games', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh',
    'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh', 'years_in_league',
    'age'

        # Career Stats
    ]

    QB_FEATURES = [
       'completions', 'attempts',
        'passing_yards', 'passing_tds', 'interceptions', 'sacks', 'sack_yards',
        'sack_fumbles', 'sack_fumbles_lost', 'passing_air_yards',
        'passing_yards_after_catch', 'passing_first_downs', 'passing_epa',
        'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards',
        'rushing_tds', 'rushing_fumbles', 'rushing_fumbles_lost',
        'rushing_first_downs', 'rushing_epa', 'rushing_2pt_conversions',
        'receptions', 'targets', 'air_yards_share',
        'wopr_x', 'fantasy_points', 'fantasy_points_ppr',
        'games', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh',
        'rfd_sh', 'rtdfd_sh', 'yptmpa', 'ppr_sh', 'years_in_league',
        'age' 
    ]

    WR_PER_GAME_STATS = [
        'fantasy_points_ppr',
        'receptions',
        'targets',
        'receiving_yards',
        'receiving_tds',
        'receiving_air_yards',
    ]

    WR_PER_REC_STATS = [
        'receiving_yards',
        'receiving_air_yards',
    ]

    WR_PER_TARGET_STATS = [
        'receiving_yards',
        'receiving_air_yards',
    ]

    WR_FEATURES = [
        # Yearly Stats
        'years_in_league',
        'age',
        'games',
        'fantasy_points_ppr',
        'receptions', 
        'targets', 
        'receiving_yards',
        'receiving_tds',
        'receiving_air_yards',
        'receiving_yards_after_catch',
        'receiving_epa',
        'tgt_sh',
        'ay_sh', 
        'yac_sh',
        # 'carries', 
        # 'rushing_yards',
        # 'rushing_epa',
        # 'receiving_first_downs', 
        # 'racr', 'target_share', 'air_yards_share',
        # 'wopr_x',
        #   'wopr_y', 'ry_sh', 'rtd_sh',
        # 'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh',
    ]

    TE_FEATURES = [
    'carries', 'rushing_yards', 'rushing_epa', 
    'receptions', 'targets', 'receiving_yards', 'receiving_tds',
    'receiving_fumbles', 'receiving_fumbles_lost', 'receiving_air_yards',
    'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa',
    'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share',
    'wopr_x', 'fantasy_points', 'fantasy_points_ppr',
    'games', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh',
    'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh', 'years_in_league',
    'age'
    ]

"""
test_features = [
    'completions', 'attempts',
    'passing_yards', 'passing_tds', 'interceptions', 'sacks', 'sack_yards',
    'sack_fumbles', 'sack_fumbles_lost', 'passing_air_yards',
    'passing_yards_after_catch', 'passing_first_downs', 'passing_epa',
    'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards',
    'rushing_tds', 'rushing_fumbles', 'rushing_fumbles_lost',
    'rushing_first_downs', 'rushing_epa', 'rushing_2pt_conversions',
    'receptions', 'targets', 'receiving_yards', 'receiving_tds',
    'receiving_fumbles', 'receiving_fumbles_lost', 'receiving_air_yards',
    'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa',
    'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share',
    'wopr_x', 'special_teams_tds', 'fantasy_points', 'fantasy_points_ppr',
    'games', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh',
    'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh', 'years_in_league',
    'age'
]"""