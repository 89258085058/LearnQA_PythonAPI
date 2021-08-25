import requests

header = {'x-secret-homework-header': 'Some secret value'}

url = "https://playground.learnqa.ru/api/homework_header"
response = requests.get(url, params=header)
response_header = response.text
response1 = '{"success":"!"}'

assert response_header == response1, f"HEADER: {response_header} does not match the expected one"

