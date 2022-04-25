class UserNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPasswordException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
