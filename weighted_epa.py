###############################################################
###############################################################
##                                                           ##
## This file outputs the the RSQ for the weighted epa        ##
##                                                           ##
###############################################################
###############################################################


## packages used ##
import pandas as pd
import numpy
import statsmodels.api as sm

## Enter your file paths ##
pbp_filepath = 'replace with your filepath for the pbp csv'
game_filepath = 'replace with your filepath for the game csv'
output_folder = 'replace with where you want the files to go' ## don't include final back slash ##

pbpDF2 = pd.read_csv(pbp_filepath,low_memory=False)
## this is a consolidated file of all nflScrapR pbp season csvs ##
## the consolidation was done with pandas concat function ##

gameDataDF = pd.read_csv(game_filepath)
## this is a consolidated file of all nflscrapR game csvs
## the consolidation was done with pandas concat function ##


## original r squared maximizing weights ##
## note that these were based on pbp scores not game file score ##
## these are **not** the maximizing values
weights = [
    {
        'defense' : .39,
        'fs_down' : -.39,
        'garbage_time' : .56,
        'ns_fumb' : 1,
        'special_teams' : .31
    }
]


## Dictionaries for standardizing team names across data sets ##
dvoa_team_standard_dict = {

    'ARI' : 'ARI',
    'ATL' : 'ATL',
    'BAL' : 'BAL',
    'BUF' : 'BUF',
    'CAR' : 'CAR',
    'CHI' : 'CHI',
    'CIN' : 'CIN',
    'CLE' : 'CLE',
    'DAL' : 'DAL',
    'DEN' : 'DEN',
    'DET' : 'DET',
    'GB'  : 'GB',
    'HOU' : 'HOU',
    'IND' : 'IND',
    'JAX' : 'JAX',
    'JAC' : 'JAX',
    'KC'  : 'KC',
    'LAC' : 'LAC',
    'LAR' : 'LAR',
    'MIA' : 'MIA',
    'MIN' : 'MIN',
    'NE'  : 'NE',
    'NO'  : 'NO',
    'NYG' : 'NYG',
    'NYJ' : 'NYJ',
    'OAK' : 'OAK',
    'PHI' : 'PHI',
    'PIT' : 'PIT',
    'SD'  : 'LAC',
    'SEA' : 'SEA',
    'SF'  : 'SF',
    'STL' : 'LAR',
    'TB'  : 'TB',
    'TEN' : 'TEN',
    'WAS' : 'WAS',

}

pbp_team_standard_dict = {

    'ARI' : 'ARI',
    'ATL' : 'ATL',
    'BAL' : 'BAL',
    'BUF' : 'BUF',
    'CAR' : 'CAR',
    'CHI' : 'CHI',
    'CIN' : 'CIN',
    'CLE' : 'CLE',
    'DAL' : 'DAL',
    'DEN' : 'DEN',
    'DET' : 'DET',
    'GB'  : 'GB',
    'HOU' : 'HOU',
    'IND' : 'IND',
    'JAC' : 'JAX',
    'JAX' : 'JAX',
    'KC'  : 'KC',
    'LA'  : 'LAR',
    'LAC' : 'LAC',
    'MIA' : 'MIA',
    'MIN' : 'MIN',
    'NE'  : 'NE',
    'NO'  : 'NO',
    'NYG' : 'NYG',
    'NYJ' : 'NYJ',
    'OAK' : 'OAK',
    'PHI' : 'PHI',
    'PIT' : 'PIT',
    'SD'  : 'LAC',
    'SEA' : 'SEA',
    'SF'  : 'SF',
    'STL' : 'LAR',
    'TB'  : 'TB',
    'TEN' : 'TEN',
    'WAS' : 'WAS',

}

