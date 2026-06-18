import json

def fix_megas():
    with open('pokemon.json', 'r') as f:
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
