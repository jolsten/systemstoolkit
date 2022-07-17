from .base import Vehicle
from .mixins.states import SatelliteStateMixin, SatelliteConstraintMixin


class Satellite(Vehicle, SatelliteStateMixin, SatelliteConstraintMixin):
    _COORD_SYSTEM = (
        'ICRF', 'J2000', 'MeanOfDate', 'TrueOfDate',
        'B1950', 'TEMEOfDate', 'TEMEOfEpoch', 'AlignmentAtEpoch',
    )

    _PROPAGATOR = (
        'TwoBody', 'J2Perturbation', 'J4Perturbation', 'HPOP', 'LOP',
    )
