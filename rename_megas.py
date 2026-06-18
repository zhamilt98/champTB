import json

def rename_megas():
    with open('pokemon.json', 'r') as f:
        data = json.load(f)
        
    for p in data:
        img = p['image']
        if img.endswith('-m.png'):
            p['name'] = 'Mega ' + p['name']
        elif img.endswith('-mx.png'):
            p['name'] = 'Mega ' + p['name'] + ' X'
        elif img.endswith('-my.png'):
            p['name'] = 'Mega ' + p['name'] + ' Y'
        elif img.endswith('-a.png'):
            if p['name'] == 'Tauros':
                p['name'] = 'Paldean ' + p['name'] + ' (Aqua)'
            else:
                p['name'] = 'Alolan ' + p['name']
        elif img.endswith('-g.png'):
            p['name'] = 'Galarian ' + p['name']
        elif img.endswith('-h.png'):
            p['name'] = 'Hisuian ' + p['name']
        elif img.endswith('-p.png'):
            p['name'] = 'Paldean ' + p['name'] + ' (Combat)'
        elif img.endswith('-b.png'):
            if p['name'] == 'Tauros':
                p['name'] = 'Paldean ' + p['name'] + ' (Blaze)'
            else:
                p['name'] = 'Blade ' + p['name']
        elif img.endswith('-f.png'):
            p['name'] = p['name'] + ' (Female)'
            
    with open('pokemon.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    print("Renamed forms successfully.")

if __name__ == "__main__":
    rename_megas()
