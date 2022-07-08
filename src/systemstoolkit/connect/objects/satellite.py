from .base import Vehicle
from .sensor import Sensor


class Satellite(Vehicle):
    def new_sensor(self, name: str) -> Sensor:
        object_path = f'{self.path}/Sensor/{name}'
        obj = Sensor(self.connect, object_path)
        obj.create()
        return obj
