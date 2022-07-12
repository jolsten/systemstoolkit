from .base import Vehicle
from .sensor import Sensor
from .mixins import SatelliteStateMixin


class Satellite(Vehicle, SatelliteStateMixin):
    _COORD_SYSTEM = (
        'ICRF', 'J2000', 'MeanOfDate', 'TrueOfDate',
        'B1950', 'TEMEOfDate', 'TEMEOfEpoch', 'AlignmentAtEpoch',
    )

    _PROPAGATOR = (
        'TwoBody', 'J2Perturbation', 'J4Perturbation', 'HPOP', 'LOP',
    )

    def new_sensor(self, name: str) -> Sensor:
        object_path = f'{self.path}/Sensor/{name}'
        obj = Sensor(self.connect, object_path)
        obj.create()
        return obj
