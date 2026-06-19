import os
import requests
from bs4 import BeautifulSoup
import json
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def fetch_movepools():
    url = "https://www.serebii.net/pokedex-champions/stat/hp.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'class': 'dextable'})
    if not table:
        print("Could not find Pokemon table")
        return
        
    rows = table.find_all('tr')[2:]
    
    pokemon_links = {}
    for row in rows:
        cols = row.find_all('td', recursive=False)
        if len(cols) < 11:
            continue
            
        name = cols[2].text.strip()
        a_tag = cols[2].find('a')
        if a_tag:
            link = a_tag['href']
            # Map form names to base names to avoid duplicate fetching, though serebii links are usually base names anyway
            base_name = name.split(' (')[0].replace('Mega ', '').replace('Alolan ', '').replace('Galarian ', '').replace('Hisuian ', '').replace('Paldean ', '').replace('Blade ', '')
            if base_name.endswith(' X') or base_name.endswith(' Y'):
                base_name = base_name[:-2]
            
            if base_name not in pokemon_links:
                pokemon_links[base_name] = link
                
    movepools = {}
    total = len(pokemon_links)
    count = 0
    
    for name, link in pokemon_links.items():
        count += 1
        page_url = "https://www.serebii.net" + link
        print(f"Fetching {count}/{total}: {name} ({page_url})")
        
        try:
            page_resp = requests.get(page_url, headers=headers)
            page_soup = BeautifulSoup(page_resp.text, 'html.parser')
            
            moves = set()
            for t in page_soup.find_all('table', {'class': 'dextable'}):
                headers_row = t.find('tr')
                if headers_row and 'Standard Moves' in headers_row.text:
                    move_rows = t.find_all('tr')[2:]
                    for m_row in move_rows:
                        m_cols = m_row.find_all('td')
                        if len(m_cols) > 1:
                            m_a = m_cols[0].find('a')
                            if m_a:
                                raw_name = m_a.text.strip()
                                # Clean up names to match PokeAPI style (hyphens to spaces, title case)
                                clean_name = raw_name.replace('-', ' ').title()
                                moves.add(clean_name)
            
            movepools[name] = sorted(list(moves))
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            
        time.sleep(0.1) # Be nice to the server
        
    with open(os.path.join(DATA_DIR, 'movepools.json'), 'w') as f:
        json.dump(movepools, f, indent=4)
        
    print(f"Saved movepools for {len(movepools)} pokemon")

if __name__ == "__main__":
    fetch_movepools()
