import datetime
from abc import ABC
from typing import Iterable, Optional
import systemstoolkit.connect.validators as validators
from systemstoolkit.exceptions import STKCommandError
from systemstoolkit.utils import stk_datetime


class Object(ABC):
    def __init__(self, connect, object_path: str) -> None:
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


class Vehicle(Object):
    def create(self) -> None:
        command = f'New / */{self.__class__.__name__} {self.name}'
        self.connect.send(command)

    def set_state_cartesian(
        self,
        epoch: datetime.datetime,
        state: Iterable,
        stepsize: float = 60.0,
        prop: str = 'TwoBody',
        coord: str = 'Fixed',
    ) -> None:
        self.connect.send(' '.join([
            f'SetState {self.path} Cartesian {prop} UseScenarioInterval', 
            f'{stepsize} {coord} "{stk_datetime(epoch)}"',
            ' '.join([str(x) for x in state]),
        ]))


class VehicleAttachment(Object):
    def create(self) -> None:
        command = f'New / {self.parent}/{self.__class__.__name__} {self.name}'
        self.connect.send(command)
