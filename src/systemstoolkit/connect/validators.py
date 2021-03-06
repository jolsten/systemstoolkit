import re
from typing import Optional, Iterable

OBJECT_NAME = re.compile(r'^[\w-]+$')

def name(name: str) -> None:
    if len(name) > 64:
        raise ValueError(
            f'Object name "{name}" cannot be more than 64 characters in length.'
        )

    if not OBJECT_NAME.match(name):
        raise ValueError(
            f'Object name "{name}" can contain only alphanumeric characters, underscores and hyphens.'
        )
    
    if name.lower() in ['_default', 'end']:
        raise ValueError(
            f'Object name "{name}" cannot be "_Default" or "end" (regardless of case), as these are reserved words in STK.'
        )

def value(
    value: float,
    min: Optional[float] = 0,
    max: Optional[float] = 360,
) -> None:
    if value is None:
        return

    value = float(value)

    if min is not None and value < min:
        raise ValueError(f'Value "{value}" must be >= min "{min}"')

    if max is not None and value > max:
        raise ValueError(f'Value "{value}" must be <= max "{max}"')

def choice(
    value: str,
    choices: Iterable[str],
    name: str = 'Value',
) -> None:
    if value.lower() not in [x.lower() for x in choices]:
        raise ValueError(f'{name} "{value}" not a valid choice in "{choices}"')
