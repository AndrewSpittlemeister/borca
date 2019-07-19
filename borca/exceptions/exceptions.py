class BorcaException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return self.__class__.__name__ + ': ' + self.message


class InvalidTomlPath(BorcaException):
    '''An exception denoting an unsuccessful attempt find a valid pyproject.toml file.'''

    pass


class InvalidToolConfiguration(BorcaException):
    '''An exception denoting an incorrect data configuration found in the TOML file under the borca.tool heading.'''

    pass


class InvalidTaskConfiguration(BorcaException):
    '''An exception denoting an incorrect data configuration found in the TOML file under a borca.tool.task heading.'''

    pass


def exception_guard(exception):
    def decorator(func):
        def runner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except BorcaException as e:
                raise exception('Outer Exception') from e

        return runner

    return decorator
