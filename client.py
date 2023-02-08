from database import Database
from getpass import getpass
from sensor import Sensor
import logging
import requests


class Client:
    """ SmartFarm API client

    API client to connect to the SmartFarm APIs. Only the public methods should be used
    """

    def __init__(self, api_url:str, db: Database):
        self.api_url = api_url
        self.db = db
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

        refresh_token = self.db.get_refresh_token(username)
        if refresh_token is not None:
            if self.__do_refresh_request(username, refresh_token):
                return True
            else:
                logging.info('Refreshing unsuccessful, going with standard authentication')

        password = getpass('Password: ')

        headers = {'Content-Type': 'application/json'}
        body = {'_username': username, '_password': password}

        url = self.api_url + '/login_check'
        response = requests.post(url, json=body, headers=headers)

        return self.__handle_authentication_response(response, username)

    def __do_refresh_request(self, username: str, refresh_token: str) -> bool:
        body = {'refresh_token': refresh_token}
        url = self.api_url + '/token/refresh'
        response = requests.post(url, data=body)

        return self.__handle_authentication_response(response, username)

    def __handle_authentication_response(self, response, username:str) -> bool:
        if 200 == response.status_code:
            data = response.json()
            self.token = data['token']
            self.refresh_token = data['refresh_token']
            self.db.save_refresh_token(username, self.refresh_token)
            return True
        else:
            print('Invalid credentials')
            return False
