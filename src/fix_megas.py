import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def fix_megas():
    with open(os.path.join(DATA_DIR, 'pokemon.json'), 'r') as f:
        data = json.load(f)
        
    counts = {}
    for p in data:
        name = p['name']
        counts[name] = counts.get(name, 0) + 1
        
    for name, count in counts.items():
        if count > 1:
            # Let's print the name, image url and stats to see
            forms = [p for p in data if p['name'] == name]
            for f in forms:
                print(f"Name: {f['name']}, Image: {f['image']}")

if __name__ == "__main__":
    fix_megas()
