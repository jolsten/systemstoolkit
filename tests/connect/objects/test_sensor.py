import pytest
import mock
from systemstoolkit.connect import Connect
from systemstoolkit.connect.objects import Satellite, Sensor


def test_sensor_unload():
    exp = 'Unload / */Satellite/ERS1/Sensor/FOV'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Sensor(c, '*/Satellite/ERS1/Sensor/FOV')
            sat_obj.unload()

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_create():
    exp = 'New / */Satellite/ERS1/Sensor FOV'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Sensor(c, '*/Satellite/ERS1/Sensor/FOV')
            sat_obj.create()

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_conical():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon Conical 0.0 85.0 0.0 360.0 AngularRes 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_conical('0.0', '85.0', '0.0', '360.0', resolution='10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_half_power():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon HalfPower 1000000000 1 AngularRes 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_half_power(1000000000, 1, resolution='10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_rectangular():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon Rectangular 4.0 10.0 AngularRes 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_rectangular('4.0', '10.0', resolution='10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_sar():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon SAR 10 50 30 40 AngularRes 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_sar(10, 50, 30, 40, resolution='10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_simple():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon SimpleCone 10 AngularRes 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_simple(10, resolution='10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_custom():
    exp = r'Define */Satellite/Shuttle/Sensor/Horizon Custom "C:\path\to\file.sen"'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define_custom(r'C:\path\to\file.sen')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_by_type():
    exp = 'Define */Satellite/Shuttle/Sensor/Horizon Rectangular 4.0 10.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            sensor_obj.define('rectangular', '4.0', '10.0')

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_sensor_define_by_type_invalid():
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sensor_obj = Sensor(c, '*/Satellite/Shuttle/Sensor/Horizon')
            with pytest.raises(ValueError):
                sensor_obj.define('not_a_sensor_type', '4.0', '10.0')
