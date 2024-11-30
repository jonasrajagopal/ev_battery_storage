import json
import pandas as pd
import numpy as np

def capacity_wind(x):
    if x < 3 or x > 25:
        return 0
    if x > 15:
        return 1
    return x**3 / 15**3
    
state_abbrev = 'TX'
with open(f'{state_abbrev}_coords.json', 'r') as f:
    in_state = json.load(f)
    
raw_data = pd.read_csv(f'{state_abbrev}2021overall.csv')
raw_data['lat_lon'] = raw_data.apply(lambda x: f"{x['lat']} {x['lon']}", axis=1)
raw_data = raw_data[raw_data['lat_lon'].isin(in_state)]

raw_data['wind_speed'] = raw_data.apply(lambda x: np.sqrt(x['U50M']**2 + x['V50M']**2), axis=1)
raw_data['wind_capacity'] = raw_data['wind_speed'].apply(lambda x: capacity_wind(x))

hourly_data = {'time': [], 'total_SWGDN': [], 'total_wind_capacity':[]}
for time, hour in raw_data.groupby('time'):
    hourly_data['time'].append(time)
    hourly_data['total_SWGDN'].append(hour['SWGDN'].sum())
    hourly_data['total_wind_capacity'].append(hour['wind_capacity'].sum())

supply_data = pd.DataFrame(hourly_data)

if state_abbrev == 'CA':
    supply_data = supply_data.iloc[:-24, :]
    demand_data = pd.read_csv('CAISO_mid_demand.csv')
    demand_data=demand_data[demand_data['YEAR'] == 2021]
    init_demands = list(demand_data['BASELINE_CONSUMPTION'])
    adjusted_demands = [0, 0, 0, 0, 0, 0, 0, 0] + init_demands[:-8]  
    supply_data['demand'] = adjusted_demands
    supply_data = supply_data.iloc[8:, :]
elif state_abbrev == 'TX':
    supply_data = supply_data.iloc[:-24, :]
    demand_data = pd.read_csv('Native_Load_2021.csv')
    init_demands = list(demand_data['ERCOT'])
    adjusted_demands = ['0', '0', '0', '0', '0', '0', '0'] + init_demands[:-7]  
    adjusted_demands = [float(x.replace(',', '')) for x in adjusted_demands]
    supply_data['demand'] = adjusted_demands
    supply_data = supply_data.iloc[7:, :]

supply_data.to_csv(f'{state_abbrev}2021hourly.csv')
    