<<<<<<< HEAD
import datetime
import numpy as np
import pathlib
from typing import Iterable
from dateutil.parser import parse as parse_datetime, ParserError
from systemstoolkit.typing import DateTimeLike


STK_DATE_FMT = '%d %b %Y %H:%M:%S.%f'

def stk_datetime(timestamp: DateTimeLike) -> str:

    if isinstance(timestamp, datetime.datetime):
        return timestamp.strftime(STK_DATE_FMT)[0:24]

    elif isinstance(timestamp, np.datetime64):
        return timestamp.astype(datetime.datetime).strftime(STK_DATE_FMT)[0:24]

    raise TypeError(
        f'Expected {DateTimeLike}, got "{timestamp}" of type {type(timestamp)}'
    )


def parse_file_data(file_text) -> tuple:
    time, data = [], []
    epoch = None
    for line in file_text.splitlines():
        try:
            parts = line.strip().split()
            
            if parts[0] == 'ScenarioEpoch':
                epoch = parse_datetime(' '.join(parts[1:]))
            
            t = epoch + datetime.timedelta(seconds=float(parts[0]))
            time.append(t)
            data.append([float(x) for x in parts[1:]])
        except (ValueError, ParserError):
            pass
    time = np.array(time, dtype='datetime64[ms]')
    data = np.array(data, dtype='float32')
    return time, data


def read_file_data(file) -> tuple:
    return parse_file_data(pathlib.Path(file).read_text())


def make_command(parts: Iterable) -> str:
    fmt_parts = []
    for p in parts:
        if isinstance(p, str):
            fmt_parts.append(p)
        elif isinstance(p, (datetime.datetime, np.datetime64)):
            fmt_parts.append(
                f'"{stk_datetime(p)}"'
            )
        elif isinstance(p, Iterable):
            fmt_parts.append(make_command(p))
        else:
            fmt_parts.append(str(p))
    return ' '.join(fmt_parts)
=======
import datetime
import numpy as np
import pathlib
from typing import Iterable
from dateutil.parser import parse as parse_datetime, ParserError
from systemstoolkit.typing import DateTimeLike


STK_DATE_FMT = '%d %b %Y %H:%M:%S.%f'

def stk_datetime(timestamp: DateTimeLike) -> str:

    if isinstance(timestamp, datetime.datetime):
        return timestamp.strftime(STK_DATE_FMT)[0:24]

    elif isinstance(timestamp, np.datetime64):
        return timestamp.astype(datetime.datetime).strftime(STK_DATE_FMT)[0:24]

    raise TypeError(
        f'Expected {DateTimeLike}, got "{timestamp}" of type {type(timestamp)}'
    )


def parse_file_data(file_text) -> tuple:
    time, data = [], []
    epoch = None
    for line in file_text.splitlines():
        try:
            parts = line.strip().split()
            
            if parts[0] == 'ScenarioEpoch':
                epoch = parse_datetime(' '.join(parts[1:]))
            
            t = epoch + datetime.timedelta(seconds=float(parts[0]))
            time.append(t)
            data.append([float(x) for x in parts[1:]])
        except (ValueError, ParserError):
            pass
    time = np.array(time, dtype='datetime64[ms]')
    data = np.array(data, dtype='float32')
    return time, data


def read_file_data(file) -> tuple:
    return parse_file_data(pathlib.Path(file).read_text())


def make_command(parts: Iterable) -> str:
    fmt_parts = []
    for p in parts:
        if isinstance(p, str):
            fmt_parts.append(p)
        elif isinstance(p, (datetime.datetime, np.datetime64)):
            fmt_parts.append(
                f'"{stk_datetime(p)}"'
            )
        elif isinstance(p, Iterable):
            fmt_parts.append(make_command(p))
        else:
            fmt_parts.append(str(p))
    return ' '.join(fmt_parts)
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
