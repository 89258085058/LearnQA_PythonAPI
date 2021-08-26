from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(responce: Response, name, expected_value, error_message):
        try:
            responce_as_dict = responce.json()
        except json.JSONDecodeError:
            assert False, f"Responce is not in JSON format. Responce text is '{responce.text}"

        assert name in responce_as_dict, f"Responce JSON doesn't have key '{name}"
        assert responce_as_dict[name] == expected_value, error_message