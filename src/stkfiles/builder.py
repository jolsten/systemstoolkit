import datetime
import numpy as np

from .files import AttitudeFile
from .keywords import (
    AttitudeFileFormat,
    MessageLevel,
    CoordinateAxes,
    CoordinateAxesEpoch,
    ScenarioEpoch,
    CentralBody,
    Interpolation,
    InterpolationMethod,
    InterpolationOrder,
    AttitudeDeviations,
    BlockingFactor,
)

def attitude_file(
    time: np.ndarray,
    data: np.ndarray,
    format: str = None,
    epoch: datetime.datetime = None,
    axes: str = None,
    axes_epoch: datetime.datetime = None,
    message: str = 'Warnings',
    body: str = None,
    int_method: str = None,
    int_order: int = None,
    deviations: str = None,
    blocking: int = None,
) -> str:
    format = AttitudeFileFormat(format)
    if message:
        message = MessageLevel(message)

    if axes:
        coord = CoordinateAxes(axes)
        if axes_epoch:
            axes_epoch = CoordinateAxesEpoch(axes_epoch)
        axes = CoordinateAxes(axes=coord, epoch=axes_epoch)

    if epoch:
        epoch = ScenarioEpoch(epoch)

    if body:
        body = CentralBody(body)

    if int_method:
        int_method = InterpolationMethod(int_method)

    if int_order:
        int_order = InterpolationOrder(int_order)

    interpolation = Interpolation(method=int_method, order=int_order)

    if deviations:
        deviations = AttitudeDeviations(deviations)
    
    if blocking:
        blocking = BlockingFactor(blocking)

    a_file = AttitudeFile(
        time,
        data,
        format=format,
        axes=axes,
        epoch=epoch,
        message=message,
        body=body,
        interp=interpolation,
        deviations=deviations,
        blocking=blocking,
    )

    return a_file.to_string()
