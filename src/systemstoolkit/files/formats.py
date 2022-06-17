from enum import auto
from systemstoolkit.files.keywords import KeywordEnum


class DataFileFormat(KeywordEnum):
    def validate_data(self, time, data):
        return time, data


class AttitudeFileFormat(DataFileFormat):
    # Quaternion-based formats
    Quaternions = auto()
    QuatScalarFirst = auto()
    QuatAngVels = auto()
    AngVels = auto()

    # Euler-based Formats
    EulerAngles = auto()
    EulerAngleRates = auto()
    EulerAnglesAndRates = auto()

    # YPR-based formats
    YPRAngles = auto()
    YPRAngleRates = auto()
    YPRAnglesAndRates = auto()

    # DCM-based formats
    DCM = auto()
    DCMAngVels = auto()

    # Vector-based formats
    ECFVector = auto()
    ECIVector = auto()

    def __str__(self) -> str:
        return f'AttitudeTime{self.name}'
