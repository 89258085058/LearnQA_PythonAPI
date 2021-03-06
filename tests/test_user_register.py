from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import pytest

params = [
    ("username"),
    ("firstName"),
    ("lastName"),
    ("email"),
    ("password")
]

@allure.epic("Authorization cases")
class TestUserRegister(BaseCase):

    @allure.description("This test successfully authorize user by email and password")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


    @allure.description("This test doesn't register user with email without '@'")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotov-example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"



    @allure.description("This test doesn't register user missed param")
    @pytest.mark.parametrize('param', params)
    def test_create_user_without_param(self, param):
        data = self.prepare_registration_data()
        data.pop(param)
        missed_param = data
        response = MyRequests.post("/user/", data=missed_param)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {param}", \
            f"Unexpected response content {response.content} with missed param: {param}"


    @allure.description("This test doesn't register user with short name")
    def test_creating_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'L'
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
            f"Unexpected response content for field 'firstName' when it is too short"


    @allure.description("This test doesn't register user with a very long name-longer than 250 characters")
    def test_create_user_long_name(self):
        data = self.prepare_registration_data()
        long_name = ""
        while len(long_name) <= 250:
            long_name += "l"
        data['firstName'] = long_name
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"Unexpected response content for field 'firstName' when it is too long"
