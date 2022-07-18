class STKError(Exception):
    pass

class STKConnectError(STKError):
    pass

class STKCommandError(STKError):
    def __init__(self, command: str, response: str) -> None:
        message = f'Sent "{command}"; Got "{response}"'
        super().__init__(message)
