import requests

data = requests.get('http://localhost:8000/example.json').json()
print(data)
print()

in_values = {'username':'Name','password':'pass'}

res = requests.post('http://localhost:8000', json=in_values)
print(res.text)


