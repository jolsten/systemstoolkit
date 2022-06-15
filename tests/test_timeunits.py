import pytest
from pytest import approx
import numpy as np

from stkfiles.units import (
    EpSecTimeUnit,
    EpMinTimeUnit,
    EpHrTimeUnit,
    EpDayTimeUnit,
    YYYYDDDTimeUnit,
    YYYYMMDDTimeUnit,
    ISOYMDTimeUnit,
)

UTC_TIMES = [
    ['2021-01-01 00:00:00', 2021001.000, 20210101.000],
    ['2021-01-01 06:00:00', 2021001.500, 20210101.250],
    ['2021-01-01 12:00:00', 2021001.500, 20210101.500],
    ['2021-01-01 18:00:00', 2021001.500, 20210101.750],
    ['2021-01-31 00:00:00', 2021031.000, 20210131.000],
    ['2021-01-31 06:00:00', 2021031.000, 20210131.250],
    ['2021-01-31 12:00:00', 2021031.000, 20210131.500],
    ['2021-01-31 18:00:00', 2021031.000, 20210131.750],
]

EPOCH = np.datetime64(UTC_TIMES[0][0])
EPOCH_TIMES = []
for time, _, _ in UTC_TIMES:
    td = np.datetime64(time) - EPOCH
    row = [(td / np.timedelta64(1, unit)).astype('float64') for unit in ['s', 'm', 'h', 'D']]
    EPOCH_TIMES.append([time] + row)


@pytest.mark.parametrize('time, yyyyddd, yyyymmdd', UTC_TIMES)
def test_utc_timeunit(time, yyyyddd, yyyymmdd):
    time = np.datetime64(time)

    yd = YYYYDDDTimeUnit()
    ymd = YYYYMMDDTimeUnit()
    assert yd.format(time) == approx(yyyyddd)
    assert ymd.format(time) == approx(yyyymmdd)

    time = np.array([time, time, time, time, time])
    assert yd.format(time) == approx(yyyyddd)
    assert ymd.format(time) == approx(yyyymmdd)


@pytest.mark.parametrize('time, s, m, h, D', EPOCH_TIMES)
def test_epoch_timeunit(time, s, m, h, D):
    time = np.datetime64(time)

    print(EPOCH_TIMES)

    EpochTimeUnits = [EpSecTimeUnit, EpMinTimeUnit, EpHrTimeUnit, EpDayTimeUnit]
    for cls, td in zip(EpochTimeUnits, [s, m, h, D]):
        a = cls(epoch=EPOCH)
        assert a.format(time) == approx(td)
