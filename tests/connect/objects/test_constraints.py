import pytest
import mock
from systemstoolkit.connect import Connect
from systemstoolkit.connect.objects import Satellite, Facility


def test_facility_set_constraint_lighting():
    exp = 'SetConstraint */Facility/DC Lighting DirectSun'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_lighting('DirectSun')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_lighting_invalid():
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            with pytest.raises(ValueError):
                fac_obj = Facility(c, '*/Facility/DC')
                fac_obj.set_constraint_lighting('NotAValidSunConstraint')


def test_facility_set_constraint_lighting_off():
    exp = 'SetConstraint */Facility/DC Lighting Off'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_lighting(None)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_azimuth():
    exp = 'SetConstraint */Facility/DC AzimuthAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_azimuth(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_azimuth_off():
    exp = 'SetConstraint */Facility/DC AzimuthAngle Min Off Max Off'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_azimuth(None, None)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_azimuth_invalid_values():
    exp = 'SetConstraint */Facility/DC AzimuthAngle Min Off Max Off'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            with pytest.raises(ValueError):
                fac_obj.set_constraint_azimuth(270, 480)


def test_facility_set_constraint_azimuth_invalid_minmax():
    exp = 'SetConstraint */Facility/DC AzimuthAngle Min Off Max Off'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            with pytest.raises(ValueError):
                fac_obj.set_constraint_azimuth(10, 0)


def test_facility_set_constraint_azimuth_invalid_mutual():
    exp = 'SetConstraint */Facility/DC AzimuthAngle Min Off Max Off'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            with pytest.raises(ValueError):
                fac_obj.set_constraint_azimuth(None, 10)


def test_facility_set_constraint_elevation():
    exp = 'SetConstraint */Facility/DC ElevationAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_elevation(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_azimuth_rate():
    exp = 'SetConstraint */Facility/DC AzimuthRate Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_azimuth_rate(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_elevation_rate():
    exp = 'SetConstraint */Facility/DC ElevationRate Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_elevation_rate(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_range():
    exp = 'SetConstraint */Facility/DC Range Min 10 Max 20000'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_range(min=10, max=20000)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_range_rate():
    exp = 'SetConstraint */Facility/DC RangeRate Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_range_rate(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_angular_rate():
    exp = 'SetConstraint */Facility/DC AngularRate Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_angular_rate(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_altitude():
    exp = 'SetConstraint */Facility/DC Altitude Min 1000 Max 20000'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_altitude(min=1000, max=20000)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_propagation_delay():
    exp = 'SetConstraint */Facility/DC PropagationDelay Min 0.1 Max 0.2'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_propagation_delay(min=0.1, max=0.2)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_solar_elevation_angle():
    exp = 'SetConstraint */Facility/DC SunElevationAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_solar_elevation_angle(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_lunar_elevation_angle():
    exp = 'SetConstraint */Facility/DC LunarElevationAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_lunar_elevation_angle(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_los_solar_illumination_angle():
    exp = 'SetConstraint */Facility/DC LOSSunIlluminationAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_los_solar_illumination_angle(min=10, max=20)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_los_solar_illumination_angle_invalid_mutual():
    exp = 'SetConstraint */Facility/DC LOSSunIlluminationAngle Min 10 Max 20'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            with pytest.raises(ValueError):
                fac_obj.set_constraint_los_solar_illumination_angle(10, None)


def test_facility_set_constraint_los_solar_exclusion():
    exp = 'SetConstraint */Facility/DC LOSSunExclusion 10'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_los_solar_exclusion(10)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_los_lunar_exclusion():
    exp = 'SetConstraint */Facility/DC LOSLunarExclusion 10'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_los_lunar_exclusion(10)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_constraint_sun_specular_exclusion():
    exp = 'SetConstraint */Facility/DC SunSpecularExclusion 10'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/DC')
            fac_obj.set_constraint_sun_specular_exclusion(10)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp
