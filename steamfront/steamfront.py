from .exceptions import *
from .user import *
from .game import *
from requests import get as _get


class Client(object):
    """
    Provides a front for the Steam store and all relevant applications and data

    :param str api_key: The key used for API functions. This is not required for all methods, but a good few of them. Defaults to ``None``.
    :type api_key: str or None
    :ivar api_key: The api key that was passed when the class was created. Can be ``None``.
    """
    
    def __init__(self, *, api_key:str=None):

        self.api_key = api_key
        self._steam_games = None

        # Populate game list
        self._get_steam_games()

    def _get_steam_games(self) -> list:
        """
        Gives a list of all games on Steam
        """

        # Get the list from the API
        dict_games = _get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/')

        # Get the list from the dictionary
        json_games = dict_games.json()
        game_list = json_games['applist']['apps']['app']

        # Store everything nicely
        self._steam_games = game_list
        return game_list

    def get_game_from_id(self, appid:str) -> Game:
        """
        Gets the information of a game from an appid.
        Just calls :class:`steamfront.game.Game` with the id passed into it.

        :param str appid: The ID of the game you're trying to get.
        :return: The :class:`steamfront.game.Game` object of the input app ID.
        :rtype: :class:`steamfront.game.Game`
        """

        return Game(appid)

    def get_game_from_name(self, name:str, *, refresh:bool=False, case_sensitive:bool=True) -> Game:
        """
        Gets the data from a game via its name
        Not guarenteed to be accurate
        Will return a list of given results

        :param str name: The name of the game you're trying to find.
        :param bool refresh: Determines whether or not to repopulate the internal game list. Defaults to `False`.
        :param bool case_sensitive: Determines whether your search is case sensitive or not. Defaults to `True`.
        :return: The :class:`steamfront.game.Game` object for a game that matches the name you searched. If none are found, ``False`` is returned.
        :rtype: :class:`steamfront.game.Game` or ``False``
        :raises GameDoesNotExist: In rare cases, an internally stored game may give an ID value that does not exist on the store. In that case, this will be thrown.
        """

        if refresh:
            self._get_steam_games()

        if case_sensitive:
            namecheck = lambda x, y: x == y 
        else:
            namecheck = lambda x, y: x.lower() == y.lower()

        for i in self._steam_games:
            if namecheck(i['name'], name):
                g = Game(i['appid'])
                return g

        return False

    def get_games_from_search(self, name:str, *, refresh:bool=False, case_sensitive:bool=True) -> list:
        """
        Gets a list of all the names matching a game via its name
        Not guarenteed to be accurate
        Will return a list of given results

        :param str name: The name of the game you're trying to find.
        :param bool refresh: Determines whether or not to repopulate the internal game list. Defaults to ``False``.
        :param bool case_sensitive: Determines whether your search is case sensitive or not. Defaults to ``True``.
        :return: A list of ``tuple`` as ``(GameName, GameID)``.
        :rtype: list
        """

        if refresh:
            self._get_steam_games()

        if case_sensitive:
            namecheck = lambda x, y: x == y 
        else:
            namecheck = lambda x, y: x.lower() == y.lower()

        game_tuple = []

        for i in self._steam_games:
            if namecheck(i['name'], name):
                n = i['name']
                d = i['appid']
                game_tuple.append((n, d))

        return game_tuple

    def get_user_from_name(self, name:str):
        """
        Gets a user object from its name

        :param str name: The name of the user you're trying to find.
        :return: The :class:`steamfront.user.User` object associated with the given name.
        :rtype: :class:`steamfront.user.User`
        :raises UserDoesNotExist: If the given ID does not belong to a user, the class will throw :class:`UserDoesNotExist`.
        """

        return User(name, False)

    def get_user_from_id(self, id64:str):
        """
        Gets a user object from their ID64

        :param str id64: The ID64 of the user you're trying to find.
        :return: The :class:`steamfront.user.User` object associated with the given name.
        :rtype: :class:`steamfront.user.User`
        :raises UserDoesNotExist: If the given ID64 does not belong to a user, the class will throw :class:`UserDoesNotExist`.
        """

        return User(id64)
