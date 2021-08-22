import requests
from json import loads, dumps

API_KEY = 'AIzaSyAemadkCuLLWhPAI7jBgLQIOC56yGjSNXU'
URL = 'https://www.googleapis.com/books/v1/volumes?'
search_type = 'isbn'
search = '1635576059'
querystring = f'q={search_type}:{search}&key={API_KEY}'
res = requests.get(f'{URL}{querystring}')
l = loads(res.content)
print(dumps(l))
