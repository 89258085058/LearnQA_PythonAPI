import pytest
import requests


class UserAgent:
    headers = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
    ]
    @pytest.mark.parametrize("User-Agent", headers)
    def test_user_agent_header(self, header):

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"User-Agent": header}
        response = requests.get(url, headers= data)
        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert 'platform' in response_dict, "There is not filed 'platform' in the response"
        assert 'browser' in response_dict, "There is not filed 'browser' in the response"
        assert 'device' in response_dict, "There is not filed 'device' in the response"

        if len(header) == 0:
            expected_response_text = "platform, someone"
            expected_response_text1 = "browser, someone"
            expected_response_text2 = "device, someone"
        else:
            expected_response_text = f"platform, {header}"
            expected_response_text1 = f"browser, {header}"
            expected_response_text2 = f"device, {header}"


        actual_response_text = response_dict['platform']
        actual_response_text1 = response_dict['browser']
        actual_response_text2 = response_dict['device']

        assert actual_response_text == expected_response_text, "Actual text in the response 'platform' is not correct"
        assert actual_response_text1 == expected_response_text1, "Actual text in the response 'browser' is not correct"
        assert actual_response_text2 == expected_response_text2, "Actual text in the response 'device' is not correct"