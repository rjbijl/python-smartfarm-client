class Sensor:

    TYPE_HUMIDITY_25 = 'rh25'
    TYPE_UNKNOWN = 'unknown'

    def __init__(self, name, value):
        self.type = name #self.__get_type_from_name(name)
        self.value = value

    def print(self):
        return f'{self.type}: {self.value}'

    def __get_type_from_name(self, name) -> str:
        if name == 'dew_point_25' or name == 'RH4':
            return TYPE_HUMIDITY_25
        else:
            return TYPE_UNKNOWN

