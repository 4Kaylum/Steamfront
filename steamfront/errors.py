class MissingArguments(ValueError):
    '''You are missing required values from the function or method. Please consult the documentation.'''
    pass


class AppNotFound(Exception):
    '''The specified app was not found on Steam via the API.'''
    pass


class UserNotFound(Exception):
    '''The specified user was not found on Steam via the API.'''
    pass


class APIKeyRequired(Exception):
    '''Doing this requires an API key.'''
    pass
