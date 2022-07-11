import datetime
from abc import ABC
from typing import TYPE_CHECKING, Tuple
import systemstoolkit.connect.validators as validators
from systemstoolkit.exceptions import STKCommandError

if TYPE_CHECKING:
    from systemstoolkit.connect import Connect


class Object(ABC):
    # TYPE HINT MUST BE STRING BECAUSE OF CIRCULAR IMPORT
    def __init__(self, connect: 'Connect', object_path: str) -> None:
        self.connect = connect
        self.path = object_path
        self.children = []
    
    @property
    def name(self) -> str:
        return self.path.split('/')[-1]
    
    @property
    def parent(self) -> str:
        return '/'.join(self.path.split('/')[0:-2])
    
    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        n = self.__class__.__name__
        return f'{n}(connect={self.connect}, object_path={self.path})'

    def unload(self) -> None:
        command = f'Unload / {self.path}'
        self.connect.send(command)
    
    def rename(self, name: str) -> None:
        validators.name(name)
        new_path = f'{self.parent}/{self.__class__.__name__}/{name}'
        try:
            self.connect.send(f'Rename {self.path} {name}')
        except STKCommandError as msg:
            raise
        else:
            self.path = new_path


class Scenario(Object):
    def create(self) -> None:
        # Unload current scenario
        self.connect.send('Unload / *')

        # Create new scenario
        command = f'New / Scenario {self.name}'
        self.connect.send(command)
    
    def get_time_period(self) -> Tuple[datetime.datetime, datetime.datetime]:
        self.connect.send(f'GetTimePeriod {self.path}')
        msg = self.connect.get_single_message()
        print(msg)
        return msg


class Vehicle(Object):
    _PROPAGATOR = ()
    _COORD_SYSTEM = ()

    def create(self) -> None:
        command = f'New / */{self.__class__.__name__} {self.name}'
        self.connect.send(command)


class VehicleAttachment(Object):
    def create(self) -> None:
        command = f'New / {self.parent}/{self.__class__.__name__} {self.name}'
        self.connect.send(command)


