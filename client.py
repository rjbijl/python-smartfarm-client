from getpass import getpass
from sensor import Sensor
import json
import requests


class Client:
    """ SmartFarm API client

    API client to connect to the SmartFarm APIs. Only the public methods should be used
    """

    def __init__(self):
        self.api_url = 'https://smartfarm.appsforagri.com/api'
        self.token = None
        self.refresh_token = None

    def get_devices(self) -> dict | None:
        return self.__do_authenticated_request('/devices')

    def get_all_data_sources(self) -> dict:
        sensors = {}
        for sensor in self.get_sensors():
            sensors[sensor['id']] = Sensor(sensor['id'], sensor['name'], sensor['units'])

        for additional_data_type in self.get_additional_data_types():
            sensors[additional_data_type['id']] = Sensor(additional_data_type['id'],
                                                         additional_data_type['name'],
                                                         additional_data_type['unit'])
        return sensors

    def get_additional_data_types(self) -> dict | None:
        return self.__do_authenticated_request('/additional-data-types')

    def get_sensors(self) -> dict | None:
        return self.__do_authenticated_request('/sensors')

    def get_last_sample(self, device_id: int) -> dict | None:
        return self.__do_authenticated_request(f'/samples/device/{device_id}/last')

    def __do_authenticated_request(self, path: str) -> dict | None:
        if self.token is None and not self.__do_authentication_request():
            return None

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + path, headers=headers)
        if 200 != response.status_code:
            return None

        return response.json()

    def __do_request(self, path: str) -> dict | None:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + path, headers=headers)
        if 200 != response.status_code:
            return None

        return response.json()

    def __do_authentication_request(self) -> bool:
        username = input('Username: ')
        password = getpass('Password: ')

        headers = {'Content-Type': 'application/json'}
        body = {'_username': username, '_password': password}

        url = self.api_url + '/login_check'
        response = requests.post(url, json=body, headers=headers)

        if 200 == response.status_code:
            self.token = response.json()['token']
            self.refresh_token = response.json()['refresh_token']
            return True
        else:
            print('Invalid credentials')
            return False
