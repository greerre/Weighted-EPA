###############################################################
###############################################################
##                                                           ##
## This file allows you to test new features with only 2     ##
## lines of code per feature. Add one line to define how     ##
## the weight should be calcualted, and another to add it    ##
## to a list of weights to test                              ##
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



def feature_test(pbpDF,discount):
    ###############################################
    ############  edit below this line ############
    ###############################################
    ## create custom weights ##
    ## these fields must have '_weight' at the end ##
    pbpDF['fumble_weight'] = numpy.where((pbpDF['fumble'] == 1), 1-discount,1)
    pbpDF['big_play_weight'] = numpy.where((pbpDF['epa'] > 3), 1-discount,1)
    pbpDF['big_run_weight'] = numpy.where((pbpDF['play_type'] == 'run') & (pbpDF['epa'] > 3), 1-discount,1)
    pbpDF['kicker_weight'] = numpy.where((numpy.isin(pbpDF['play_type'],['extra_point','field_goal'])), 1-discount,1)
    pbpDF['return_weight'] = numpy.where((numpy.isin(pbpDF['play_type'],['punt','kickoff'])), 1-discount,1)
    pbpDF['holding_weight'] = numpy.where((pbpDF['penalty_type'] == 'Offensive Holding'), 1-discount,1)
    pbpDF['first_down_penalty_weight'] = numpy.where((pbpDF['first_down_penalty'] == 1), 1-discount,1)
    pbpDF['qb_hit_weight'] = numpy.where((pbpDF['qb_hit'] == 1), 1-discount,1)
    ## Add weights to list ##
    ## The weight names must match above, minus the '_weight' ##
    weights = [
        'fumble',
        'big_play',
        'big_run',
        'kicker',
        'return',
        'holding',
        'first_down_penalty',
        'qb_hit'
    ]
    ## run the script ##
    ################################################
    ############ ignore below this line ############
    ################################################
    ## add a baseline for comparison ##
    pbpDF['baseline_weight'] = 1
    weights.append('baseline')
    ## create all neeeded lists and aggregation dictionaries ##
    aggregationDict = {
        'margin' : 'max',
    }
    renameDict = {
        'defteam' : 'posteam',
    }
    headers = [
        'game_id',
        'posteam',
        'season',
        'game_number',
        'margin'
    ]
    finalAggDict = {
        'margin' : 'sum',
    }
    lastRenameDict = {
        'margin' : 'margin_L8',
    }
    print('Calculating R2 for {0} weights...'.format(len(weights)))
    ## creates epa's and define aggregations for each weight ##
    for weight in weights:
        pbpDF['{0}_epa'.format(weight)] = pbpDF['epa'] * pbpDF['{0}_weight'.format(weight)]
        aggregationDict['{0}_epa'.format(weight)] = 'sum'
        renameDict['{0}_epa'.format(weight)] = '{0}_epa_against'.format(weight)
        headers.append('{0}_net'.format(weight))
        finalAggDict['{0}_net'.format(weight)] = 'sum'
        lastRenameDict['{0}_net'.format(weight)] = '{0}_net_L8'.format(weight)
    gameDF = pbpDF.groupby(['posteam','defteam','season','game_id','game_number']).agg(aggregationDict).reset_index()
    gameDF = gameDF.sort_values(by=['posteam','game_id'])
    gameDF_defense = gameDF.drop(columns=['posteam','game_number','margin'])
    gameDF_defense = gameDF_defense.rename(columns=renameDict)
    gameDF = pd.merge(gameDF,gameDF_defense,on=['posteam','season','game_id'])
    for weight in weights:
        gameDF['{0}_net'.format(weight)] = gameDF['{0}_epa'.format(weight)] - gameDF['{0}_epa_against'.format(weight)]
    completeDF = gameDF[headers]
    completeDFfirst = completeDF[completeDF['game_number'] <= 8]
    completeDFlast = completeDF[completeDF['game_number'] > 8]
    completeDFfirst = completeDFfirst.drop(columns=['game_id','game_number'])
    completeDFlast = completeDFlast.drop(columns=['game_id','game_number'])
    completeDFfirst = completeDFfirst.groupby(['posteam','season']).agg(finalAggDict).reset_index()
    completeDFlast = completeDFlast.groupby(['posteam','season']).agg(finalAggDict).reset_index()
    completeDFlast = completeDFlast.rename(columns=lastRenameDict)
    finalDF = pd.merge(completeDFfirst,completeDFlast,on=['posteam','season'])
    result_row = {
        'discount' : '{0}%'.format(round(discount*100,0)),
    }
    for weight in weights:
        model = sm.OLS(finalDF['margin_L8'],finalDF['{0}_net'.format(weight)])
        results = model.fit()
        result_row['{0}'.format(weight)] = results.rsquared
    return {'result_row' : result_row, 'weights' : weights,}


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

list100 = range(-100,101)
listDec = []
for i in list100:
    listDec.append(i/100)

resultList = []
weight_list = []
for i in listDec:
    results = feature_test(pbpFinalDF,i)
    resultList.append(results['result_row'])
    weight_list = results['weights']

r2DF = pd.DataFrame(resultList)

finalHeaders = [
    'discount',
    'baseline',
]

for weight in weight_list:
    if weight == 'baseline':
        pass
    else:
        finalHeaders.append(weight)

r2DF = r2DF[finalHeaders]

r2DF.to_csv('{0}/new_feature_rsqs.csv'.format(output_folder))

maxList = []
for col in finalHeaders:
    if col in ['epa_to_first_8', 'discount']:
        pass
    else:
        maxLoc = r2DF[col].idxmax()
        if col == 'baseline':
            result_row3 = {
                'weight_type' : col,
                'weight' : 0,
                'rsq' : r2DF.loc[maxLoc, col],
            }
        else:
            result_row3 = {
                'weight_type' : col,
                'weight' : r2DF.loc[maxLoc, 'discount'],
                'rsq' : r2DF.loc[maxLoc, col],
            }
        maxList.append(result_row3)


maximizing_weight_df = pd.DataFrame(maxList)
maximizing_weight_df = maximizing_weight_df[['weight_type','weight','rsq']]
maximizing_weight_df = maximizing_weight_df.sort_values(by=['rsq']).reset_index()
print(maximizing_weight_df)
maximizing_weight_df.to_csv('{0}/new_feature_rsqs_max_only.csv'.format(output_folder))
