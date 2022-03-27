import requests
from pprint import pprint
# import json

url = 'https://api.github.com/users/eugen/repos'

response = requests.get(url)

j_data = response.json()

# with open('result.json', 'w') as fp:
#   json.dump(j_data, fp)

res = [sub['name'] for sub in j_data]

pprint(res)





