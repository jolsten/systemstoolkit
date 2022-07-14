from typing import TYPE_CHECKING, Optional
from systemstoolkit.connect.objects.base import Object

if TYPE_CHECKING:
    from systemstoolkit.connect import Connect # pragma: no cover


class Facility(Object):
    def set_position_cartesian(
        self,
        x: float,
        y: float,
        z: float,
    ) -> None:
        self.connect.send(f'SetPosition {self.path} Cartesian {x} {y} {z}')

    def set_position_geodetic(
        self,
        lat: float,
        lon: float,
        alt: float = 0.0,
        msl: bool = False,
    ) -> None:
        command = f'SetPosition {self.path} Geodetic {lat} {lon} {alt}'
        if msl:
            command = command + ' MSL'
        self.connect.send(command)

    def set_position_geocentric(
        self,
        lat: float,
        lon: float,
        alt: float = 0.0,
        msl: bool = False,
    ) -> None:
        command = f'SetPosition {self.path} Geocentric {lat} {lon} {alt}'
        if msl:
            command = command + ' MSL'
        self.connect.send(command)
    
    def set_height_above_ground(self, height: float) -> None:
        command = f'SetHeightAboveGround {self.path} {height}'
        self.connect.send(command)


class Target(Facility):
    pass


class Place(Facility):
    pass
