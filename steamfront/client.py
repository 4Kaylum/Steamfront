from requests import get as _get
from .app import App as _App
from .user import User as _User
from .errors import AppNotFound as _AppNotFound
from .errors import MissingArguments as _MissingArguments


class Client(object):
    '''
    Provides a client for you to get apps, users, and other miscellania with.

    :param apiKey: The key used for API functions. This is not required for all methods, but a good few of them. Defaults to ``None`` if no key is passed on client creation.
    :type apiKey: Optional[str]
    '''

    def __init__(self, apiKey: str=None):

        self._apiKey = apiKey
        self._appList = None

        # # Populate game list
        # self._getGamesFromSteam()

    def _getGamesFromSteam(self) -> list:
        '''
        Gives a list of all games on Steam.
        '''

        # Get the list from the API
        steamAppList = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
        dictGames = _get(steamAppList)

        # Get the list from the dictionary
        jsonGames = dictGames.json()
        gameList = jsonGames['applist']['apps']['app']

        # Store everything nicely
        self._appList = gameList
        return gameList

    def _getIDOfApp(self, name: str, caseSensitive: bool=True) -> str:
        '''
        Gives the ID of an app whose name you have
        '''

        # Refresh/make the app list if necessary
        if self._appList == None:
            self._getGamesFromSteam()

        sensitive = lambda x, y: x == y['name']
        unsensitive = lambda x, y: x.lower() == y['name'].lower()
        searchStyle = {True: sensitive, False: unsensitive}[caseSensitive]

        # Iterate through the list and get the game's name.
        for i in self._appList:
            if searchStyle(name, i):
                return i['appid']

        # No game found, raise error
        raise _AppNotFound(
            'The name `{}` was not found on the API. Try using an app ID.'.format(name))

    def getApp(self, *, name: str=None, appid: str=None, caseSensitive: bool=True) -> _App:
        '''
        Returns a :class:`steamfront.app.App` of the name or app ID that was input to the function.

        :param str appid: The ID of the app you're getting the object of. 
        :param str name: The name of the app you're getting the object of. May not be 100% accurate.
        :param bool caseSensitive: Whether or not the name being searched for is case sensitive or not. Has no effect on appid.
        :return: The object of relevant data on the app.
        :rtype: :class:`steamfront.app.App`
        :raises steamfront.errors.MissingArguments: Raised if there is neither a name or an app id passed.
        :raises steamfront.errors.AppNotFound: Raised if the app or name provided can't be found.
        '''

        if appid is not None:

            # An app's ID was passed, get its object
            return _App(appid)
        elif name is not None:

            # A name was passed, get its ID and then return its object
            appid = self._getIDOfApp(name, caseSensitive)
            return _App(appid)
        else:

            # Neither was passed, raise MissingArguments
            raise _MissingArguments('Missing parameters: `name` or `appid`.')

    def getUser(self, *, name: str=None, id64: str=None) -> _User:
        '''
        Returns a :class:`steamfront.user.User` of the name or ID64 that was input to the function.

        :param str id64: The ID64 of a user you want the object of.
        :param str name: The Steam ID (name) of a user you want the object of. Names are case sensitive.
        :return: The object of relevant data on the user.
        :rtype: :class:`steamfront.user.User`
        :raises steamfront.errors.MissingArguments: Raised if there is neither a name or an ID64 passed.
        '''

        if id64 is not None:

            # A user's ID64 was passed, get its object
            return _User(id64, apiKey=self._apiKey)

        elif name is not None:

            # A user's name was passed, get its ID64 and then return its object
            raise NotImplementedError('This is yet to be implemented. Please use an ID64.')
            # id64 = self._getIDOfUser(name)
            # return _User(id64, apiKey=self._apiKey)
        else:

            # Neither was passed, raise MissingArguments
            raise _MissingArguments('Missing parameters: `name` or `id64`.')
