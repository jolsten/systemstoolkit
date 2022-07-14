import pytest
import mock
from systemstoolkit.connect import Connect
from systemstoolkit.connect.objects import Facility


def test_create_facility():
    exp = 'New / */Facility FacilityName'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/FacilityName')
            fac_obj.create()

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_position_cartesian():
    exp = 'SetPosition */Facility/AGIHQ Cartesian 1216360.0 -4736250.0 4081270.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/AGIHQ')
            fac_obj.set_position_cartesian('1216360.0', '-4736250.0', '4081270.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_position_geodetic():
    exp = 'SetPosition */Facility/Wallops Geodetic 37.9 -75.5 0.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/Wallops')
            fac_obj.set_position_geodetic('37.9', '-75.5', '0.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_position_geodetic_msl():
    exp = 'SetPosition */Facility/Wallops Geodetic 37.9 -75.5 0.0 MSL'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/Wallops')
            fac_obj.set_position_geodetic('37.9', '-75.5', '0.0', msl=True)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_position_geocentric():
    exp = 'SetPosition */Facility/Wallops Geocentric 37.9 -75.5 0.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/Wallops')
            fac_obj.set_position_geocentric('37.9', '-75.5', '0.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_position_geocentric_msl():
    exp = 'SetPosition */Facility/Wallops Geocentric 37.9 -75.5 0.0 MSL'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/Wallops')
            fac_obj.set_position_geocentric('37.9', '-75.5', '0.0', msl=True)

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_facility_set_height_above_ground():
    exp = 'SetHeightAboveGround */Facility/aero1 17.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            fac_obj = Facility(c, '*/Facility/aero1')
            fac_obj.set_height_above_ground('17.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp
