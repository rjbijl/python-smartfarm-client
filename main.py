from client import Client
from sensor import Sensor

if __name__ == '__main__':
    client = Client()
    devices = client.get_devices()

    for device in devices:
        last_sample = client.get_last_sample(device['id'])
        # print(last_sample)
        sensors = []
        for sensor_object in last_sample['additional_data']:
            # print(sensor_object)
            sensors.append(Sensor(sensor_object['type'], sensor_object['value']))
        #
        for sensor in sensors:
            print(sensor.print())

        break
