from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(responce: Response, name, expected_value, error_message):
        try:
            responce_as_dict = responce.json()
        except json.JSONDecodeError:
            assert False, f"Responce is not in JSON format. Responce text is '{responce.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"
        assert responce_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            responce_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Responce is not in JSON format. Responce text is '{response.text}'"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"

    @staticmethod
    def assert_code_status(responce: Response, expected_status_code):
        assert responce.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {responce.status_code}"

    @staticmethod
    def assert_json_has_not_key(responce: Response, name):
        try:
            responce_as_dict = responce.json()
        except json.JSONDecodeError:
            assert False, f"Responce is not in JSON format. Responce text is '{responce.text}'"

        assert name not in responce_as_dict, f"Responce JSON shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            responce_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Responce is not in JSON format. Responce text is '{response.text}'"
        for name in names:
            assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}'"


