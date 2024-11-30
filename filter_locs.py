import xarray as xr
import requests
import pandas as pd
import json 
from tqdm import tqdm
def reverse_geocode(lat, lon):
    # Nominatim reverse geocoding URL
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 'referer': 'https://developer.mozilla.org/testpage.html'}
    # Make the request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Return the formatted address and state
        address = data.get("display_name", "Address not found")
        return address
    else:
        return "Error: Unable to retrieve data"

state_name = 'Texas'
state_abbrev = 'TX'
db = xr.open_dataset('/Users/jonasrajagopal/Desktop/22.04/project/M2T1NXRAD.5.12.4:MERRA2_400.tavg1_2d_rad_Nx.20210101.nc4.dap.nc4?dap4.ce=%2FSWGDN[0:23][230:256][115:141];%2Ftime;%2Flat[230:256];%2Flon[115:141]', engine="netcdf4")
csv = db.SWGDN.to_dataframe().reset_index()
csv['lat_lon'] = csv.apply(lambda x: f"{x['lat']} {x['lon']}", axis=1)
all_coords = set(csv['lat_lon'])
in_state = set()
for coord in tqdm(all_coords):
    address = reverse_geocode(coord.split()[0], coord.split()[1])
    if state_name in address:
        in_state.add(coord)

icl = list(in_state)

with open(f'{state_abbrev}_coords.json', 'w') as f:
    json.dump(icl, f)