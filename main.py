from client import Client
from sensor import Sensor
import logging

def main():
    logging.basicConfig(filename='pythonlog.log', encoding='utf-8', level=logging.INFO)

    client = Client()

    sensors = {}
    for sensor in client.get_sensors():
        sensors[sensor['id']] = Sensor(sensor['id'], sensor['name'], sensor['units'])

    for additional_data_type in client.get_additional_data_types():
        sensors[additional_data_type['id']] = Sensor(additional_data_type['id'],
                                                     additional_data_type['name'],
                                                     additional_data_type['unit'])

    devices = client.get_devices()
    if not devices:
        exit()

    print()
    for device in devices:
        print(f'Device: {device["name"]}')
        logging.info(device)

        if not (last_sample := client.get_last_sample(device['id'])):
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
