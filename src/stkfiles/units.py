import datetime
import numpy as np
from enum import Enum, auto
from typing import Union
from abc import ABC

DateTimeLike = Union[datetime.datetime, np.datetime64]
DateTimeOrArray = Union[datetime.datetime, np.datetime64, np.ndarray]


class TimeUnit(ABC):
    def format(self, time: DateTimeOrArray):
        pass


class EpochTimeUnit(TimeUnit):
    unit = 's'

    def __init__(
            self, 
            epoch: datetime.datetime
        ) -> None:
        super().__init__()
        self.epoch = epoch

    @property
    def epoch(self):
        return self._epoch

    @epoch.setter
    def epoch(self, epoch: DateTimeLike):
        self._epoch = np.datetime64(epoch)

    def format(
            self,
            time: DateTimeOrArray,
        ):
        time = np.asarray(time, dtype='datetime64[us]')
        return (time - self.epoch) / np.timedelta64(1, self.unit)


class EpSecTimeUnit(EpochTimeUnit):
    unit = 's'


class EpMinTimeUnit(EpochTimeUnit):
    unit = 'm'


class EpHrTimeUnit(EpochTimeUnit):
    unit = 'h'


class EpDayTimeUnit(EpochTimeUnit):
    unit = 'D'


# class EpYearTimeUnit(EpochTimeUnit):
#     unit = 'Y'


class UTCTime(TimeUnit):
    pass


class YYYYDDDTimeUnit(UTCTime):
    def format(self, time: DateTimeOrArray) -> np.ndarray:
        time = np.asarray(time, dtype='datetime64[us]')

        day = time.astype('datetime64[D]')
        year = day.astype('datetime64[Y]')
        doy = day - year
        frac_day = (time - day) / np.timedelta64(1, 'D')

        yyyy = 1000*(1970+year.astype('uint32'))
        ddd = doy.astype('uint32') + 1 + frac_day.astype('float64')
        return yyyy + ddd


class YYYYMMDDTimeUnit(UTCTime):
    def format(self, time: DateTimeOrArray) -> np.ndarray:
        time = np.asarray(time, dtype='datetime64[us]')
        day = time.astype('datetime64[D]')
        mon = time.astype('datetime64[M]')
        year = time.astype('datetime64[Y]')
        moy = mon - year
        dom = day - mon
        frac_day = ((time - day) / np.timedelta64(1, 'D')).astype('float64')
        y = 10000 * (year.astype('uint32') + 1970)
        m = 100 * (moy.astype('uint32') + 1)
        d = dom.astype('uint32') + 1
        print(y, m, d, frac_day)
        return y + m + d + frac_day


class ISOYMDTimeUnit(UTCTime):
    def format(self, time: DateTimeOrArray) -> np.ndarray:
        time = np.asarray(time, dtype='datetime64[us]')
        return time.astype(str)


class TimeUnit(Enum):
    EpSec = EpSecTimeUnit
    EpMin = EpMinTimeUnit
    EpHour = EpHrTimeUnit
    EpDays = EpDayTimeUnit
    # EpYear = EpYearTimeUnit
    YYYYDDD = YYYYDDDTimeUnit
    YYYYMMDD = YYYYMMDDTimeUnit
    ISOYMD = ISOYMDTimeUnit

    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower() == name.replace('-', '').lower():
                return member
