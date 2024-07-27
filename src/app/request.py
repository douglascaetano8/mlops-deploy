import requests
import requests.auth

url = "http://127.0.0.1:5000/cotacao/"
dados = {
    "garagem": 2,
    "tamanho": 120,
    "ano": 2001
}

auth = requests.auth.HTTPBasicAuth("douglas", "123456")

response = requests.post(url, json=dados, auth=auth)
print(response.json())