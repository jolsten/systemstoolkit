from typing import Optional
import re

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

    if value is not None and value < min:
        raise ValueError(f'Value "{value}" must be >= min "{min}"')

    if value is not None and value < min:
        raise ValueError(f'Value "{value}" must be <= max "{max}"')
