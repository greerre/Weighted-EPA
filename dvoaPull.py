###############################################################
###############################################################
##                                                           ##
## This file allows you to pull DVOA from footballoutsiders. ##
## To do this, you must have your own login and cookies to   ##
## to use in the get request. Based on the ToS, I don't      ##
## believe I can upload these files directly to GitHub       ##
##                                                           ##
###############################################################
###############################################################


import requests
import time
import random
import os
import glob
import string
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy

## Enter your file paths ##
output_folder = 'replace with where you want the files to go' ## don't include final back slash ##


## Enter your cookies after signing in to footballoutsiders.com ##
cookie_dict = {

    '__atuvc' : 'You cookie info',
    '__atuvs' : 'You cookie info',
    '__gads' : 'You cookie info',
    '__utma' : 'You cookie info',
    '__utmb' : 'You cookie info',
    '__utmc' : 'You cookie info',
    '__utmt' : 'You cookie info',
    '__utmz' : 'You cookie info',
     'You cookie info', :  'You cookie info',

}

season_start = 2009
season_end = 2018
current_season = season_start
week_start = 1
week_end = 17
current_week = 1

url = 'https://www.footballoutsiders.com/premium/weekTeamSeasonDvoa.php?'

df_headers = {
    'Season' : [],
    'Week' : [],
    'Team' : [],
    'W/L' : [],
    'Total DVOA' : [],
    'Total DVOA Rank' : [],
    'Weighted DVOA' : [],
    'Weighted DVOA Rank' : [],
    'Offense DVOA' : [],
    'Offense DVOA Rank' : [],
    'Weighted Offense DVOA' : [],
    'Weighted Offense DVOA Rank' : [],
    'Defense DVOA' : [],
    'Defense DVOA Rank' : [],
    'Weighted Defense DVOA' : [],
    'Weighted Defense DVOA Rank' : [],
    'ST DVOA' : [],
    'ST DVOA Rank' : [],
    'Weighted ST DVOA' : [],
    'Weighted ST DVOA Rank' : [],
}

df = pd.DataFrame(df_headers)
while current_week <= week_end and current_season <= season_end:
    payload = {
        'od' : 'O',
        'year' : current_season,
        'team' : 'ARI',
        'week' : current_week,
    }
    time.sleep((1.5 + random.random() * 2)) ## be nice to servers! ##
    print('Requesting data for week {0}, {1}'.format(current_week,current_season))
    raw = requests.get(url, cookies=cookie_dict, params=payload)
    parsed = BeautifulSoup(raw.content, 'html.parser')
    table_rows = parsed.find_all('tbody')[0].find_all('tr')
    df_content = df_headers
    for row in table_rows:
        data = []
        for table_data in row.find_all('td'):
            stringed = str(table_data.text) ##convert from unicode##
            stringed = stringed.replace('\n','') ## replace line breaks with blanks##
            stringed = stringed.strip() ## remove spaces ##
            data.append(stringed)
        df_content['Season'].append(current_season)
        df_content['Week'].append(current_week)
        df_content['Team'].append(data[0])
        df_content['W/L'].append(data[1])
        df_content['Total DVOA'].append(data[2])
        df_content['Total DVOA Rank'].append(data[3])
        df_content['Weighted DVOA'].append(data[4])
        df_content['Weighted DVOA Rank'].append(data[5])
        df_content['Offense DVOA'].append(data[6])
        df_content['Offense DVOA Rank'].append(data[7])
        df_content['Weighted Offense DVOA'].append(data[8])
        df_content['Weighted Offense DVOA Rank'].append(data[9])
        df_content['Defense DVOA'].append(data[10])
        df_content['Defense DVOA Rank'].append(data[11])
        df_content['Weighted Defense DVOA'].append(data[12])
        df_content['Weighted Defense DVOA Rank'].append(data[13])
        df_content['ST DVOA'].append(data[14])
        df_content['ST DVOA Rank'].append(data[15])
        df_content['Weighted ST DVOA'].append(data[16])
        df_content['Weighted ST DVOA Rank'].append(data[17])
    weekDF = pd.DataFrame(df_content)
    df = pd.concat([df,weekDF], ignore_index=True)
    if current_week == week_end:
        current_season += 1
        current_week = 1
    else:
        current_week += 1

df = df[['Season', 'Week', 'Team', 'W/L', 'Total DVOA', 'Total DVOA Rank', 'Weighted DVOA', 'Weighted DVOA Rank', 'Offense DVOA', 'Offense DVOA Rank', 'Weighted Offense DVOA', 'Weighted Offense DVOA Rank', 'Defense DVOA', 'Defense DVOA Rank', 'Weighted Defense DVOA', 'Weighted Defense DVOA Rank', 'ST DVOA', 'ST DVOA Rank', 'Weighted ST DVOA', 'Weighted ST DVOA Rank']]
df = df.drop_duplicates()

df.to_csv('{0}/{1}_{2}_dvoa.csv'.format(output_folder,current_season,current_week))