market_team_standard_dict = {

    'ARI' : 'ARI',
    'ATL' : 'ATL',
    'BAL' : 'BAL',
    'BUF' : 'BUF',
    'CAR' : 'CAR',
    'CHI' : 'CHI',
    'CIN' : 'CIN',
    'CLE' : 'CLE',
    'DAL' : 'DAL',
    'DEN' : 'DEN',
    'DET' : 'DET',
    'GB'  : 'GB',
    'HOU' : 'HOU',
    'IND' : 'IND',
    'JAC' : 'JAX',
    'JAX' : 'JAX',
    'KC'  : 'KC',
    'LA'  : 'LAR',
    'LAC' : 'LAC',
    'MIA' : 'MIA',
    'MIN' : 'MIN',
    'NE'  : 'NE',
    'NO'  : 'NO',
    'NYG' : 'NYG',
    'NYJ' : 'NYJ',
    'OAK' : 'OAK',
    'PHI' : 'PHI',
    'PIT' : 'PIT',
    'SD'  : 'LAC',
    'SEA' : 'SEA',
    'SF'  : 'SF',
    'STL' : 'LAR',
    'TB'  : 'TB',
    'TEN' : 'TEN',
    'WAS' : 'WAS',

}


## standardize team names across data sets ##
pbpDF2['posteam'] = pbpDF2['posteam'].replace(pbp_team_standard_dict)
pbpDF2['defteam'] = pbpDF2['defteam'].replace(pbp_team_standard_dict)
gameDataDF['home_team'] = gameDataDF['home_team'].replace(pbp_team_standard_dict)
gameDataDF['away_team'] = gameDataDF['away_team'].replace(pbp_team_standard_dict)
## marketDataDF['posteam'] = marketDataDF['posteam'].replace(market_team_standard_dict)



## not all plays are considered ##
excludedPlayTypes = [
    'End of Game',
    ##'Extra Point',
    ##'Field Goal',
    'Half End',
    'QB Kneel',
    'Quarter End',
    'Spike',
    'Timeout',
    'Two Minute Warning',
    ##'No Play',
    ##'Punt',
    ##'Kickoff',
]

## special teams plays ##
st_plays = [
    'Punt',
    'Kickoff',
    'Extra Point',
    'Field Goal'
]

pbpDF2 = pbpDF2[~pbpDF2['play_type'].isin(excludedPlayTypes)]

## Calculate margin and manipulate game file to make it easier to attach ##
gameDataDF['home_margin'] = gameDataDF['home_score'] - gameDataDF['away_score']
gameDataDF['away_margin'] = gameDataDF['away_score'] - gameDataDF['home_score']
gameDataHomeDF = gameDataDF.drop(columns=['away_team','home_score','away_score','away_margin'])
gameDataHomeDF = gameDataHomeDF.rename(columns={'home_team' : 'posteam', 'home_margin' : 'margin'})
gameDataAwayDF = gameDataDF.drop(columns=['home_team','home_score','away_score','home_margin'])
gameDataAwayDF = gameDataAwayDF.rename(columns={'away_team' : 'posteam', 'away_margin' : 'margin'})
gameDataDFFinal = pd.concat([gameDataHomeDF,gameDataAwayDF],ignore_index=True).sort_values(by=['game_id'])

## add a game number to the game data to use instead of week ##
gameDataDFFinal['game_number'] = gameDataDFFinal.groupby(['posteam','season']).cumcount() + 1
gameDataDFFinal = gameDataDFFinal.drop(columns=['state_of_game','game_url','type'])
## add game data to pbp data ##
pbpFinalDF = pd.merge(pbpDF2,gameDataDFFinal,on=['posteam','game_id'])


