import requests


url = "https://playground.learnqa.ru/api/homework_header"
response = requests.get(url)
print(response.headers)
headers = response.headers
correct_headers = {
  'Date': 'Wed, 25 Aug 2021 14:00:55 GMT',
  'Content-Type': 'application/json',
  'Content-Length': '15',
  'Connection': 'keep-alive',
  'Keep-Alive': 'timeout=10',
  'Server': 'Apache',
  'x-secret-homework-header': 'Some secret value',
  'Cache-Control': 'max-age=0',
  'Expires': 'Wed, 25 Aug 2021 14:00:55 GMT'
}


url = "https://playground.learnqa.ru/api/homework_header"
headerss = {'x-secret-homework-header': 'Some secret value'}
response1 = requests.head(url, params=headerss)
print(response1.text)
