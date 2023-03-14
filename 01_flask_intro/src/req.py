import requests
import json


resp = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
data = json.loads(resp.content)
print(data)