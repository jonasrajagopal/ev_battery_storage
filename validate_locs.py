import pandas as pd
import json
import matplotlib.pyplot as plt

state = 'CA'
with open(f'{state}_coords.json', 'r') as f:
    in_state = json.load(f)
    
print(len(in_state))
x, y = [], []
for coord in in_state:
    ix, iy = coord.split()
    x.append(float(ix))
    y.append(float(iy))
    
plt.scatter(y, x)
plt.savefig(f'{state}.jpg')