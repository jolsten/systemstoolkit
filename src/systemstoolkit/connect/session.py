import socket
import collections
from typing import List
from systemstoolkit.exceptions import STKCommandError, STKConnectError
from systemstoolkit.connect.objects import (
    _Application, Scenario, Satellite, Location, Facility, Target, Place
)
from systemstoolkit.connect import validators


SingleMessage = collections.namedtuple(
    'SingleMessage',
    ['CommandName', 'DataLength', 'Data'],
)

MultiMessage = collections.namedtuple(
    'MultiMessage',
    ['CommandName', 'DataLength', 'Messages'],
)


class Connect:
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 5001,
        log: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.log = log
        self._socket = None
        self._history = None
        self.units = {}
    
    def __str__(self) -> str:
        return 'Connect()'
    
    def __repr__(self) -> str:
        return f'Connect(host="{self.host}", port={self.port})'

    def __enter__(self) -> None:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb, sep="\n") -> None:
        self.close()

    def close(self) -> None:
        self._socket.close()
        self._history = None
    
    def connect(self) -> None:
        try:
            self._socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            self._socket.connect((self.host, self.port))
            self._history = []
        except ConnectionRefusedError as msg:
            raise
    
    def send(self, command: str) -> None:
        # Strip any trailing newlines
        command = command.rstrip()

        # Send the string with one (required) newline
        self._socket.sendall(str.encode(command + '\n'))

        # Check for ACK/NACK
        response = self._get_ack()
        
        if self.log:
            self._history.append((command, response))
        
        if response == 'NACK':
            raise STKCommandError(command, response)
        
    def _get_ack(self) -> str:
        data = self._socket.recv(3)
        if data.decode() == 'ACK':
            return 'ACK'
        elif data.decode() == 'NAC':
            data = data + self._socket.recv(1)
            return 'NACK'
        raise STKConnectError(
            f'Did not receive ACK or NACK, got message: {data.decode()}'
        )
    
    def get_single_message(self) -> SingleMessage:
        data = self._socket.recv(40)
        command_name, data_length = data.decode().split('\x00')[0].split()
        
        # Determine length of message, get that many bytes
        data_length = int(data_length)
        data = self._socket.recv(data_length)
        message = data.decode()

        return SingleMessage(command_name, data_length, message)

    def get_multi_message(self) -> MultiMessage:
        data = self._socket.recv(40)
        command_name, data_length = data.decode().split('\x00')[0].split()
        
        # Determine length of message, get that many bytes
        data_length = int(data_length)
        data = self._socket.recv(data_length)

        # Determine the qty of SingleMessages, get them
        num_messages = int(data)
        messages = [self.get_single_message() for _ in range(num_messages)]
        
        # Get closing SingleMessage
        self.get_single_message()
        return MultiMessage(command_name, num_messages, messages)

    def get_report(self) -> list:
        multi_msg = self.get_multi_message()
        return [msg.Data for msg in multi_msg]

    def unload_all(self) -> None:
        """Unload (delete) all objects including the current Scenario."""
        self.send('Unload / *')

    def get_class_paths(self, cls: str) -> str:
        self.send(f'ShowNames * Class {cls}')
        msg = self.get_single_message()
        paths = msg.Data.strip().split()
        return paths

    def get_scenario(self) -> Scenario:
        scenario_path = self.show_class_paths('Scenario')[0]
        obj = Scenario(self, scenario_path)
        return obj

    def get_satellites(self) -> List[Satellite]:
        paths = self.show_class_paths('Satellite')
        return [Satellite(self, path) for path in paths]

    def get_facilities(self) -> List[Facility]:
        paths = self.show_class_paths('Facility')
        return [Facility(self, path) for path in paths]
    
    def get_places(self) -> List[Place]:
        paths = self.show_class_paths('Place')
        return [Place(self, path) for path in paths]
    
    def get_targets(self) -> List[Target]:
        paths = self.show_class_paths('Target')
        return [Target(self, path) for path in paths]

    def get_locations(self) -> List[Location]:
        a = self.get_facilities()
        b = self.get_targets()
        c = self.get_places()
        return a + b + c

    def get_connect_units(self) -> str:
        self.send('Units_Get * Connect Abbreviation')
        msg = self.get_single_message()
        items = [x.split() for x in msg.Data.strip().replace(';', '').splitlines()]
        return {dim.lower(): unit for dim, unit in items}

    def new_scenario(self, name: str) -> Scenario:
        """Create a new Scenario (by first unloading all)."""
        self.unload_all()
        obj = Scenario.from_name(self, _Application(), name)
        obj.create()
        return obj

    def new_satellite(self, name: str) -> Satellite:
        """Create a new Satellite with given name."""
        validators.name(name)
        obj = Satellite(self, f'*/Satellite/{name}')
        obj.create()
        return obj
    
    def new_facility(self, name: str) -> Facility:
        """Create a new Facility with given name."""
        validators.name(name)
        obj = Facility(self, f'*/Facility/{name}')
        obj.create()
        return obj
    
    def new_place(self, name: str) -> Place:
        """Create a new Place with given name."""
        validators.name(name)
        obj = Place(self, f'*/Place/{name}')
        obj.create()
        return obj
    
    def new_target(self, name: str) -> Target:
        """Create a new Facility with given name."""
        validators.name(name)
        obj = Target(self, f'*/Target/{name}')
        obj.create()
        return obj

    def update_connect_units(self) -> None:
        """Get the current Connect units and store them as the .units attribute."""
        self.units = self.get_connect_units()
