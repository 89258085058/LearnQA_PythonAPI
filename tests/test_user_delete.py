from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import allure
import time



@allure.epic("Delete test suite")
class TestUserDelete(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test attempt to delete a user by ID 2")
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response for delete user with ID 1, 2, 3, 4 or 5."

        response3 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        expected_fields = ["username", "firstName", "lastName", "email"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Create a user, log in from under him, delete, then try to get his data by ID and make sure that the user is really deleted")
    def test_delete_created_user_get_his_data(self):
        # REGISTRATION
        time.sleep(1)
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

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

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", f"Unexpected response for getting deleted user"

    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.description("This test try to delete a user while being authorized by another user")
    def test_delete_being_authorized_by_another_user(self):
        # REGISTRATION USER 1
        register_data_1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        username_1 = register_data_1["username"]
        first_name_1 = register_data_1["firstName"]
        last_name_1 = register_data_1["lastName"]
        email_1 = register_data_1["email"]
        password_1 = register_data_1["password"]
        user_id_1 = self.get_json_value(response1, "id")

        # REGISTRATION USER 2
        register_data_2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data_2)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        username_2 = register_data_1["username"]
        first_name_2 = register_data_1["firstName"]
        last_name_2 = register_data_1["lastName"]
        email_2 = register_data_2["email"]
        password_2 = register_data_2["password"]
        user_id_2 = self.get_json_value(response2, "id")

        # LOGIN USER 1
        login_data_1 = {
            'email': email_1,
            'password': password_1
        }
        response3 = MyRequests.post("/user/login", data=login_data_1)
        auth_sid_1 = self.get_cookie(response3, 'auth_sid')
        token_1 = self.get_header(response3, 'x-csrf-token')

        # LOGIN USER 2
        login_data_2 = {
            'email': email_2,
            'password': password_2
        }
        response4 = MyRequests.post("/user/login", data=login_data_2)
        auth_sid_2 = self.get_cookie(response4, 'auth_sid')
        token_2 = self.get_header(response4, 'x-csrf-token')

        # DELETE
        response5 = MyRequests.delete(f"/user/{user_id_1}",
                                      headers={'x-csrf-token': token_2},
                                      cookies={'auth_sid': auth_sid_2}
                                      )
        Assertions.assert_code_status(response5, 200)

        # GET USER 1
        response6 = MyRequests.get(f"/user/{user_id_1}",
                                   headers={'x-csrf-token': token_1},
                                   cookies={'auth_sid': auth_sid_1})
        Assertions.assert_code_status(response6, 200)

        Assertions.assert_json_value_by_name(response6, "username", username_1,
                                             "Wrong username of the user 1 after delete with different user")
        Assertions.assert_json_value_by_name(response6, "firstName", first_name_1,
                                             "Wrong first name of the user 1 after delete with different user")
        Assertions.assert_json_value_by_name(response6, "lastName", last_name_1,
                                             "Wrong last name of the user 1 after delete with different user")
        Assertions.assert_json_value_by_name(response6, "email", email_1,
                                             "Wrong email of the user 1 after delete with different user")