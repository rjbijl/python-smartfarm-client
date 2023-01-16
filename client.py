from getpass import getpass
import json
import requests


class Client:
    """ SmartFarm API client

    API client to connect to the SmartFarm APIs. Only the public methods should be used
    """

    def __init__(self):
        self.api_url = 'https://smartfarm.appsforagri.com/api'
        self.token = None

    def get_devices(self) -> dict:
        return self.__do_authenticated_request('/devices')

    def get_additional_data_types(self) -> dict:
        return self.__do_authenticated_request('/additional-data-types')

    def get_sensors(self) -> dict:
        return self.__do_authenticated_request('/sensors')

    def get_last_sample(self, device_id: int):
        return self.__do_authenticated_request(f'/samples/device/{device_id}/last')

    def __do_authenticated_request(self, path: str) -> dict:
        if self.token is None and not self.__do_authentication_request():
            return False

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + path, headers=headers)
        if 200 != response.status_code:
            return False

        return response.json()

    def __do_request(self, path: str) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + path, headers=headers)
        if 200 != response.status_code:
            return False

        return response.json()

    def __do_authentication_request(self) -> bool:
        username = input('Username: ')
        password = getpass('Pasword: ')

        headers = {'Content-Type': 'application/json'}
        body = {'_username': username, '_password': password}

        url = self.api_url + '/login_check'
        response = requests.post(url, json=body, headers=headers)

        if 200 == response.status_code:
            self.token = response.json()['token']
            return True
        else:
            print('Invalid credentials')
            return False
