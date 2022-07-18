from abc import ABC, abstractmethod, abstractproperty
from typing import Optional
import systemstoolkit.connect.validators as validators


class ConnectCommand(ABC):
    @abstractproperty
    def command(self) -> str:
        pass


class NewObject(ConnectCommand):
    @abstractproperty
    def cls(self) -> str:
        pass

    def __init__(
        self,
        parent_path: str,
        name: str,
        ignore: bool = False,
        default: bool = True,
        central_body: Optional[str] = None,
    ) -> None:
        validators.name(name)
        self.parent_path = parent_path
        self.name = name
        self.central_body = central_body
        self.ignore = ignore
        self.default = default

    @property
    def command(self) -> str:
        return f'New / {self.parent_path}/{self.cls} {self.name}'

class NewScenario(NewObject):
    @property
    def command(self) -> str:
        return f'New / Scenario {self.name}'

class NewSatellite(NewObject):
    cls = 'Satellite'

class NewFacility(NewObject):
    cls = 'Facility'


