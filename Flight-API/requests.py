import requests

# URL da rota para adicionar passageiro no seu aplicativo Flask
url = 'http://localhost:5000/adicionar_passageiro'

# Dados do passageiro a serem enviados no corpo da requisição
data = {
    'nome': 'Maria',
    'sobrenome': 'Silva',
    'email': 'maria@example.com',
    'telefone': '9784567'
}

# Fazendo a requisição POST
response = requests.post(url, json=data)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    resposta_json = response.json()
    print(resposta_json['mensagem'])
else:
    print("Erro ao adicionar passageiro:", response.text)
