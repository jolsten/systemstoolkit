import datetime
from typing import Iterable, Optional
from systemstoolkit.utils import make_command


class SetStateCartesianMixin:
    def set_state_cartesian(
        self,
        epoch: datetime.datetime,
        state: Iterable,
        interval: Optional[tuple[datetime.datetime, datetime.datetime]] = None,
        stepsize: float = 60.0,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        if interval is None:
            interval = 'UseScenarioInterval'

        self.connect.send(make_command([
            'SetState', self.path, 'Cartesian', prop,
            interval, stepsize, coord,
            epoch, state
        ]))


