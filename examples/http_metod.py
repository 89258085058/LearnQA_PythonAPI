import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url)
token_info = response.json().get("token")
token = {"token": token_info}

response1 = requests.get(url, params=token)
status = response1.json().get("status")
if status == 'Job is NOT ready':
    time_info = response.json().get("seconds")
    time.sleep(time_info)

    response2 = requests.get(url, params=token)
    status2 = response2.json().get("status")
    if status2 == 'Job is ready' and "result" in response2.text:
        print(response2.text)
    else:
        print("error response2")

else:
    print("error response1")




