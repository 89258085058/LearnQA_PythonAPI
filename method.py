import requests

#1. Делает http-запрос любого типа без параметра method
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

#2. Делает http-запрос не из списка. Например, HEAD
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"HEAD"})
print(response.text)

#3. Делает запрос с правильным значением method
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":"GET"})
print(response.text)
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"POST"})
print(response.text)
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"PUT"})
print(response.text)
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":"DELETE"})
print(response.text)

#4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
map = [
    {'method': 'GET'},
    {'method': 'POST'},
    {'method': 'DELETE'},
    {'method': 'PUT'},
]

for data in map:
    print("get " + requests.get(url, params=data).text)

for data in map:
    print("post " +requests.post(url, data=data).text)

for data in map:
    print("put " +requests.put(url, data=data).text)

for data in map:
    print("delete " +requests.delete(url, data=data).text)