import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


@allure.epic("Edit test suite")
class TestEdit(BaseCase):

    @allure.title("This test created user")
    @allure.description("This test successfully - user after creation")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name})
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")


    @allure.title("This test edit user not authorized")
    @allure.description("This test doesn't change the user's data, being unauthorized")
    def test_edit_user_not_authorized(self):
        # REGISTER
        time.sleep(1)
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # POST
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # PUT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name})
        Assertions.assert_code_status(response3, 400)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", first_name,
                                             "Wrong name of the user after edit without authorization")

    @allure.title("This test different use")
    @allure.description("This test change the user's data, being authorized by another user")
    def test_edit_different_user(self):
        # REGISTRATION 1
        register_data_1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name_1 = register_data_1["firstName"]
        email_1 = register_data_1["email"]
        password_1 = register_data_1["password"]
        user_id_1 = self.get_json_value(response1, "id")

        # REGISTRATION 2
        register_data_2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data_2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        first_name_2 = register_data_2["firstName"]
        email_2 = register_data_2["email"]
        password_2 = register_data_2["password"]
        user_id_2 = self.get_json_value(response2, "id")

        # LOGIN 1
        login_data_1 = {
            'email': email_1,
            'password': password_1
        }
        response3 = MyRequests.post("/user/login", data=login_data_1)
        auth_sid_1 = self.get_cookie(response3, 'auth_sid')
        token_1 = self.get_header(response3, 'x-csrf-token')

        # LOGIN 2
        login_data_2 = {
            'email': email_2,
            'password': password_2
        }
        response4 = MyRequests.post("/user/login", data=login_data_2)
        auth_sid_2 = self.get_cookie(response4, 'auth_sid')
        token_2 = self.get_header(response4, 'x-csrf-token')

        # PUT
        new_name = "Changed name"
        response5 = MyRequests.put(f"/user/{user_id_1}",
                                   headers={'x-csrf-token': token_2},
                                   cookies={'auth_sid': auth_sid_2},
                                   data={'firstName': new_name})
        Assertions.assert_code_status(response5, 200)

        # GET USER 1
        response6 = MyRequests.get(f"/user/{user_id_1}",
                                   headers={'x-csrf-token': token_1},
                                   cookies={'auth_sid': auth_sid_1})

        Assertions.assert_json_value_by_name(response6, "firstName", first_name_1,
                                             "Wrong name of the user 1 after edit with different user")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test try to change the user's email, being authorized by the same user, to a new email without the symbol @")
    def test_edit_email_to_invalid_email(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # PUT
        new_email = "Alexandr.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': new_email})
        Assertions.assert_code_status(response3, 400)
        assert response3.text == 'Invalid email format', "Unexpected response text for invalid email"

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assertions.assert_json_value_by_name(response4, "email", email, "Wrong email of the user after edit")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test  try to change the user's firstName, being authorized by the same user, to a very short value of one character")
    def test_edit_user_name_to_invalid_name(self):
        # REGISTER
        time.sleep(1)
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_name = register_data["firstName"]
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # PUT
        new_name = "U"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name})
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Too short value for field firstName",
                                             "Unexpected response for too short name")

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", first_name, "Wrong email of the user after edit")