import datetime
from typing import Iterable, Optional, TYPE_CHECKING
from systemstoolkit.utils import make_command
from systemstoolkit.typing import TimeInterval
from systemstoolkit.connect.objects.base import Vehicle

EQUI_DIRECTIONS = ('Retrograde', 'Posigrade')


class SetState11ParameterMixin:
    def set_state_11_parameter(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateCartesianMixin:
    def set_state_cartesian(
        self: Vehicle,
        epoch: datetime.datetime,
        state: Iterable,
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        if prop not in self._PROPAGATOR:
            raise ValueError(f'Propagator "{prop}" not in {self._PROPAGATOR}')
        
        if coord not in self._COORD_SYSTEM:
            raise ValueError(f'Coordinate System "{coord}" not in {self._COORD_SYSTEM}')

        self.connect.send(make_command([
            'SetState', self.path, 'Cartesian', prop,
            interval, stepsize, coord,
            epoch, state
        ]))


class SetStateClassicalMixin:
    def set_state_classical(
        self: Vehicle,
        epoch: datetime.datetime,
        state: Iterable,
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        if prop not in self._PROPAGATOR:
            raise ValueError(f'Propagator "{prop}" not in {self._PROPAGATOR}')
        
        if coord not in self._COORD_SYSTEM:
            raise ValueError(f'Coordinate System "{coord}" not in {self._COORD_SYSTEM}')

        self.connect.send(make_command([
            'SetState', self.path, 'Classical', prop,
            interval, stepsize, coord,
            epoch, state
        ]))


class SetStateEquiMixin:
    def set_state_equi(
        self: Vehicle,
        epoch: datetime.datetime,
        state: Iterable,
        direction: str = 'Posigrade',
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        if prop not in self._PROPAGATOR:
            raise ValueError(f'Propagator "{prop}" not in {self._PROPAGATOR}')
        
        if coord not in self._COORD_SYSTEM:
            raise ValueError(f'Coordinate System "{coord}" not in {self._COORD_SYSTEM}')

        if direction not in EQUI_DIRECTIONS:
            raise ValueError(f'Direction "{direction}" not in {EQUI_DIRECTIONS}')

        self.connect.send(make_command([
            'SetState', self.path, 'Classical', prop,
            interval, stepsize, coord,
            epoch, state
        ]))


class SetStateFromFileMixin:
    def set_state_from_file(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateGPSMixin:
    def set_state_gps(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateMixedSphericalMixin:
    def set_state_mixed_spherical(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateSGP4Mixin:
    def set_state_sgp4(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateSimpleAscentMixin:
    def set_state_simple_ascent(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateSP3Mixin:
    def set_state_sp3(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateSPICEMixin:
    def set_state_spice(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateSphericalMixin:
    def set_state_spherical(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SetStateTLEMixin:
    def set_state_tle(
        self: Vehicle,
        *args,
        **kwargs,
    ) -> None:
        raise NotImplementedError


class SatelliteStateMixin(
    SetState11ParameterMixin,
    SetStateCartesianMixin,
    SetStateClassicalMixin,
    SetStateEquiMixin,
    SetStateFromFileMixin,
    SetStateGPSMixin,
    SetStateMixedSphericalMixin,
    SetStateSGP4Mixin,
    SetStateSP3Mixin,
    SetStateSPICEMixin,
    SetStateSphericalMixin,
    SetStateTLEMixin,
):
    pass


class MissileStateMixin(
    SetStateCartesianMixin,
    SetStateClassicalMixin,
    SetStateEquiMixin,
    SetStateFromFileMixin,
    SetStateMixedSphericalMixin,
    SetStateSphericalMixin,
):
    pass


class LaunchVehicleStateMixin(
    SetStateFromFileMixin,
    SetStateSimpleAscentMixin,
):
    pass
