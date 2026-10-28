######################################################################
# Filename:    create_csv_reports.py
# Author:      Deanna Nash dnash@ucsd.edu
# Description: Script to create .csv of landslide dates reported by NOAA Storm Events Database
#
######################################################################

# Standard Python modules
import os, sys
import glob
import numpy as np
import pandas as pd
import xarray as xr

path_to_data = '/cw3e/mead/projects/cwp140/data/'
path_to_out  = '../out/'       # output files (numerical results, intermediate datafiles) -- read & write

###################################################
### LANDSLIDE DATES FROM NOAA STORM EVENTS DATA ###
###################################################
## glob files in directory since they have weird names
fname_pattern = path_to_data + 'downloads/noaastormevents/StormEvents_details-ftp_*.csv'
fname_lst = glob.glob(fname_pattern, recursive=False)
df_lst = []
for i, fname in enumerate(sorted(fname_lst)):
    print(fname)
    df = pd.read_csv(fname, header=0)
    ## subset to San Mateo County
    idx = df['CZ_NAME'].str.contains('SAN MATEO', case=False, na=False)
    df = df.loc[idx]
    print(len(df))
    if len(df) > 0:
        # event type filter
        event_idx = df['EVENT_TYPE'].isin(['Debris Flow', 'Flood', 'Flash Flood'])

        ## filter by keywords
        df['EVENT_NARRATIVE'] = df['EVENT_NARRATIVE'].astype(str)
        df['EPISODE_NARRATIVE'] = df['EPISODE_NARRATIVE'].astype(str)

        keyword_idx = (
            df['EVENT_NARRATIVE'].str.contains('mudslide|debris flow|landslide|mass wasting', case=False, regex=True) |
            df['EPISODE_NARRATIVE'].str.contains('mudslide|debris flow|landslide|mass wasting', case=False, regex=True)
        )
                    
        df = df.loc[event_idx | keyword_idx]
        df_lst.append(df)
    else:
        pass

df = pd.concat(df_lst)
# ## set begin date to index
# Convert 'YearMonth' to datetime and extract year and month
df['YearMonth'] = pd.to_datetime(df['BEGIN_YEARMONTH'], format='%Y%m')
df['Year'] = df['YearMonth'].dt.year
df['Month'] = df['YearMonth'].dt.month
df['Day'] = pd.to_datetime(df['BEGIN_DAY'], format='%d').dt.day

# Create datetime column
df['DateTime'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df = df.set_index(pd.to_datetime(df['DateTime']))

out_fname = path_to_out + 'noaastormevents_SAN_MATEO_COUNTY_FLOOD_LANDSLIDES.csv'
df.to_csv(out_fname, index=True)