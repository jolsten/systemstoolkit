import datetime
from typing import Iterable, Optional, Union, TYPE_CHECKING
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
        state: Iterable[Union[float, str]],
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        """Set the state of a Vehicle using Cartesian coordinates.

        Params
        ------
        epoch: datetime.datetime
            Epoch time for the state vector.
        
        state: Iterable[float]
            The 6-element cartesian state vector as a list or tuple, for instance. Elements are as follows:

                X-Position [m]
                Y-Position [m]
                Z-Position [m]
                X-Velocity [m/s]
                Y-Velocity [m/s]
                Z-Velocity [m/s]

        interval: TimeInterval
            The time interval for the propagator.
        
        stepsize: float
            The orbit propagator step size in seconds.
        
        prop: str
            The propagator to use. Choices: {self._PROPAGATOR}
        
        coord: str
            The coordinate system to use. Choices: {self._COORD_SYSTEM}

        Returns
        -------
        None
        """
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
        state: Iterable[Union[float, str]],
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        """Set the state of a Vehicle using Classical orbital elements.

        Params
        ------
        epoch: datetime.datetime
            Epoch time for the state vector.
        
        state: Iterable[float]
            The 6-element classical orbital elements as a list or tuple, for instance. Elements are as follows:

                Semi-Major Axis     [m]
                Eccentricity        [-]
                Inclination         [-]
                Argument of Perigee [deg]
                RAAN                [deg]
                Mean Anomaly        [deg]

        interval: TimeInterval
            The time interval for the propagator.
        
        stepsize: float
            The orbit propagator step size in seconds.
        
        prop: str
            The propagator to use. Choices: {self._PROPAGATOR}
        
        coord: str
            The coordinate system to use. Choices: {self._COORD_SYSTEM}

        Returns
        -------
        None
        """

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
        state: Iterable[Union[float, str]],
        direction: str = 'Posigrade',
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        f"""Set the state of a Vehicle using Equinoctial elements.
        
        Params
        ------
        epoch: datetime.datetime
            Epoch time for the state vector.
        
        state: Iterable[float]
            The 6-element equinoctial element vector as a list or tuple, for instance. Elements are as follows:

                Semi-Major Axis [m]
                h               [-]
                k               [-]
                p               [-]
                q               [-]
                Mean Longitude  [deg]

        direction: str
            Equinoctial elements require a direction. Choices: {EQUI_DIRECTIONS}.

        interval: TimeInterval
            The time interval for the propagator.
        
        stepsize: float
            The orbit propagator step size in seconds.
        
        prop: str
            The propagator to use. Choices: {self._PROPAGATOR}
        
        coord: str
            The coordinate system to use. Choices: {self._COORD_SYSTEM}

        Returns
        -------
        None
        """
        if prop.lower() not in [x.lower() for x in self._PROPAGATOR]:
            raise ValueError(f'Propagator "{prop}" not in {self._PROPAGATOR}')
        
        if coord.lower() not in [x.lower() for x in self._COORD_SYSTEM]:
            raise ValueError(f'Coordinate System "{coord}" not in {self._COORD_SYSTEM}')

        if direction.lower() not in [x.lower() for x in EQUI_DIRECTIONS]:
            raise ValueError(f'Direction "{direction}" not in {EQUI_DIRECTIONS}')

        self.connect.send(make_command([
            'SetState', self.path, 'Equi', prop,
            interval, stepsize, coord,
            epoch, state, direction,
        ]))


class SetStateFromFileMixin:
    def set_state_from_file(
        self: Vehicle,
        filepath: str,
        epoch: Optional[datetime.datetime] = None,
    ) -> None:
        f"""Set the state of a Vehicle using an External File.
        
        Params
        ------
        epoch: Optional[datetime.datetime]
            Overwrite the start time for the data file.

        Returns
        -------
        None
        """
        cmds = [
            'SetState', self.path, 'FromFile', f'"{filepath}"',
        ]

        if epoch is not None:
            cmds.extend(['StartTime', epoch])

        self.connect.send(make_command(cmds))


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
        ssc: int,
        file: str = None,
        interval: TimeInterval = 'UseScenarioInterval',
        stepsize: float = 60,
    ) -> None:
        """Set the state of a Vehicle using an SGP4 TLE.
        
        Params
        ------
        ssc: int
            Space Surveillance Catalog Number of the desired TLE.
        
        file: Optional[str]
            If None, then the AGI database is used.

            Otherwise, file must be a path to the TLE file.

        interval: TimeInterval
            The time interval for the propagator.
        
        stepsize: float
            The orbit propagator step size in seconds.

        Returns
        -------
        None
        """
        if file is None:
            source = 'AGIServer'
        else:
            file = f'File "{file}"'

        self.connect.send(make_command([
            'SetState', self.path, 'SGP4', interval, stepsize, ssc,
            f'TLESource Automatic Source {source} UseTLE All SwitchMethod TCA',
        ]))


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
