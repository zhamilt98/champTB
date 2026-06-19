import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
data_path = os.path.join(DATA_DIR, 'pokemon.json')

with open(data_path, 'r') as f:
    data = json.load(f)

for p in data:
    if p['name'] == 'Hisuian Palafin':
        p['name'] = 'Palafin (Hero)'

with open(data_path, 'w') as f:
    json.dump(data, f, indent=4)
