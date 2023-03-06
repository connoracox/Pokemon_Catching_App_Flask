import requests
from random import randint


class Pokemon:
    def __init__(self, name, types, weight, abilities):
        self.name = name
        self.types = types
        self.weight = weight
        self.abilities = abilities

def poke_api_call(pokemon):
    # Use the pokemon parameter to make a request to the pokeapi
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')
    # if the status code is 200:
    if response.status_code == 200:
        # Get the pokemon's data with the json method
        data = response.json()
        # Pull out the name, weight, types, abilities
        name = data['name']
        types = data['types']
        types = list(map(lambda x: x['type']['name'], types))
        weight = data['weight']
        abilities = data['abilities']
        abilities = list(map(lambda x: x['ability']['name'], abilities))
        # Create an instance of the Pokemon class
        pokemon = Pokemon(name, types, weight, abilities)
        # Return the instance of the class
        return pokemon
    # if the status code is not 200, print an error message
    else:
        print(f'ERROR, STATUS CODE {response.status_code}')

pokemon1 = poke_api_call('pikachu')
print(pokemon1.types)


# Random number generated for each pokemon id
random_team1 = [randint(1,898) for i in range(10)]

# your_team = ['electabuzz', 'haunter','tyranitar','blaziken','marowak','dragonair']

random_team = list(map(poke_api_call, random_team1))

print(random_team)

for team_member in random_team:
    print(team_member.name)

