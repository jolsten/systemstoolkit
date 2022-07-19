from abc import ABC, abstractproperty
from typing import Protocol, Optional
import systemstoolkit.connect.validators as validators


class ConnectCommand(Protocol):
    command: str = ...


class New:
    def __init__(
        self,
        cls: str,
        name: str,
        parent_path: Optional[str] = None,
        ignore: bool = False,
        default: bool = True,
        central_body: Optional[str] = None,
    ) -> None:
        validators.name(name)
        self.parent_path = parent_path
        self.cls = cls
        self.name = name
        self.central_body = central_body
        self.ignore = ignore
        self.default = default

        if self.parent_path is None and self.cls != 'Scenario':
            raise ValueError(f'parent_path can only be None if cls=Scenario')

    @property
    def command(self) -> str:
        if self.parent_path is None:
            return f'New / {self.cls} {self.name}'
        return f'New / {self.parent_path}/{self.cls} {self.name}'


class Unload:
    """Unload <ApplicationPath> <ObjectPath> [RemAssignedObjs]"""
    def __init__(
        self,
        path: str,
        assigned_objects: bool = False,
    ) -> None:
        self.path = path
        self.assigned_objects = assigned_objects

    @property
    def command(self) -> str:
        return f'Unload / {self.path}' + ' RemAssignedObjects' if self.assigned_objects else ''





