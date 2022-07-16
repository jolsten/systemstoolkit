from typing import Optional, Union
from .base import Attachment


_SENSOR_TYPES = {
    'Conical': 'conical',
    'HalfPower': 'half_power',
    'Custom': 'custom',
    'Rectangular': 'rectangular',
    'SAR': 'sar',
    'SimpleCone': 'simple_cone',
}


class Sensor(Attachment):
    def define(
        self: Attachment,
        type: str,
        *args,
        **kwargs,
    ) -> None:
        if type.lower() not in [t.lower() for t in _SENSOR_TYPES.keys()]:
            raise ValueError(f'Sensor type "{type}" not in "{list(_SENSOR_TYPES.keys())}"')
        
        getattr(self, f'define_{_SENSOR_TYPES[type]}')

    def define_conical(
        self: Attachment,
        inner_half: float,
        outer_half: float,
        min_clock: float,
        max_clock: float,
        resolution: Optional[float] = None,
    ) -> None:
        command = f'Define {self.path} Conical {inner_half} {outer_half} {min_clock} {max_clock}'
        if resolution is not None:
            command += f' AngularRes {resolution}'
        self.connect.send(command)

    def define_half_power(
        self: Attachment,
        frequency: float,
        diameter: float,
        resolution: Optional[float] = None,
    ) -> None:
        command = f'Define {self.path} HalfPower {frequency} {diameter}'
        if resolution is not None:
            command += f' AngularRes {resolution}'
        self.connect.send(command)

    def define_custom(
        self: Attachment,
        file_path: str,
    ) -> None:
        command = f'Define {self.path} Custom "{file_path}"'
        self.connect.send(command)

    def define_rectangular(
        self: Attachment,
        vertical_half: float,
        horizontal_half: float,
        resolution: Optional[float] = None,
    ) -> None:
        command = f'Define {self.path} Rectangular {vertical_half} {horizontal_half}'
        if resolution is not None:
            command += f' AngularRes {resolution}'
        self.connect.send(command)

    def define_sar(
        self: Attachment,
        min_elevation: float,
        max_elevation: float,
        forward_exclusion: float,
        aft_exclusion: float,
        parent_altitude: Optional[Union[str, float]] = None,
        resolution: Optional[float] = None,
    ) -> None:
        command = f'Define {self.path} SAR {min_elevation} {max_elevation} {forward_exclusion} {aft_exclusion}'
        if parent_altitude is not None:
            raise NotImplementedError

        if resolution is not None:
            command += f' AngularRes {resolution}'
        self.connect.send(command)

    def define_simple_cone(
        self: Attachment,
        cone_angle: float,
        resolution: Optional[float] = None,
    ) -> None:
        command = f'Define {self.path} SimpleCone {cone_angle}'
        if resolution is not None:
            command += f' AngularRes {resolution}'
        self.connect.send(command)
