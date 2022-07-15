import datetime
from abc import ABC
from typing import TYPE_CHECKING, Tuple
import systemstoolkit.connect.validators as validators
from systemstoolkit.exceptions import STKCommandError

if TYPE_CHECKING:
    from systemstoolkit.connect import Connect # pragma: no cover
    from systemstoolkit.connect.objects.sensors import Sensor # pragma: no cover


class Object(ABC):
    # TYPE HINT MUST BE STRING BECAUSE OF CIRCULAR IMPORT
    def __init__(self, connect: 'Connect', path: str) -> None:
        self.connect = connect
        self.path = path
        self.children = []
    
    @property
    def name(self) -> str:
        '''The object name.
        
        Returns
        -------
        name: str
        '''
        return self.path.split('/')[-1]
    
    @property
    def parent(self) -> str:
        '''The path to the parent object.
        
        Returns
        -------
        parent name: str
        '''
        return '/'.join(self.path.split('/')[0:-2])
    
    @property
    def type(self) -> str:
        '''The object class name.
        
        Returns
        -------
        class name: str
        '''
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'{self.type}(connect={self.connect}, path="{self.path}")'

    def unload(self) -> None:
        '''Unload (delete) the object from the scenario.'''
        command = f'Unload / {self.path}'
        self.connect.send(command)
    
    def create(self) -> None:
        '''Add the Vehicle object in the current Scenario.'''
        command = f'New / */{self.type} {self.name}'
        self.connect.send(command)

    def rename(self, name: str) -> None:
        '''Rename the object.

        Params
        ------
        name: str
            The new object name.

        Returns
        -------
        None
        '''
        validators.name(name)
        new_path = f'{self.parent}/{self.type}/{name}'
        try:
            self.connect.send(f'Rename {self.path} {name}')
        except STKCommandError as msg:
            raise
        else:
            self.path = new_path


class Scenario(Object):
    def create(self) -> None:
        '''Create a new Scenario.'''
        # Unload current scenario
        self.connect.send('Unload / *')

        # Create new scenario
        command = f'New / Scenario {self.name}'
        self.connect.send(command)
    
    def get_time_period(self) -> Tuple[datetime.datetime, datetime.datetime]:
        '''Get the Scenario Time Period.'''
        self.connect.send(f'GetTimePeriod {self.path}')
        msg = self.connect.get_single_message()
        print(msg)
        return msg


class Vehicle(Object):
    _PROPAGATOR = ()
    _COORD_SYSTEM = ()

    def new_sensor(self, name: str) -> 'Sensor':
        """Add a new sensor object to this parent."""
        from systemstoolkit.connect.objects.sensors import Sensor

        object_path = f'{self.path}/Sensor/{name}'
        obj = Sensor(self.connect, object_path)
        obj.create()
        return obj


class Attachment(Object):
    def create(self) -> None:
        '''Add the VehicleAttachment object to its parent object.'''
        command = f'New / {self.parent}/{self.type} {self.name}'
        self.connect.send(command)


class Location(Object):
    pass