## function for calculating weighted EPA for a set of weights ##
def calcWeightedR2(pbpDF3, weights):
    finalDF3 = None
    for weight_set in weights:
        ## create weights ##
        pbpDF3['non_sack_fumble_weight'] = numpy.where((pbpDF3['play_type'] == 'Sack') & (pbpDF3['fumble'] == 1), 1-weight_set['ns_fumb'],1)
        pbpDF3['fs_down_weight'] = numpy.where((pbpDF3['down'] == 1) | (pbpDF3['down'] == 2), 1-weight_set['fs_down'],1)
        pbpDF3['garbage_time_weight'] = numpy.where((pbpDF3['wp'] >= .90) | (pbpDF3['wp'] <= .10), 1-weight_set['garbage_time'],1)
        pbpDF3['special_teams_weight'] = numpy.where((numpy.isin(pbpDF3['play_type'],st_plays)), 1-weight_set['special_teams'],1)
        ## create epas ##
        pbpDF3['epa_baseline'] = pbpDF3['epa']
        pbpDF3['epa_weighted_m'] = pbpDF3['epa'] * pbpDF3['non_sack_fumble_weight'] * pbpDF3['fs_down_weight'] * pbpDF3['garbage_time_weight'] * pbpDF3['special_teams_weight']
        ## create aggregation dictionary ##
        aggregationDict3 = {
            'epa_baseline' : 'sum',
            'epa_weighted_m' : 'sum',
            'margin' : 'max',
        }
        gameDF3 = pbpDF3.groupby(['posteam','defteam','season','game_id','game_number']).agg(aggregationDict3).reset_index()
        gameDF3 = gameDF3.sort_values(by=['posteam','game_id'])
        renameDict3 = {
            'defteam' : 'posteam',
            'epa_baseline' : 'epa_baseline_against',
            'epa_weighted_m' : 'epa_weighted_m_against',
            'margin' : 'margin_against',
        }
        gameDF_defense3 = gameDF3.drop(columns=['posteam','game_number'])
        gameDF_defense3 = gameDF_defense3.rename(columns=renameDict3)
        gameDF3 = pd.merge(gameDF3,gameDF_defense3,on=['posteam','season','game_id'])
        gameDF3['epa_baseline_net'] = gameDF3['epa_baseline'] - gameDF3['epa_baseline_against']
        gameDF3['epa_weighted_m_net'] = gameDF3['epa_weighted_m'] - ((1-weight_set['defense']) * gameDF3['epa_weighted_m_against'])
        gameDF3['epa_weighted_delta_to_baseline_net'] = gameDF3['epa_weighted_m_net'] - gameDF3['epa_baseline_net']
        headers3 = [
            'game_id',
            'posteam',
            'season',
            'game_number',
            'epa_baseline_net',
            'epa_weighted_m_net',
            'epa_weighted_delta_to_baseline_net',
            'margin'
        ]
        completeDF3 = gameDF3[headers3]
        completeDFfirst3 = completeDF3[completeDF3['game_number'] <= 8]
        completeDFlast3 = completeDF3[completeDF3['game_number'] > 8]
        completeDFfirst3 = completeDFfirst3.drop(columns=['game_id','game_number'])
        completeDFlast3 = completeDFlast3.drop(columns=['game_id','game_number'])
        finalAggDict3 = {
            'epa_baseline_net' : 'sum',
            'epa_weighted_m_net' : 'sum',
            'epa_weighted_delta_to_baseline_net' : 'sum',
            'margin' : 'sum',
        }
        completeDFfirst3 = completeDFfirst3.groupby(['posteam','season']).agg(finalAggDict3).reset_index()
        completeDFlast3 = completeDFlast3.groupby(['posteam','season']).agg(finalAggDict3).reset_index()
        lastRenameDict3 = {
            'epa_baseline_net' : 'epa_baseline_net_L8',
            'epa_weighted_m_net' : 'epa_weighted_m_L8',
            'epa_weighted_delta_to_baseline_net' : 'epa_weighted_delta_to_baseline_net_L8',
            'margin' : 'margin_L8',
        }
        completeDFlast3 = completeDFlast3.rename(columns=lastRenameDict3)
        finalDF3 = pd.merge(completeDFfirst3,completeDFlast3,on=['posteam','season'])
        model1 = sm.OLS(finalDF3['margin'],finalDF3['epa_baseline_net'])
        results1 = model1.fit()
        model2 = sm.OLS(finalDF3['margin_L8'],finalDF3['epa_baseline_net'])
        results2 = model2.fit()
        model3 = sm.OLS(finalDF3['margin_L8'],finalDF3['epa_weighted_m_net'])
        results3 = model3.fit()
        result_row3 = {
            'epa_to_first_8' : results1.rsquared,
            'baseline' : results2.rsquared,
            'weighted' : results3.rsquared,
        }
    ##return result_row3
    return finalDF3


weightedDF = pd.DataFrame(calcWeightedR2(pbpFinalDF, weights))


weightedDF.to_csv('{0}/weighted_epa.csv'.format(output_folder))
