import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.serebii.net/pokedex-champions/snorlax/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

moves = set()
for table in soup.find_all('table', {'class': 'dextable'}):
    headers_row = table.find('tr')
    if headers_row and 'Standard Moves' in headers_row.text:
        # The next row usually has the column headers (Attack Name, Type, Cat, etc.)
        # The rows after that are the actual moves. But wait, in Serebii, sometimes each move is 2 rows (one for stats, one for description).
        # Or maybe it's just one row for stats.
        rows = table.find_all('tr')[2:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                a_tag = cols[0].find('a')
                if a_tag:
                    moves.add(a_tag.text.strip())

print(sorted(list(moves))[:10])
print("Total:", len(moves))
