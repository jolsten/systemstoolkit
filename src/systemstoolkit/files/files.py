import io
import numpy as np
from typing import Union, Optional
from dataclasses import dataclass, asdict
from enforce_typing import enforce_types

from .formats import AttitudeFileFormat
from .keywords import (
    Keyword,
    AttitudeDeviations,
    ScenarioEpoch,
    Coordinate,
    CoordinateAxes,
    CoordinateAxesEpoch,
    MessageLevel,
    CentralBody,
    BlockingFactor,
    Interpolation,
    InitialAttitude,
    TimeFormat,
    TrendingControl,
    NumberOfAttitudePoints,
)


class StkFile:
    version = '11.0'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'


ATTITUDE_FILE_TEMPLATE = '''stk.v.{version}
BEGIN Attitude
{keywords}
{format}
{data}
END Attitude
'''


@enforce_types
@dataclass
class AttitudeFile(StkFile):
    time: Union[list, np.ndarray]
    data: Union[list, np.ndarray]
    format: AttitudeFileFormat
    epoch: Optional[ScenarioEpoch] = None
    message: Optional[MessageLevel] = MessageLevel('Warnings')
    axes: Optional[Coordinate] = Coordinate(CoordinateAxes('ICRF'))
    body: Optional[CentralBody] = CentralBody('Earth')
    interp: Optional[Interpolation] = None
    deviations: Optional[AttitudeDeviations] = None
    blocking: Optional[BlockingFactor] = None
    initial: Optional[InitialAttitude] = None
    time_fmt: Optional[TimeFormat] = None
    trending: Optional[TrendingControl] = None

    def __post_init__(self):
        self.time, self.data = self.format.validate_data(self.time, self.data)
        self.points = NumberOfAttitudePoints(self.data.shape[0])

    def keywords(self) -> str:
        lines = []
        for key in asdict(self).keys():
            keyword_obj = getattr(self, key)
            if isinstance(keyword_obj, Keyword):
                lines.append(str(keyword_obj))
        return '\n'.join(lines) + '\n'

    def format_data(self) -> str:
        buf = io.StringIO()

        if self.epoch is None:
            self.epoch = ScenarioEpoch(self.time[0])
        sse = (self.time - self.epoch.value) / np.timedelta64(1, 's')
        
        for time, row in zip(sse, self.data):
            t = f'{time:15.3f}'
            print(t, ' '.join([f'{x:.6f}'.rjust(15) for x in row]), file=buf)
        
        return buf.getvalue()

    def to_string(self) -> str:
        # Format data first to set epoch if necessary
        formatted_data = self.format_data()

        return ATTITUDE_FILE_TEMPLATE.format(
            version = self.version,
            keywords = self.keywords(),
            format = self.format,
            data = formatted_data,
        )
