import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
count = len(response.history)
last_redirect = response.history[-1]
first_redirect = response.history[0]
second_redirect = response.history[1]
third_redirect = response.history[2]
#Выводим сколько редиректов происходит от изначальной точки назначения до итоговой
print('Count_redirect= ', count - 1)
#Выводим какие ULR редиктов до итоговой
print('URL_redirect= ', last_redirect.url, second_redirect.url, third_redirect.url)
#Выврдим итоговый url
print ('last_redirect= ', last_redirect.url)