from client import Client
from database import Database
import logging


def main():
    logging.basicConfig(filename='pythonlog.log', encoding='utf-8', level=logging.INFO)

    database = Database(db_path='./smartfarm.db')
    client = Client(api_url='https://smartfarm.appsforagri.com/api', db=database)
    sensors = client.get_all_data_sources()

    devices = client.get_devices()
    if not devices:
        exit()

    print()
    for device in devices:
        print(f'Device: {device["name"]}')
        logging.info(device)
        database.save_device(device)

        if None == (last_sample := client.get_last_sample(device['id'])):
            print('No recent data')
            print('========================')
            print()
            continue

        print(f'Timestamp: {last_sample["date_time"]}')
        for data_point in last_sample['data_points']:
            sensor = sensors[data_point['sensor']]
            print(f'{sensor.name}: {data_point["rounded_value"]} {sensor.unit}')
        for additional_data in last_sample['additional_data']:
            sensor = sensors[additional_data['type']]
            print(f'{sensor.name}: {additional_data["value"]} {sensor.unit}')

        print('========================')
        print()


if __name__ == '__main__':
    main()
