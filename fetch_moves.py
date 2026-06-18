import requests
import json

def fetch_moves_graphql():
    url = "https://beta.pokeapi.co/graphql/v1beta"
    query = """
    query {
      pokemon_v2_move {
        name
        power
        accuracy
        pokemon_v2_type {
          name
        }
        pokemon_v2_movedamageclass {
          name
        }
      }
    }
    """
    response = requests.post(url, json={'query': query})
    data = response.json()
    
    moves = {}
    for move in data['data']['pokemon_v2_move']:
        name = move['name'].replace('-', ' ').title()
        power = move['power']
        accuracy = move['accuracy']
        type_name = move['pokemon_v2_type']['name'].title() if move['pokemon_v2_type'] else 'Unknown'
        damage_class = move['pokemon_v2_movedamageclass']['name'].title() if move['pokemon_v2_movedamageclass'] else 'Unknown'
        
        moves[name] = {
            'power': power,
            'accuracy': accuracy,
            'type': type_name,
            'category': damage_class
        }
        
    with open('moves.json', 'w') as f:
        json.dump(moves, f, indent=4)
        
    print(f"Saved {len(moves)} moves to moves.json")

if __name__ == "__main__":
    fetch_moves_graphql()