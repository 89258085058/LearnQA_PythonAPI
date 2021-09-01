import requests

def test_check_correct_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    response_cookie = dict(response.cookies)
    correct_cookie = {'HomeWork': 'hw_value'}
    assert response_cookie == correct_cookie, f" this value: {response_cookie} does not match the expected value"


