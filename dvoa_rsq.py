###############################################################
###############################################################
##                                                           ##
## This calculates the OOS Rsq for DVOA                      ##
##                                                           ##
###############################################################
###############################################################

## packages used ##
import numpy
import pandas as pd


## Enter your file paths ##
dvoa_filepath = 'replace with your filepath for the dvoa csv'
game_filepath = 'replace with your filepath for the game csv'
output_folder = 'replace with where you want the files to go' ## don't include final back slash ##


gameDataDF = pd.read_csv(game_filepath)
## this is a consolidated file of all nflscrapR game csvs
## the consolidation was done with pandas concat function ##

dvoa_df = pd.read_csv(dvoa_filepath)
## this is a file with all DVOAs going back to 2009 ##


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
## pbpDF2['posteam'] = pbpDF2['posteam'].replace(pbp_team_standard_dict)
## pbpDF2['defteam'] = pbpDF2['defteam'].replace(pbp_team_standard_dict)
gameDataDF['home_team'] = gameDataDF['home_team'].replace(pbp_team_standard_dict)
gameDataDF['away_team'] = gameDataDF['away_team'].replace(pbp_team_standard_dict)
dvoa_df['posteam'] = dvoa_df['Team'].replace(dvoa_team_standard_dict)


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


## prep additional dvoa naming ##
dvoa_rename_dict = {
    'Week' : 'week',
    'Season' : 'season',
}

dvoa_df = dvoa_df.drop(columns=['Team'])
dvoa_df = dvoa_df.rename(columns=dvoa_rename_dict)

combinedDF = pd.merge(gameDataDFFinal,dvoa_df, on=['posteam','week','season'])

combinedDF_headers = [
    'posteam',
    'week',
    'season',
    'game_number',
    'margin',
    'Total DVOA'
]

combinedDF = combinedDF[combinedDF_headers]

## calculate r2 ##
combinedDFfirst = combinedDF[combinedDF['game_number'] == 8]
combinedDFsecond = combinedDF[combinedDF['game_number'] > 8]
combinedDFfinal = combinedDF[combinedDF['game_number'] == 16]

combinedDFfirst = combinedDFfirst.drop(columns=['week','game_number','margin'])
combinedDFfinal = combinedDFfinal.drop(columns=['week','game_number','margin'])
combinedDFsecond = combinedDFsecond.drop(columns=['week','game_number','Total DVOA'])

combined_agg_dict = {
    'margin' : 'sum',
}

rename_first = {
    'Total DVOA' : 'Total DVOA (After 8 Games)',
}

rename_final = {
    'Total DVOA' : 'Total DVOA (After 16 Games)',
}

combinedDFsecond = combinedDFsecond.groupby(['posteam','season']).agg(combined_agg_dict).reset_index()

combinedDFfirst = combinedDFfirst.rename(columns=rename_first)
combinedDFfinal = combinedDFfinal.rename(columns=rename_final)

final_df = pd.merge(combinedDFfirst,combinedDFfinal,on=['posteam','season'])
final_df = pd.merge(final_df,combinedDFsecond,on=['posteam','season'])

final_df.to_csv('{0}/dvoa_rsq.csv'.format(output_folder))





##
