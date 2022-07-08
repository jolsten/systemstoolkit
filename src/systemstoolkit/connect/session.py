import sys
import socket
import collections

from systemstoolkit.exceptions import STKCommandError
from systemstoolkit.connect.objects import Satellite
from systemstoolkit.connect.objects.base import Object
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
    ) -> None:
        self.host = host
        self.port = port
        self._socket = None
        
    def close(self) -> None:
        self._socket.close()
    
    def connect(self) -> None:
        try:
            self._socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            self._socket.connect((self.host, self.port))
        except ConnectionRefusedError as msg:
            raise
    
    def send(self, command: str) -> None:
        command = command.rstrip()
        self._socket.sendall(str.encode(command + '\n'))
        response = self._get_ack()
        if response == 'NACK':
            raise STKCommandError(f'NACK: {command}')
        
    def _get_ack(self) -> str:
        data = self._socket.recv(3)
        if data.decode() == 'ACK':
            return 'ACK'
        elif data.decode() == 'NAC':
            data = data + self._socket.recv(1)
            return 'NACK'
        raise STKCommandError(
            f'Did not receive ACK or NACK, got message: {data.decode()}'
        )
    
    def get_single_message(self) -> SingleMessage:
        data = self._socket.recv(40)
        command_name, data_length = data.decode().split()
        data_length = int(data_length)
        data = self._socket.recv(data_length)
        message = data.decode()
        return SingleMessage(command_name, data_length, message)

    def get_multi_message(self) -> MultiMessage:
        data = self._socket.recv(40)
        command_name, data_length = data.decode().split()
        data_length = int(data_length)
        data = self._socket.recv(data_length)
        num_messages = int(data)
        messages = [self.get_single_message() for _ in range(num_messages)]
        self.get_single_message()
        return MultiMessage(command_name, num_messages, messages)

    def get_report(self) -> list:
        multi_msg = self.get_multi_message()
        return [msg.Data for msg in multi_msg]

    def unload_all(self) -> None:
        self.send('Unload / *')

    def new_scenario(self, name: str) -> str:
        self.unload_all()
        self.send(f'New / Scenario {name}')

    def new_satellite(self, name: str) -> Satellite:
        validators.name(name)
        obj = Satellite(self, f'*/Satellite/{name}')
        obj.create()
        return obj


class _FakeConnect(Connect):
    def close(self) -> None:
        pass

    def connect(self) -> None:
        self._messages = []
    
    def send(self, command: str) -> None:
        self._messages.append(command)
