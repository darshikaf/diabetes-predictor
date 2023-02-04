class BaseCustomException(Exception):
    """
    Base Exception Class
    """
    def __init__(self, msg: str, **args: object) -> None:
        msg = f"{self.__class__.__name__}: {msg}"
        super().__init__(msg, *args)

class InvalidModelVersion(BaseCustomException):
    """
    Exception raised when an invalid model version is provided.
    """

class InvalidInput(BaseCustomException):
    """
    Exception raised if invalid input is provided.
    """

