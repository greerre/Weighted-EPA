###############################################################
###############################################################
##                                                           ##
## This file will recreate the original wegithed epa analysis##
## Please read the notes below, which contain information    ##
## On how the script has changed since the original post.    ##
## TLDR is that there were 2 erros, it used the old PBP files##
## and used PosTeamScore to calculate game margin.           ##
##                                                           ##
## This script was written in a way that makes it laborous   ##
## to add new features. If you'd like to test new features,  ##
## you should use the new_feature_test.py script             ##
##                                                           ##
###############################################################
###############################################################


## issues to fix with new nflscrapR data structure ##
## Accepted.Penalty no longer exists --> investigate how penalties report ##
## PlayType no long specifies things like end of quarter --> figure out the impact ##

## Errors in original code ##
## ns_fumb was *sack* only fumbles. ns_fumb turns out not to be as impactful ##
## all fumbles are now included instead ##
## red zone was using ydstogo not yds_100 ##

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



## not all plays are considered ##
excludedPlayTypes = [
    'End of Game',
    ##'Extra Point',
    ##'Field Goal',
    'Half End',
    'qb_kneel',
    'qb_spike',
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
    'punt',
    'kickoff',
    'extra_point',
    'field_goal'
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
pbpDF2 = pbpFinalDF


## function that calculates an r squared for every weighting ##
def calcR2(pbpDF2, discount):
    ## create weights ##
    pbpDF2['run_weight'] = numpy.where((pbpDF2['play_type'] == 'run'), 1-discount,1)
    pbpDF2['fumble_weight'] = numpy.where(pbpDF2['fumble'] == 1), 1-discount,1)
    pbpDF2['fs_down_weight'] = numpy.where((pbpDF2['down'] == 1) | (pbpDF2['down'] == 2), 1-discount,1)
    pbpDF2['red_zone_weight'] = numpy.where((pbpDF2['yardline_100'] <= 20), 1-discount,1)
    pbpDF2['garbage_time_weight'] = numpy.where((pbpDF2['wp'] >= .90) | (pbpDF2['wp'] <= .10), 1-discount,1)
    pbpDF2['special_teams_weight'] = numpy.where((numpy.isin(pbpDF2['play_type'],st_plays)), 1-discount,1)
    pbpDF2['penalty_weight'] = numpy.where((pbpDF2['penalty'] == 1), 1-discount,1)
    pbpDF2['int_weight'] = numpy.where((pbpDF2['interception'] ==1), 1-discount,1)
    ## create epas ##
    pbpDF2['epa_baseline'] = pbpDF2['epa']
    pbpDF2['epa_run'] = pbpDF2['epa'] * pbpDF2['run_weight']
    pbpDF2['epa_fumb'] = pbpDF2['epa'] * pbpDF2['fumble_weight']
    pbpDF2['epa_fs_down'] = pbpDF2['epa'] * pbpDF2['fs_down_weight']
    pbpDF2['epa_red_zone'] = pbpDF2['epa'] * pbpDF2['red_zone_weight']
    pbpDF2['epa_garbage_time'] = pbpDF2['epa'] * pbpDF2['garbage_time_weight']
    pbpDF2['epa_st'] = pbpDF2['epa'] * pbpDF2['special_teams_weight']
    pbpDF2['epa_penalty'] = pbpDF2['epa'] * pbpDF2['penalty_weight']
    pbpDF2['epa_int'] = pbpDF2['epa'] * pbpDF2['int_weight']
    ## create aggregation dictionary ##
    aggregationDict2 = {
        'epa_baseline' : 'sum',
        'epa_run' : 'sum',
        'epa_fumb' : 'sum',
        'epa_fs_down' : 'sum',
        'epa_red_zone' : 'sum',
        'epa_garbage_time' : 'sum',
        'epa_st' : 'sum',
        'epa_penalty' : 'sum',
        'epa_int' : 'sum',
        'margin' : 'max',
    }
    gameDF2 = pbpDF2.groupby(['posteam','defteam','season','game_id','game_number']).agg(aggregationDict2).reset_index()
    gameDF2 = gameDF2.sort_values(by=['posteam','game_id'])
    renameDict2 = {
        'defteam' : 'posteam',
        'epa_baseline' : 'epa_baseline_against',
        'epa_run' : 'epa_run_against',
        'epa_fumb' : 'epa_ns_fumb_against',
        'epa_fs_down' : 'epa_fs_down_against',
        'epa_red_zone' : 'epa_red_zone_against',
        'epa_garbage_time' : 'epa_garbage_time_against',
        'epa_st' : 'epa_st_against',
        'epa_penalty' : 'epa_penalty_against',
        'epa_int' : 'epa_int_against',
    }
    gameDF_defense2 = gameDF2.drop(columns=['posteam','game_number','margin'])
    gameDF_defense2 = gameDF_defense2.rename(columns=renameDict2)
    gameDF2 = pd.merge(gameDF2,gameDF_defense2,on=['posteam','season','game_id'])
    gameDF2['epa_baseline_net'] = gameDF2['epa_baseline'] - gameDF2['epa_baseline_against']
    gameDF2['epa_defense_net'] = gameDF2['epa_baseline'] - ((1-discount) * gameDF2['epa_baseline_against'])
    gameDF2['epa_run_net'] = gameDF2['epa_run'] - gameDF2['epa_run_against']
    gameDF2['epa_fumb_net'] = gameDF2['epa_fumb'] - gameDF2['epa_fumb_against']
    gameDF2['epa_fs_down_net'] = gameDF2['epa_fs_down'] - gameDF2['epa_fs_down_against']
    gameDF2['epa_red_zone_net'] = gameDF2['epa_red_zone'] - gameDF2['epa_red_zone_against']
    gameDF2['epa_garbage_time_net'] = gameDF2['epa_garbage_time'] - gameDF2['epa_garbage_time_against']
    gameDF2['epa_st_net'] = gameDF2['epa_st'] - gameDF2['epa_st_against']
    gameDF2['epa_penalty_net'] = gameDF2['epa_penalty'] - gameDF2['epa_penalty_against']
    gameDF2['epa_int_net'] = gameDF2['epa_int'] - gameDF2['epa_int_against']
    headers2 = [
        'game_id',
        'posteam',
        'season',
        'game_number',
        'epa_baseline_net',
        'epa_defense_net',
        'epa_run_net',
        'epa_fumb_net',
        'epa_fs_down_net',
        'epa_red_zone_net',
        'epa_garbage_time_net',
        'epa_st_net',
        'epa_penalty_net',
        'epa_int_net',
        'margin'
    ]
    completeDF2 = gameDF2[headers2]
    completeDFfirst2 = completeDF2[completeDF2['game_number'] <= 8]
    completeDFlast2 = completeDF2[completeDF2['game_number'] > 8]
    completeDFfirst2 = completeDFfirst2.drop(columns=['game_id','game_number'])
    completeDFlast2 = completeDFlast2.drop(columns=['game_id','game_number'])
    finalAggDict2 = {
        'epa_baseline_net' : 'sum',
        'epa_defense_net' : 'sum',
        'epa_run_net' : 'sum',
        'epa_fumb_net' : 'sum',
        'epa_fs_down_net' : 'sum',
        'epa_red_zone_net' : 'sum',
        'epa_garbage_time_net' : 'sum',
        'epa_st_net' : 'sum',
        'epa_penalty_net' : 'sum',
        'epa_int_net' : 'sum',
        'margin' : 'sum',
    }
    completeDFfirst2 = completeDFfirst2.groupby(['posteam','season']).agg(finalAggDict2).reset_index()
    completeDFlast2 = completeDFlast2.groupby(['posteam','season']).agg(finalAggDict2).reset_index()
    lastRenameDict2 = {
        'epa_baseline_net' : 'epa_baseline_net_L8',
        'epa_defense_net' : 'epa_defense_net_L8',
        'epa_run_net' : 'epa_run_net_L8',
        'epa_fumb_net' : 'epa_fumb_net_L8',
        'epa_fs_down_net' : 'epa_fs_down_net_L8',
        'epa_red_zone_net' : 'epa_red_zone_net_L8',
        'epa_garbage_time_net' : 'epa_garbage_time_net_L8',
        'epa_st_net' : 'epa_st_net_L8',
        'epa_penalty_net' : 'epa_penalty_net_L8',
        'epa_int_net' : 'epa_int_net_L8',
        'margin' : 'margin_L8',
    }
    completeDFlast2 = completeDFlast2.rename(columns=lastRenameDict2)
    finalDF2 = pd.merge(completeDFfirst2,completeDFlast2,on=['posteam','season'])
    model1 = sm.OLS(finalDF2['margin'],finalDF2['epa_baseline_net'])
    results1 = model1.fit()
    model2 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_baseline_net'])
    results2 = model2.fit()
    model3 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_defense_net'])
    results3 = model3.fit()
    model4 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_run_net'])
    results4 = model4.fit()
    model5 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_fumb_net'])
    results5 = model5.fit()
    model6 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_fs_down_net'])
    results6 = model6.fit()
    model7 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_red_zone_net'])
    results7 = model7.fit()
    model8 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_garbage_time_net'])
    results8 = model8.fit()
    model9 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_st_net'])
    results9 = model9.fit()
    model10 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_penalty_net'])
    results10 = model10.fit()
    model11 = sm.OLS(finalDF2['margin_L8'],finalDF2['epa_int_net'])
    results11 = model11.fit()
    result_row2 = {
        'discount' : '{0}%'.format(round(discount*100,0)),
        'epa_to_first_8' : results1.rsquared,
        'baseline' : results2.rsquared,
        'defense' : results3.rsquared,
        'run' : results4.rsquared,
        'fumb' : results5.rsquared,
        'fs_down' : results6.rsquared,
        'red_zone' : results7.rsquared,
        'garbage_time' : results8.rsquared,
        'special_teams' : results9.rsquared,
        'penalties' : results10.rsquared,
        'ints' : results11.rsquared,
    }
    return result_row2

## calculate r squared for every weight from -100% to 100% ##
list100 = range(-100,101)
listDec = []
for i in list100:
    listDec.append(i/100)

resultList = []
for i in listDec:
    resultList.append(calcR2(pbpDF2,i))

r2DF = pd.DataFrame(resultList)

finalHeaders2 = [
    'epa_to_first_8',
    'discount',
    'baseline',
    'defense',
    'fs_down',
    'garbage_time',
    'ns_fumb',
    'red_zone',
    'run',
    'special_teams',
    'penalties',
    'ints'
]

r2DF = r2DF[finalHeaders2]


r2DF.to_csv('{0}/r2_weightings.csv'.format(output_folder))

## find max values ##
maxList = []
for col in finalHeaders2:
    if col in ['epa_to_first_8', 'discount']:
        pass
    else:
        maxLoc = r2DF[col].idxmax()
        result_row3 = {
            'weight_type' : col,
            'weight' : r2DF.loc[maxLoc, 'discount'],
            'rsq' : r2DF.loc[maxLoc, col],
        }
        maxList.append(result_row3)

maximizing_weight_df = pd.DataFrame(maxList)
maximizing_weight_df.to_csv('{0}/max_r2_weightings.csv'.format(output_folder))
