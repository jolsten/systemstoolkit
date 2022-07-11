import datetime
import numpy as np
from typing import Iterable, Optional
from systemstoolkit.utils import stk_datetime


def make_command(parts: Iterable) -> str:
    fmt_parts = []
    for p in parts:
        if isinstance(p, str):
            fmt_parts.append(p)
        elif isinstance(p, (datetime.datetime, np.datetime64)):
            fmt_parts.append(
                f'"{stk_datetime(p)}"'
            )
        elif isinstance(p, Iterable):
            fmt_parts.append(make_command(p))
        else:
            fmt_parts.append(str(p))
    return ' '.join(fmt_parts)


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
