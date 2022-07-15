import datetime
from typing import Iterable, Optional, Union, TYPE_CHECKING
from systemstoolkit.utils import make_command
from systemstoolkit.typing import TimeInterval
from systemstoolkit.connect.objects.base import Object, Vehicle, Location

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
            source = f'File "{file}"'

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


class BaseConstraintMixin:
    def _set_constraint_minmax(
        self: Object,
        constraint_name: str,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        if min is None:
            min = 'Off'
        
        if max is None:
            max = 'Off'

        command = f'SetConstraint {self.path} {constraint_name} Min {min} Max {max}'
        self.connect.send(command)

    def _set_constraint_value(
        self: Object,
        constraint_name: str,
        value: Optional[float] = None,
    ) -> None:
        if value is None:
            value = 'Off'

        command = f'SetConstraint {self.path} {constraint_name} {value}'
        self.connect.send(command)


class BasicConstraintMixin:
    def set_constraint_azimuth(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Azimuth Angle constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('AzimuthAngle', min=min, max=max)

    def set_constraint_elevation(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Elevation Angle constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('ElevationAngle', min=min, max=max)

    def set_constraint_range(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Range constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('Range', min=min, max=max)

    def set_constraint_range_rate(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Range Rate constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('RangeRate', min=min, max=max)

    def set_constraint_angular_rate(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Angular Rate constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('AngularRate', min=min, max=max)

    def set_constraint_altitude(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Altitude constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('Altitude', min=min, max=max)

    def set_constraint_propagation_delay(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Propagation Delay constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('PropagationDelay', min=min, max=max)


class SunConstraintMixin:
    def set_constraint_sun_elevation_angle(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Sun Elevation Angle constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('SunElevationAngle', min=min, max=max)

    def set_constraint_lunar_elevation_angle(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Lunar Elevation Angle constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('LunarElevationAngle', min=min, max=max)

    def set_constraint_los_sun_illumination_angle(
        self: Object,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Line of Sight (LOS) Sun Illumination Angle constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('LOSSunIlluminationAngle', min=min, max=max)
    
    def set_constraint_los_sun_exclusion(
        self: Object,
        value: Optional[float] = None,
    ) -> None:
        """Set Line of Sight (LOS) Sun Exclusion constraint on this object.
        
        Params
        ------
        value: Optional[float]
            Set the value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_value('LOSSunExclusion', value)
    
    def set_constraint_sun_specular_exclusion(
        self: Object,
        value: Optional[float] = None,
    ) -> None:
        """Set Sun Specular Exclusion constraint on this object.
        
        Params
        ------
        value: Optional[float]
            Set the value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_value('SunSpecularExclusion', value)

    def set_constraint_los_lunar_exclusion(
        self: Object,
        value: Optional[float] = None,
    ) -> None:
        """Set Line of Sight (LOS) Lunar Exclusion constraint on this object.
        
        Params
        ------
        value: Optional[float]
            Set the value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_value('LOSLunarExclusion', value)

    def set_constraint_lighting(
        self: Object,
        value: Optional[float] = None,
    ) -> None:
        """Set Lighting constraint on this object.
        
        Params
        ------
        value: Optional[str]
            Set the value for this constraint.
            If value is None, then disable this constraint.

            Valid choices:
                Off
                DirectSun
                PenumbraDirectSun
                PenumbraUmbra
                Penumbra
                UmbraDirectSun
                Umbra
        """
        VALID = (
            None, 'Off', 'DirectSun', 'PenumbraDirectSun',
            'PenumbraUmbra','Penumbra', 'UmbraDirectSun', 'Umbra',
        )

        if value not in VALID:
            raise ValueError(f'Lighting constraint "{value}" not in {VALID}')

        self._set_constraint_value('Lighting', value)


class SatelliteConstraintMixin(
    BaseConstraintMixin,
    BasicConstraintMixin,
    SunConstraintMixin,
):
    pass


class FacilityConstraintMixin(
    BaseConstraintMixin,
    BasicConstraintMixin,
    SunConstraintMixin,
):
    def set_constraint_azimuth_rate(
        self: Location,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Azimuth Rate constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('AzimuthRate', min=min, max=max)

    def set_constraint_elevation_rate(
        self: Location,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ) -> None:
        """Set Elevation Rate constraint on this object.
        
        Params
        ------
        min: Optional[float]
            Set the minimum value for this constraint.
            If value is None, then disable this constraint.

        max: Optional[float]
            Set the maximum value for this constraint.
            If value is None, then disable this constraint.
        """
        self._set_constraint_minmax('ElevationRate', min=min, max=max)
