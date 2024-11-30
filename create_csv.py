import pickle
import os
import xarray as xr
import pandas as pd
from tqdm import tqdm

state_abbrev = 'TX'
solar_data = pd.DataFrame([], columns=['time', 'lat', 'lon', 'SWGDN'])
wind_1_data = pd.DataFrame([], columns=['time', 'lat', 'lon', 'U50M'])
wind_2_data = pd.DataFrame([], columns=['time', 'lat', 'lon', 'V50M'])

dir = f'{state_abbrev}2021Solar'
for f in tqdm(os.listdir(dir)):
    if not f.startswith('.'):
        db = xr.open_dataset(os.path.join(dir, f), engine="netcdf4")
        db = db.SWGDN.to_dataframe().reset_index()
        solar_data = pd.concat([solar_data, db], axis=0)
    
solar_data.to_csv(f'{state_abbrev}2021Solar.csv')
        
dir = f'{state_abbrev}2021Wind'
for f in tqdm(os.listdir(dir)):
    if not f.startswith('.'):
        db = xr.open_dataset(os.path.join(dir, f), engine="netcdf4")
        db = db.U50M.to_dataframe().reset_index()
        wind_1_data = pd.concat([wind_1_data, db], axis=0)
wind_1_data.to_csv(f'{state_abbrev}2021U50M.csv')

for f in tqdm(os.listdir(dir)):
    if not f.startswith('.'):
        db = xr.open_dataset(os.path.join(dir, f), engine="netcdf4")
        db = db.V50M.to_dataframe().reset_index()
        wind_2_data = pd.concat([wind_2_data, db], axis=0)
wind_2_data.to_csv(f'{state_abbrev}2021V50M.csv')

test_merge_1 = pd.merge(solar_data, wind_1_data, on=['time', 'lat', 'lon'], how='outer')
test_merge_2 = pd.merge(test_merge_1, wind_2_data, on=['time', 'lat', 'lon'], how='outer')

test_merge_2.to_csv(f'{state_abbrev}2021overall.csv')