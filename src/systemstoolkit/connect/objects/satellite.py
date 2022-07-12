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
