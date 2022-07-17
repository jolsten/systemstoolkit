from typing import Optional
from systemstoolkit.typing import TimeInterval
from systemstoolkit.connect.objects.base import Object, Vehicle, Location
import systemstoolkit.connect.validators as validators


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
        validators.value(min, 0, 360)
        validators.value(max, min, 360)

        # Must be specified together or not at all
        a = bool(min is None)
        b = bool(max is None)

        if (a and not b) or (not a and b):
            raise ValueError(f'Azimuth constraint must have both min and max, or neither')

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
        validators.value(min, 0, 90)
        validators.value(max, min, 90)
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
        validators.value(min, 0, None)
        validators.value(max, min, None)
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
        validators.value(min, 0, None)
        validators.value(max, min, None)
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
        validators.value(min, 0, None)
        validators.value(max, min, None)
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
    def set_constraint_solar_elevation_angle(
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
        validators.value(min, 0, 90)
        validators.value(max, min, 90)
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
        validators.value(min, 0, 90)
        validators.value(max, min, 90)
        self._set_constraint_minmax('LunarElevationAngle', min=min, max=max)

    def set_constraint_los_solar_illumination_angle(
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
        validators.value(min, 0, 90)
        validators.value(max, min, 90)

        # Must be specified together or not at all
        a = bool(min is None)
        b = bool(max is None)
        if (a and not b) or (not a and b):
            raise ValueError(f'Azimuth constraint must have both min and max, or neither')

        self._set_constraint_minmax('LOSSunIlluminationAngle', min=min, max=max)

    def set_constraint_los_solar_exclusion(
        self: Object,
        value: Optional[float] = None,
    ) -> None:
        """Set Line of Sight (LOS) Solar Exclusion constraint on this object.
        
        Params
        ------
        value: Optional[float]
            Set the value for this constraint.
            If value is None, then disable this constraint.
        """
        validators.value(value, 0, 180)
        self._set_constraint_value('LOSSunExclusion', value)

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
        validators.value(value, 0, 180)
        self._set_constraint_value('LOSLunarExclusion', value)

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
        validators.value(value, 0, 180)
        self._set_constraint_value('SunSpecularExclusion', value)

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
        validators.value(min, 0, None)
        validators.value(max, min, None)
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
        validators.value(min, 0, None)
        validators.value(max, min, None)
        self._set_constraint_minmax('ElevationRate', min=min, max=max)
