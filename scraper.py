import requests
from bs4 import BeautifulSoup
import json

def fetch_pokemon():
    url = "https://www.serebii.net/pokedex-champions/stat/hp.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pokemon_list = []
    
    table = soup.find('table', {'class': 'dextable'})
    if not table:
        print("Could not find Pokemon table")
        return
        
    rows = table.find_all('tr')[2:] # skip headers
    
    for row in rows:
        cols = row.find_all('td', recursive=False)
        if len(cols) < 11:
            continue
            
        dex_no = cols[0].text.strip()
        name = cols[2].text.strip()
        
        # Types
        type_col = cols[3]
        types = [img['src'].split('/')[-1].split('.')[0] for img in type_col.find_all('img')]
        
        # Abilities
        abilities_col = cols[4]
        abilities = [a.text.strip() for a in abilities_col.find_all('a')]
        
        # Stats
        hp = cols[5].text.strip()
        atk = cols[6].text.strip()
        df = cols[7].text.strip()
        sa = cols[8].text.strip()
        sd = cols[9].text.strip()
        spd = cols[10].text.strip()
        
        # Image
        pic_col = cols[1]
        img_tag = pic_col.find('img')
        img_url = "https://www.serebii.net" + img_tag['src'] if img_tag else ""
        
        pokemon_list.append({
            "name": name,
            "dex_no": dex_no,
            "types": types,
            "abilities": abilities,
            "stats": {
                "hp": int(hp),
                "atk": int(atk),
                "def": int(df),
                "spa": int(sa),
                "spd": int(sd),
                "spe": int(spd)
            },
            "image": img_url
        })
        
    with open('pokemon.json', 'w') as f:
        json.dump(pokemon_list, f, indent=4)
    print(f"Saved {len(pokemon_list)} Pokemon")

def fetch_items():
    url = "https://www.serebii.net/pokemonchampions/items.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = []
    tables = soup.find_all('table', {'class': 'dextable'})
    for table in tables:
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 3:
                continue
            name = cols[1].text.strip()
            effect = cols[2].text.strip()
            
            pic_col = cols[0]
            img_tag = pic_col.find('img')
            img_url = "https://www.serebii.net" + img_tag['src'] if img_tag else ""
            
            items.append({
                "name": name,
                "effect": effect,
                "image": img_url
            })
            
    with open('items.json', 'w') as f:
        json.dump(items, f, indent=4)
    print(f"Saved {len(items)} Items")

if __name__ == "__main__":
    fetch_pokemon()
    fetch_items()
