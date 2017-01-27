from requests import get as _get
from .errors import AppNotFound as _AppNotFound


class User(object):
    '''
    The user object, representing a Steam user

    :param str id64: The user's ID64.
    :param apiKey: Your API key.
    :type apiKey: Optional[str]
    '''

    def __init__(self, id64: str, apiKey: str=None):
        pass
