import requests

POKEAPI_URL = 'https://pokeapi.co/api/v2/'

def get_pokemon(pokemon_name):
    url = f"{POKEAPI_URL}pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    if response.ok:
        pokemon_data = response.json()
        return pokemon_data
    else:
        raise Exception(f"Unable to retrieve data for Pokemon {pokemon_name}: {response.content}")

def get_moves(move_names):
    moves_data = []
    for move_name in move_names:
        url = f"{POKEAPI_URL}move/{move_name.lower()}/"
        response = requests.get(url)
        if response.ok:
            move_data = response.json()
            moves_data.append(move_data)
        else:
            raise Exception(f"Unable to retrieve data for move {move_name}: {response.content}")
    return moves_data

def get_types(type_names):
    types_data = []
    for type_name in type_names:
        url = f"{POKEAPI_URL}type/{type_name.lower()}/"
        response = requests.get(url)
        if response.ok:
            type_data = response.json()
            types_data.append(type_data)
        else:
            raise Exception(f"Unable to retrieve data for type {type_name}: {response.content}")
    return types_data