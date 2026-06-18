import requests
import json

def fetch_movepools():
    url = "https://beta.pokeapi.co/graphql/v1beta"
    query = """
    query {
      pokemon_v2_pokemon {
        name
        pokemon_v2_pokemonmoves {
          pokemon_v2_move {
            name
          }
        }
      }
    }
    """
    response = requests.post(url, json={'query': query})
    data = response.json()
    
    movepools = {}
    for pokemon in data['data']['pokemon_v2_pokemon']:
        name = pokemon['name'].replace('-', ' ').title()
        moves = set()
        for move_edge in pokemon['pokemon_v2_pokemonmoves']:
            if move_edge['pokemon_v2_move']:
                move_name = move_edge['pokemon_v2_move']['name'].replace('-', ' ').title()
                moves.add(move_name)
        movepools[name] = list(moves)
        
    with open('movepools.json', 'w') as f:
        json.dump(movepools, f, indent=4)
        
    print(f"Saved movepools for {len(movepools)} pokemon")

if __name__ == "__main__":
    fetch_movepools()
