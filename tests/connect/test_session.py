import pytest
import mock
from systemstoolkit.connect.session import Connect
from systemstoolkit.connect.objects import Scenario, Satellite, Sensor
from systemstoolkit.exceptions import STKCommandError


def test_connect_socket():
    with mock.patch('socket.socket'):
        s = Connect()
        s.connect()
        s._socket.connect.assert_called_with(('localhost', 5001))
        assert s._socket.connect.call_count == 1


def test_connect_socket_refused():
    c = Connect('localhost', 1)

    with pytest.raises(ConnectionRefusedError):
        c.connect()


@pytest.mark.parametrize('command', [
    'New / Scenario See_DC',
    'New / */Satellite ERS1',
])
def test_send_command_ack(command):
    with mock.patch('socket.socket') as mock_sock:
        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect(log=True) as c:
            assert c._socket.connect.call_count == 1

            c.send(command)
            sent_command = c._socket.sendall.call_args[0][0].decode().strip()
            assert sent_command == command.strip()
                
            # Check that command shows up in the last spot in command log
            assert c._history[-1] == (command.strip(), 'ACK')


@pytest.mark.parametrize('command', [
    'New / Scenario See_DC',
    'New / */Satellite ERS1',
])
def test_send_command_nack(command):
    with mock.patch('socket.socket') as mock_sock:
        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'NACK'

        with Connect(log=True) as c:
            with pytest.raises(STKCommandError):
                c.send(command)
                sent_command = c._socket.sendall.call_args[0][0].decode().strip()
                assert sent_command == command.strip()
                
                # Check that command shows up in the last spot in command log
                assert c._history[-1] == (command.strip(), 'NACK')


def test_new_scenario():
    with mock.patch('socket.socket') as mock_sock:
        s = Connect()
        s.connect()
        assert s._socket.connect.call_count == 1

        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'ACK'
        
        name = 'ScenarioNameHere'
        scenario_obj = s.new_scenario(name)
        cmd = s._socket.sendall.call_args[0][0].decode().strip()
        
        assert isinstance(scenario_obj, Scenario)
        assert cmd == f'New / Scenario {name}'


def test_new_satellite():
    with mock.patch('socket.socket') as mock_sock:
        s = Connect()
        s.connect()
        assert s._socket.connect.call_count == 1

        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'ACK'
        
        name = 'SatNameHere'
        sat_obj = s.new_satellite(name)
        cmd = s._socket.sendall.call_args[0][0].decode().strip()
        
        assert isinstance(sat_obj, Satellite)
        assert cmd == f'New / */Satellite {name}'


def test_new_sensor():
    with mock.patch('socket.socket') as mock_sock:
        s = Connect()
        s.connect()
        assert s._socket.connect.call_count == 1

        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'ACK'

        sat_name = 'SatelliteName'
        sat_obj = s.new_satellite(sat_name)
        cmd = s._socket.sendall.call_args[0][0].decode().strip()

        print('Command 1:', cmd)
        print(s._socket.sendall.call_args)
        assert isinstance(sat_obj, Satellite)
        assert cmd == f'New / */Satellite {sat_name}'

        sen_name = 'SensorName'
        sen_obj = sat_obj.new_sensor(sen_name)
        cmd = s._socket.sendall.call_args[0][0].decode().strip()

        print('Command 2:', cmd)
        print(s._socket.sendall.call_args)
        print('path:', sat_obj.path)
        print('sensor_name:', sen_name)
        assert isinstance(sen_obj, Sensor)
        assert cmd == f'New / {sat_obj.path}/Sensor {sen_name}'
