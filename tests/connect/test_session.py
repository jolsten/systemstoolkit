import pytest
import mock
from systemstoolkit.connect.session import Connect
from systemstoolkit.connect.objects import Scenario, Satellite, Sensor


def test_connect_socket():
    with mock.patch('socket.socket'):
        s = Connect()
        s.connect()
        s._socket.connect.assert_called_with(('localhost', 5001))
        assert s._socket.connect.call_count == 1



class MockConnect:
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 50001,
        return_value = 'ACK',
    ) -> None:
        self.host = host
        self.port = port
        self.return_value = return_value
    
    def __enter__(self):
        with mock.patch('socket.socket') as mock_sock:
            self.connect = Connect(self.host, self.port)
            self.connect()

    def __exit__(self):
        self.connect.close()

    def get_sent(self) -> list:
        return


@pytest.mark.parametrize('command', [
    'New / Scenario See_DC',
    'New / */Satellite ERS1',
])
def test_send_command(command):
    with mock.patch('socket.socket') as mock_sock:
        s = Connect()
        s.connect()
        assert s._socket.connect.call_count == 1

        # Set the recv return value to be ACK so get_ack() works in send()
        mock_sock.return_value.recv.return_value = b'ACK'
        
        s.send(command)
        sent_command = s._socket.sendall.call_args[0][0].decode().strip()
        assert sent_command == command.strip()


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
