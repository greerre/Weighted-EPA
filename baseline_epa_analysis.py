###############################################################
###############################################################
## This file outputs the baseline analysis for EPAs and rsqs ##
## Included is the rsq for:                                  ##
##      Point Margin                                         ##
##      Net EPA / Play                                       ##
##      Total EPA                                            ##
##      ex Special Teams  (i.e. Pass and Rush Only)          ##
##      Pass Only                                            ##
##      Rush Only                                            ##
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
pbpDF2 = pbpFinalDF

## create EPAs to replicate @moo12152's work ##
pbpDF2['epa_baseline'] = pbpDF2['epa']
pbpDF2['epa_baseline_sum'] = pbpDF2['epa']
pbpDF2['epa_offense_defense_only'] = pbpDF2['epa'] * numpy.where((numpy.isin(pbpDF2['play_type'],st_plays)),0,1)
pbpDF2['epa_pass_only'] = pbpDF2['epa'] * numpy.where((numpy.isin(pbpDF2['play_type'],st_plays)),0,1) * numpy.where((pbpDF2['play_type'] == 'Run'),0,1)
pbpDF2['epa_rush_only'] = pbpDF2['epa'] * numpy.where((numpy.isin(pbpDF2['play_type'],st_plays)),0,1) * numpy.where((pbpDF2['play_type'] == 'Run'),1,0)

## calculate game totals ##
aggregationDict = {
    'epa_baseline' : 'mean',
    'epa_baseline_sum' : 'sum',
    'epa_offense_defense_only' : 'mean',
    'epa_pass_only' : 'mean',
    'epa_rush_only' : 'mean',
    'margin' : 'max',
}

gameDF = pbpDF2.groupby(['posteam','defteam','season','game_id','game_number']).agg(aggregationDict).reset_index()
gameDF = gameDF.sort_values(by=['posteam','game_id'])

## create 'against' EPAs for defense ##
renameDict = {
    'defteam' : 'posteam',
    'epa_baseline' : 'epa_baseline_against',
    'epa_baseline_sum' : 'epa_baseline_sum_against',
    'epa_offense_defense_only' : 'epa_offense_defense_only_against',
    'epa_pass_only' : 'epa_pass_only_against',
    'epa_rush_only' : 'epa_rush_only_against',
    'margin' : 'margin_against',
}

gameDF_defense = gameDF.drop(columns=['posteam','game_number'])
gameDF_defense = gameDF_defense.rename(columns=renameDict)

gameDF = pd.merge(gameDF,gameDF_defense,on=['posteam','season','game_id'])


## calculate net EPA by substracting against plays ##
gameDF['epa_baseline_net'] = gameDF['epa_baseline'] - gameDF['epa_baseline_against']
gameDF['epa_baseline_sum_net'] = gameDF['epa_baseline_sum'] - gameDF['epa_baseline_sum_against']
gameDF['epa_offense_defense_only_net'] = gameDF['epa_offense_defense_only'] - gameDF['epa_offense_defense_only_against']
gameDF['epa_pass_only_net'] = gameDF['epa_pass_only'] - gameDF['epa_pass_only_against']
gameDF['epa_rush_only_net'] = gameDF['epa_rush_only'] - gameDF['epa_rush_only_against']

headers = [
    'game_id',
    'posteam',
    'season',
    'game_number',
    'epa_baseline_net',
    'epa_baseline_sum_net',
    'epa_offense_defense_only_net',
    'epa_pass_only_net',
    'epa_rush_only_net',
    'margin'
]

completeDF = gameDF[headers]

## split data set into first and second half ##
completeDFfirst = completeDF[completeDF['game_number'] <= 8]
completeDFlast = completeDF[completeDF['game_number'] > 8]
completeDFfirst = completeDFfirst.drop(columns=['game_id'])
completeDFlast = completeDFlast.drop(columns=['game_id'])

finalAggDict = {
    'epa_baseline_net' : 'mean',
    'epa_baseline_sum_net' : 'sum',
    'epa_offense_defense_only_net' : 'mean',
    'epa_pass_only_net' : 'mean',
    'epa_rush_only_net' : 'mean',
    'margin' : 'sum',
    'game_number' : 'count',
}

completeDFfirst = completeDFfirst.groupby(['posteam','season']).agg(finalAggDict).reset_index()
completeDFlast = completeDFlast.groupby(['posteam','season']).agg(finalAggDict).reset_index()

lastRenameDict = {
    'epa_baseline_net' : 'epa_baseline_net_L8',
    'epa_baseline_sum_net' : 'epa_baseline_sum_net_L8',
    'epa_offense_defense_only_net' : 'epa_offense_defense_only_net_L8',
    'epa_pass_only_net' : 'epa_pass_only_net_L8',
    'epa_rush_only_net' : 'epa_rush_only_net_L8',
    'margin' : 'margin_L8',
    'game_number' : 'game_number_l8',
}
completeDFlast = completeDFlast.rename(columns=lastRenameDict)

finalDF = pd.merge(completeDFfirst,completeDFlast,on=['posteam','season'])
finalDF.to_csv('{0}/baseline_epa_analysis.csv'.format(output_folder))

## calculate rsquareds ##
model0 = sm.OLS(finalDF['margin_L8'],finalDF['margin'])
results0 = model0.fit()
model1 = sm.OLS(finalDF['margin_L8'],finalDF['epa_baseline_net'])
results1 = model1.fit()
model2 = sm.OLS(finalDF['margin_L8'],finalDF['epa_baseline_sum_net'])
results2 = model2.fit()
model3 = sm.OLS(finalDF['margin_L8'],finalDF['epa_offense_defense_only_net'])
results3 = model3.fit()
model4 = sm.OLS(finalDF['margin_L8'],finalDF['epa_pass_only_net'])
results4 = model4.fit()
model5 = sm.OLS(finalDF['margin_L8'],finalDF['epa_rush_only_net'])
results5 = model5.fit()
model6 = sm.OLS(finalDF['margin'],finalDF['epa_baseline_sum_net'])
results6 = model6.fit()

result_row = {
    'Point Margin vs Point Margin L8' : results0.rsquared,
    'net-EPA / Play vs Point Margin L8' : results1.rsquared,
    'Total net-EPA vs Point Margin L8' : results2.rsquared,
    'net-EPA / Play ex Special Teams vs Point Margin L8' : results3.rsquared,
    'net-EPA / Play Pass Only vs Point Margin L8' : results4.rsquared,
    'net-EPA / Play Rush Only vs Point Margin L8' : results5.rsquared,
    'Total net-EPA vs Point Margin F8' : results6.rsquared,
}

rsq_df = pd.DataFrame([result_row])
rsq_df = rsq_df[[
    'Point Margin vs Point Margin L8',
    'net-EPA / Play vs Point Margin L8',
    'Total net-EPA vs Point Margin L8',
    'net-EPA / Play ex Special Teams vs Point Margin L8',
    'net-EPA / Play Pass Only vs Point Margin L8',
    'net-EPA / Play Rush Only vs Point Margin L8',
    'Total net-EPA vs Point Margin F8'
]]
rsq_df.to_csv('{0}/baseline_epa_rsqs.csv'.format(output_folder))
