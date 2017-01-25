from .exceptions import *
from .user import *
from .game import *
from requests import get as _get


class Client(object):
    """
    Provides a front for the Steam store and all relevant applications and data

    Parameters
    ----------
        api_key : Optional[``str``]
                The key used for API functions. This is not required for all methods, but a good few of them.

    Attributes
    ----------
        api_key : The api key that was passed when the class was created. May be ``None``.
    """
    
    def __init__(self, *, api_key:str=None):

        self.api_key = api_key
        # '''The API key that was input with the class.'''
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
        Just calls :class:`Game` with the id passed into it.

        Parameters
        ----------
            appid : str, mandatory
                    The ID of the game you're trying to get.

        Returns
        ----------
            game : A :class:`Game` of the ID you entered.
        """

        return Game(appid)

    def get_game_from_name(self, name:str, *, refresh:bool=False, case_sensitive:bool=True) -> Game:
        """
        Gets the data from a game via its name
        Not guarenteed to be accurate
        Will return a list of given results

        Parameters
        ----------
            name : str, mandatory
                    The name of the game you're trying to find.
            refresh : bool, optional
                    Determines whether or not to repopulate the internal game list. Defaults to `False`.
            case_sensitive : bool, optional
                    Determines whether your search is case sensitive or not. Defaults to `True`.

        Returns
        ----------
            :class:`Game`
                This will be a game from a name, but it may not give the exact game you asked if there are
                games with duplicate names. If none are found, `False` is instead returned.
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

        Parameters
        ----------
        name : str
            The name of the game you're trying to get
        refresh : Optional[bool]
            Determines whether or not to repopulate the internal game list. Defaults to ``False``.
        case_sensitive : Optional[bool]
            Determines whether your search is case sensitive or not. Defaults to ``True``.

        Returns
        ----------
        ``list``
            This will be a list of ``tuple``s, containing a string of the name of the game as the first item, and the game's ID as 
            the second item.
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

        Parameters
        ----------
        name : str
            The name of the user you're trying to get

        Returns
        ----------
        User
            The user object from the name you're getting
        """

        return User(name, False)

    def get_user_from_id(self, id64:str):
        """
        Gets a user object from their ID64

        Parameters
        ----------
        id64 : str
            The ID64 of the user you're trying to get

        Returns
        ----------
        User
            The user object from the ID you're getting
        """

        return User(id64)
