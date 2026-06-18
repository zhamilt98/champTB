import json

with open('pokemon.json', 'r') as f:
    data = json.load(f)

for p in data:
    if p['name'] == 'Hisuian Palafin':
        p['name'] = 'Palafin (Hero)'

with open('pokemon.json', 'w') as f:
    json.dump(data, f, indent=4)
